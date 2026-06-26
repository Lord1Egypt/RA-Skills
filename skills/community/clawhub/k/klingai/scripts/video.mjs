#!/usr/bin/env node
/**
 * Kling AI video generation — text-to-video, image-to-video, Omni, multi-shot
 * Node.js 18+, zero external deps
 */
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { submitTask, queryTask, pollAndDownload, downloadFile } from './shared/task.mjs';
import { parseArgs, getTokenOrExit, readMediaAsValue, readOmniVideoRefUrl, resolveAllowedOutputDir } from './shared/args.mjs';

const API_T2V = '/v1/videos/text2video';
const API_I2V = '/v1/videos/image2video';
const API_OMNI = '/v1/videos/omni-video';

function normalizeModelName(v) {
  return String(v || '').trim();
}

/** Lowercase trim for route checks and API `model_name` enum matching. */
function normalizeModelKey(v) {
  return normalizeModelName(v).toLowerCase();
}

function normalizeAliasKey(v) {
  return String(v || '').trim().toLowerCase().replace(/[\s_]+/g, '-');
}

function getVideoModelAliasTarget(v) {
  const key = normalizeAliasKey(v);
  const aliasMap = new Map([
    ['omni3', 'kling-v3-omni'],
    ['omni-3', 'kling-v3-omni'],
    ['omni-v3', 'kling-v3-omni'],
    ['kling-video-o3', 'kling-v3-omni'],
    ['v3-omni', 'kling-v3-omni'],
    ['o3', 'kling-v3-omni'],
    ['O3', 'kling-v3-omni'],
    ['kling-o3', 'kling-v3-omni'],
    ['omni1', 'kling-video-o1'],
    ['omni-1', 'kling-video-o1'],
    ['o1', 'kling-video-o1'],
    ['kling-o1', 'kling-video-o1'],
  ]);
  return aliasMap.get(key) || '';
}

function validateModelAliasInput(rawModel) {
  if (!rawModel) return;
  const model = normalizeModelKey(rawModel);
  const target = getVideoModelAliasTarget(rawModel);
  if (!target || model === target) return;
  throw new Error(
    `Invalid --model alias / --model 使用了别名: ${rawModel}\n`
    + `Use canonical name / 请改用标准名: ${target}\n`
    + 'Alias mapping / 别名映射: omni3 | omni v3 | o3 -> kling-v3-omni; o1 | omni1 -> kling-video-o1',
  );
}

function normalizeSound(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return '';
  if (s === 'on' || s === 'off') return s;
  return s;
}

function normalizeReferType(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return 'base';
  return s;
}

function normalizeKeepOriginalSound(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return '';
  return s;
}

/** Multi-shot `shot_type`: `customize` | `intelligence` (empty → default customize when --multi_shot) */
function normalizeShotType(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return '';
  if (s === 'customize' || s === 'intelligence') return s;
  return s;
}

/**
 * Sets `multi_shot`, `shot_type`, and `prompt` / `multi_prompt` on payload (text2video / image2video / omni-video share rules).
 * Exits the process on validation error.
 * @param {Record<string, unknown>} payload
 * @param {Record<string, unknown>} args
 */
function mergeMultiShotIntoPayload(payload, args) {
  const rawShot = normalizeShotType(args.shot_type);
  const shotType = rawShot || 'customize';
  if (shotType !== 'customize' && shotType !== 'intelligence') {
    console.error(
      'Error / 错误: --shot_type must be customize or intelligence / 须为 customize 或 intelligence',
    );
    process.exit(1);
  }
  payload.multi_shot = true;
  payload.shot_type = shotType;

  if (shotType === 'customize') {
    if (!args.multi_prompt || !String(args.multi_prompt).trim()) {
      console.error(
        'Error / 错误: customize multi-shot requires --multi_prompt / 自定义分镜须提供 --multi_prompt',
      );
      process.exit(1);
    }
    try {
      payload.multi_prompt = JSON.parse(args.multi_prompt);
    } catch {
      console.error('Error / 错误: --multi_prompt must be valid JSON / 必须是合法 JSON');
      process.exit(1);
    }
    payload.prompt = '';
  } else {
    const p = String(args.prompt || '').trim();
    if (!p) {
      console.error(
        'Error / 错误: intelligence multi-shot requires non-empty --prompt / 智能分镜须提供非空 --prompt',
      );
      process.exit(1);
    }
    if (args.multi_prompt && String(args.multi_prompt).trim()) {
      console.error(
        'Error / 错误: intelligence multi-shot does not use --multi_prompt / 智能分镜请勿传 --multi_prompt',
      );
      process.exit(1);
    }
    payload.prompt = p;
  }
}

function validateModelForRoute(apiPath, args) {
  validateModelAliasInput(args.model);
  const model = normalizeModelKey(args.model);
  if (!model) return;

  // We only validate what we can be sure about from public enums.
  // - omni-video: only kling-v3-omni / kling-video-o1
  // - non-omni video: must not use omni-only models
  if (apiPath === API_OMNI) {
    const allowed = new Set(['kling-v3-omni', 'kling-video-o1']);
    if (!allowed.has(model)) {
      throw new Error(
        `Invalid --model for omni-video / omni-video 不支持该模型: ${model}\n`
        + `Allowed / 允许: kling-v3-omni, kling-video-o1`,
      );
    }
  } else {
    const forbidden = new Set(['kling-v3-omni', 'kling-video-o1', 'kling-image-o1']);
    if (forbidden.has(model)) {
      throw new Error(
        `Invalid --model for text2video/image2video / 文生/图生不支持该模型: ${model}\n`
        + `Hint / 提示: remove --model or use a basic video model (e.g. kling-v3, kling-v2-6)`,
      );
    }
  }
}

function validateSoundConstraints(apiPath, args) {
  const sound = normalizeSound(args.sound || 'off') || 'off';
  const model = normalizeModelKey(args.model);

  if (apiPath === API_OMNI && args.video && sound === 'on') {
    throw new Error(
      'Invalid --sound with Omni --video / Omni 参考视频时 sound 仅支持 off。\n'
      + 'Fix / 修复: remove --sound or set --sound off',
    );
  }
  if (model === 'kling-video-o1' && sound === 'on') {
    throw new Error(
      'Invalid --sound for kling-video-o1 / kling-video-o1 不支持 sound。\n'
      + 'Fix / 修复: set --sound off or omit it',
    );
  }
}

function validateOmniVideoListRules(args) {
  if (!args.video) {
    if (args.video_refer_type) {
      throw new Error(
        'Invalid --video_refer_type without --video / 仅在传入 --video 时才能设置 --video_refer_type。',
      );
    }
    if (args.keep_original_sound) {
      throw new Error(
        'Invalid --keep_original_sound without --video / 仅在传入 --video 时才能设置 --keep_original_sound。',
      );
    }
    return { referType: '', keepOriginalSound: '' };
  }

  const rawVideo = String(args.video).trim();
  if (!rawVideo) {
    throw new Error('Invalid --video / --video 不能为空，video_url 必须为非空公网 http(s) URL。');
  }
  if (rawVideo.includes(',')) {
    throw new Error('Invalid --video / 当前仅支持 1 段参考视频，请只传一个 video_url。');
  }

  const referType = normalizeReferType(args.video_refer_type);
  if (referType !== 'feature' && referType !== 'base') {
    throw new Error(
      `Invalid --video_refer_type / 无效 refer_type: ${referType}. Allowed / 允许: feature, base`,
    );
  }

  const keepOriginalSound = normalizeKeepOriginalSound(args.keep_original_sound);
  if (keepOriginalSound && keepOriginalSound !== 'yes' && keepOriginalSound !== 'no') {
    throw new Error(
      `Invalid --keep_original_sound / 无效 keep_original_sound: ${keepOriginalSound}. Allowed / 允许: yes, no`,
    );
  }

  return { referType, keepOriginalSound };
}

function parseImageInputs(rawImageArg) {
  if (!rawImageArg) return [];
  const parts = String(rawImageArg).split(',').map(s => s.trim());
  if (parts.some(p => !p)) {
    throw new Error(
      'Invalid --image list / --image 列表中存在空值；请移除空项并确保每个 image_url 非空。',
    );
  }
  return parts;
}

function parseImageTypes(rawImageTypesArg, imageCount) {
  if (!rawImageTypesArg) return new Array(imageCount).fill('');
  const parts = String(rawImageTypesArg).split(',').map(s => s.trim().toLowerCase());
  if (parts.length !== imageCount) {
    throw new Error(
      `Invalid --image_types / --image_types 数量需与 --image 一致: expected ${imageCount}, got ${parts.length}`,
    );
  }
  for (const t of parts) {
    if (!t) continue;
    if (t !== 'first_frame' && t !== 'end_frame') {
      throw new Error(
        `Invalid image type / 无效图片 type: ${t}. Allowed / 允许: first_frame, end_frame, empty`,
      );
    }
  }
  return parts;
}

function parseElementIds(rawElementIdsArg) {
  if (!rawElementIdsArg) return [];
  const parts = String(rawElementIdsArg).split(',').map(s => s.trim());
  if (parts.some(p => !p)) {
    throw new Error(
      'Invalid --element_ids list / --element_ids 列表中存在空值；请移除空项并确保每个 element_id 非空。',
    );
  }
  return parts;
}

function validateOmniImageListRules(args, imageInputs, imageTypes, hasTailArg) {
  // API limit: with reference video max 4 images, otherwise max 7.
  const maxImages = args.video ? 4 : 7;
  const totalImages = imageInputs.length + (hasTailArg ? 1 : 0);
  if (totalImages > maxImages) {
    throw new Error(
      `Too many images for omni-video / omni-video 图片数量超限: max ${maxImages} (current ${totalImages})`,
    );
  }

  const hasFirstFrame = imageTypes.includes('first_frame');
  const hasEndFrame = imageTypes.includes('end_frame') || hasTailArg;

  if (hasEndFrame && !hasFirstFrame) {
    throw new Error(
      'Invalid image_list: end_frame needs first_frame / 不支持仅尾帧，配置 end_frame 时必须同时有 first_frame。',
    );
  }

  // O1 + >2 images does not support end_frame.
  const model = normalizeModelKey(args.model);
  if (model === 'kling-video-o1' && hasEndFrame && totalImages > 2) {
    throw new Error(
      'Invalid image_list for kling-video-o1 / kling-video-o1 在图片数超过 2 时不支持任何 end_frame。',
    );
  }

  // Frame generation cannot be used with video editing (base).
  const hasFrame = hasFirstFrame || hasEndFrame;
  if (hasFrame && args.video && normalizeReferType(args.video_refer_type) === 'base') {
    throw new Error(
      'Invalid combo: frame images with video edit / 首帧或尾帧生视频不能与视频编辑（--video_refer_type base）同时使用。',
    );
  }
  return { totalImages, hasFirstFrame, hasEndFrame };
}

function validateOmniElementListRules(args, elementIds, imageState) {
  if (!elementIds.length) return;
  const model = normalizeModelKey(args.model);
  const hasFirstAndEnd = imageState.hasFirstFrame && imageState.hasEndFrame;

  // Frame-generation with subjects supports up to 3 subjects.
  if ((imageState.hasFirstFrame || imageState.hasEndFrame) && elementIds.length > 3) {
    throw new Error(
      `Too many subjects with frame generation / 首帧或尾帧生视频时主体最多 3 个: current ${elementIds.length}`,
    );
  }

  // First+last frame with O1 does not support subjects.
  if (hasFirstAndEnd && model === 'kling-video-o1') {
    throw new Error(
      'Invalid element_list for kling-video-o1 / kling-video-o1 在首尾帧生视频场景不支持主体。',
    );
  }

  // Combined reference count limit: images + elements.
  const totalRefs = imageState.totalImages + elementIds.length;
  const maxRefs = args.video ? 4 : 7;
  if (totalRefs > maxRefs) {
    throw new Error(
      `Too many refs for omni-video / omni-video 参考图与主体总数超限: max ${maxRefs} (current ${totalRefs})`,
    );
  }
}

function printHelp() {
  console.log(`Kling AI video generation

Usage:
  node kling.mjs video --prompt <text> [options]               # Text-to-video
  node kling.mjs video --image <path|url> [--prompt ...]       # Image-to-video
  node kling.mjs video --prompt "..." [--image ...] [--element_ids ...]  # Omni
  node kling.mjs video --multi_shot --shot_type customize --multi_prompt <json>  # Multi-shot (customize)
  node kling.mjs video --multi_shot --shot_type intelligence --prompt "..."       # Multi-shot (intelligence)
  node kling.mjs video --task_id <id> [--download]              # Query/download

Submit (common):
  --prompt          Video description (Omni: <<<element_1>>> <<<image_1>>> <<<video_1>>>)
  --duration        Duration 3-15 s (default: 5)
  --model           T2V/I2V: kling-v3 / kling-v2-6 / …; explicit kling-v3-omni or kling-video-o1 → omni-video (simple t2v/i2v too). Omni default: kling-v3-omni or kling-video-o1
  --mode            pro / std (default: pro)
  --aspect_ratio    16:9 / 9:16 / 1:1 (default: 16:9). With --image, this routes to omni-video
  --sound           on / off (default: off). v3/omni support; with --video only off; o1 no sound
  --negative_prompt Negative prompt
  --output_dir      Output dir (default: ./output)
  --no-wait         Submit only, do not wait
  --wait            Wait for completion (default)

Image-to-video / Omni:
  --image           Image list path or URL (comma-separated for Omni)
  --image_types     Optional type list aligned with --image (comma-separated): first_frame/end_frame/empty
  --image_tail      Last-frame image
  --element_ids     Subject IDs, comma-separated (Omni; combined limits with images)
  --video           Omni reference video: public http(s) URL only (video_list[].video_url)
  --video_refer_type feature / base (default: base)
  --keep_original_sound yes / no (optional; works for feature/base)

Multi-shot (text2video / image2video / omni-video; same rules; see SKILL.md):
  --multi_shot      Enable multi-shot (with customize, top-level --prompt unused; not with --image_tail)
  --shot_type       customize | intelligence (required when multi_shot; default: customize)
  --multi_prompt    customize only: JSON array, max 6 shots, durations sum to --duration
  --prompt          intelligence: required (model splits shots); customize: ignored if set

Query/download:
  --task_id         Task ID
  --download        Download if task succeeded

Watermark:
  --watermark       Generate with watermark (adds watermark_info: {enabled: true})

Env:
  credentials file  ~/.config/kling/.credentials (access_key_id, secret_access_key)
  KLING_TOKEN       Session-only Bearer (optional override)
  KLING_MEDIA_ROOTS Comma-separated extra dirs for local media / --output_dir (default: cwd only)
  KLING_ALLOW_ABSOLUTE_PATHS=1  Allow any local path (e.g. WSL downloads outside project)`);
}

function chooseApiPath(args) {
  if (args.element_ids || args.video) return API_OMNI;
  const m = normalizeModelKey(args.model);
  const explicitOmniModel = m === 'kling-v3-omni' || m === 'kling-video-o1';
  if (args.image) {
    const images = args.image.split(',').map(s => s.trim()).filter(Boolean);
    // image2video does not support aspect_ratio; route to omni-video when explicitly provided.
    if (args.aspect_ratio) return API_OMNI;
    if (images.length > 1) return API_OMNI;
    if (explicitOmniModel) return API_OMNI;
    return API_I2V;
  }
  if (explicitOmniModel) return API_OMNI;
  return API_T2V;
}

async function queryTaskAnyPath(taskId, token) {
  const paths = [API_OMNI, API_I2V, API_T2V];
  for (const apiPath of paths) {
    try {
      const data = await queryTask(apiPath, taskId, token);
      if (data && (data.task_status === 'succeed' || data.task_status === 'failed' || data.task_status === 'processing' || data.task_status === 'submitted')) {
        return { apiPath, data };
      }
    } catch (_) { /* try next */ }
  }
  throw new Error(`Task not found / 未找到任务: ${taskId}`);
}

export async function main() {
  const args = parseArgs(process.argv, ['multi_shot']);
  if (args.help) { printHelp(); return; }
  validateModelAliasInput(args.model);

  const token = await getTokenOrExit();
  const outputDir = resolveAllowedOutputDir(args.output_dir || './output');

  if (args.task_id && !args.prompt && !args.image && !args.multi_shot) {
    try {
      const { apiPath, data } = await queryTaskAnyPath(args.task_id, token);
      console.log(`Task ID / 任务 ID: ${args.task_id}`);
      console.log(`Status / 状态: ${data?.task_status || 'unknown'}`);
      if (data?.task_status_msg) console.log(`Message / 消息: ${data.task_status_msg}`);
      const videos = data?.task_result?.videos || [];
      if (videos.length > 0 && videos[0].url) {
        console.log(`Video URL / 视频链接: ${videos[0].url}`);
        if (videos[0].watermark_url) {
          console.log(`Watermark URL / 水印视频: ${videos[0].watermark_url}`);
        }
        if (args.download) {
          const { mkdir } = await import('node:fs/promises');
          const { join } = await import('node:path');
          await mkdir(outputDir, { recursive: true });
          await downloadFile(videos[0].url, join(outputDir, `${args.task_id}.mp4`));
        }
      }
    } catch (e) {
      console.error(`Error / 错误: ${e.message}`);
      process.exit(1);
    }
    return;
  }

  const imageInputs = parseImageInputs(args.image);
  const imageTypes = parseImageTypes(args.image_types, imageInputs.length);
  const elementIds = parseElementIds(args.element_ids);
  const aspectForcesOmni = Boolean(args.image && args.aspect_ratio && imageInputs.length > 0);
  const videoState = validateOmniVideoListRules(args);
  const hasImage = imageInputs.length > 0;
  if (!args.prompt && !hasImage && !args.multi_shot) {
    console.error('Error / 错误: --prompt, --image, or --multi_shot required');
    console.error('Use --help / 使用 --help 查看帮助');
    process.exit(1);
  }

  if (args.image_tail && !hasImage) {
    console.error('Error / 错误: --image_tail requires --image (first frame) / 首尾帧需要首帧 --image');
    process.exit(1);
  }

  if (args.multi_shot && args.image_tail) {
    console.error(
      'Error / 错误: multi-shot does not support first+last frame (--image_tail) / 多镜头不支持首尾帧生视频，请去掉 --image_tail',
    );
    process.exit(1);
  }

  if (hasImage) {
    const firstInput = imageInputs[0];
    const isUrl = firstInput.startsWith('http://') || firstInput.startsWith('https://');
    if (!isUrl && !existsSync(resolve(firstInput))) {
      console.error(`Error / 错误: image not found / 图片不存在: ${firstInput}`);
      process.exit(1);
    }
  }

  const apiPath = chooseApiPath(args);
  const queryHint = `node kling.mjs video --task_id`;
  if (apiPath === API_OMNI && aspectForcesOmni && args.model) {
    const model = normalizeModelKey(args.model);
    const isOmniModel = model === 'kling-v3-omni' || model === 'kling-video-o1';
    if (!isOmniModel) {
      console.error(
        `Error / 错误: --model ${model} does not support --aspect_ratio with --image.\n`
        + 'Use omni model / 请使用 Omni 模型: kling-v3-omni or kling-video-o1',
      );
      process.exit(1);
    }
  }
  if (apiPath === API_OMNI && aspectForcesOmni && args.negative_prompt) {
    console.error(
      'Info / 提示: omni-video does not support --negative_prompt; this parameter will be ignored',
    );
  }

  try {
    validateModelForRoute(apiPath, args);
    validateSoundConstraints(apiPath, args);

    if (apiPath === API_T2V) {
      const payload = {
        model_name: args.model ? normalizeModelKey(args.model) : 'kling-v3',
        negative_prompt: args.negative_prompt || '',
        duration: String(args.duration || '5'),
        mode: args.mode || 'pro',
        aspect_ratio: args.aspect_ratio || '16:9',
        sound: args.sound || 'off',
        callback_url: '',
        external_task_id: '',
      };
      if (args.watermark) payload.watermark_info = { enabled: true };
      if (args.multi_shot) {
        mergeMultiShotIntoPayload(payload, args);
      } else {
        const p = String(args.prompt || '').trim();
        if (!p) {
          console.error(
            'Error / 错误: text-to-video requires --prompt when not using --multi_shot / 文生视频非多镜头须提供 --prompt',
          );
          process.exit(1);
        }
        payload.prompt = args.prompt;
      }
      const result = await submitTask(API_T2V, payload, token);
      console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
      console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
      if (args.wait !== false) {
        console.log();
        const outPath = await pollAndDownload(API_T2V, result.taskId, outputDir, { token });
        console.log(`\n✓ Done / 完成: ${outPath}`);
      }
      return;
    }

    if (apiPath === API_I2V) {
      const payload = {
        model_name: args.model ? normalizeModelKey(args.model) : 'kling-v3',
        image: await readMediaAsValue(args.image),
        image_tail: args.image_tail ? await readMediaAsValue(args.image_tail) : '',
        negative_prompt: args.negative_prompt || '',
        duration: String(args.duration || '5'),
        mode: args.mode || 'pro',
        sound: args.sound || 'off',
        callback_url: '',
        external_task_id: '',
      };
      if (args.watermark) payload.watermark_info = { enabled: true };
      if (args.multi_shot) {
        mergeMultiShotIntoPayload(payload, args);
      } else {
        payload.prompt = args.prompt || '';
      }
      const result = await submitTask(API_I2V, payload, token);
      console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
      console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
      if (args.wait !== false) {
        console.log();
        const outPath = await pollAndDownload(API_I2V, result.taskId, outputDir, { token });
        console.log(`\n✓ Done / 完成: ${outPath}`);
      }
      return;
    }

    const payload = {
      model_name: args.model ? normalizeModelKey(args.model) : 'kling-v3-omni',
      duration: String(args.duration || '5'),
      mode: args.mode || 'pro',
      sound: args.sound || 'off',
      callback_url: '',
    };
    const hasFirstFrameRef = imageTypes.includes('first_frame');
    const usesVideoEdit = Boolean(args.video && normalizeReferType(args.video_refer_type) === 'base');
    const requireAspectRatio = !hasFirstFrameRef && !usesVideoEdit;
    if (args.aspect_ratio) {
      payload.aspect_ratio = args.aspect_ratio;
    } else if (requireAspectRatio) {
      payload.aspect_ratio = '16:9';
    }
    if (args.watermark) payload.watermark_info = { enabled: true };

    if (args.multi_shot) {
      mergeMultiShotIntoPayload(payload, args);
    } else {
      const p = String(args.prompt || '').trim();
      if (!p) {
        console.error(
          'Error / 错误: Omni (non-multi-shot) requires non-empty --prompt / 非多镜头 Omni 须提供非空 --prompt',
        );
        process.exit(1);
      }
      payload.multi_shot = false;
      payload.prompt = args.prompt;
    }

    const imageList = [];
    let imageState = { totalImages: 0, hasFirstFrame: false, hasEndFrame: false };
    if (imageInputs.length > 0 || args.image_tail) {
      imageState = validateOmniImageListRules(args, imageInputs, imageTypes, Boolean(args.image_tail));
    }
    validateOmniElementListRules(args, elementIds, imageState);
    if (imageInputs.length > 0) {
      for (let i = 0; i < imageInputs.length; i++) {
        const item = { image_url: await readMediaAsValue(imageInputs[i]) };
        if (imageTypes[i]) item.type = imageTypes[i];
        imageList.push(item);
      }
    }
    if (args.image_tail) {
      imageList.push({ image_url: await readMediaAsValue(args.image_tail), type: 'end_frame' });
    }
    if (imageList.length > 0) payload.image_list = imageList;

    if (elementIds.length > 0) {
      payload.element_list = elementIds.map(id => {
        return { element_id: String(id.trim()) };
      });
    }

    if (args.video) {
      const videoUrl = readOmniVideoRefUrl(args.video);
      const videoItem = { video_url: videoUrl, refer_type: videoState.referType };
      if (videoState.keepOriginalSound) videoItem.keep_original_sound = videoState.keepOriginalSound;
      payload.video_list = [videoItem];
    }

    const result = await submitTask(API_OMNI, payload, token);
    console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
    console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
    if (args.wait !== false) {
      console.log();
      const outPath = await pollAndDownload(API_OMNI, result.taskId, outputDir, { token });
      console.log(`\n✓ Done / 完成: ${outPath}`);
    }
  } catch (e) {
    console.error(`Error / 错误: ${e.message}`);
    process.exit(1);
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`Error / 错误: ${e?.message || e}`);
    process.exit(1);
  });
}
