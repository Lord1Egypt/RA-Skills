#!/usr/bin/env node
/**
 * Kling AI image generation — text-to-image, image-to-image, 4K, series, subject
 * Node.js 18+, zero external deps
 */
import { submitTask, queryTask, pollTask, downloadFile } from './shared/task.mjs';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs, getTokenOrExit, readMediaAsValue, resolveAllowedOutputDir } from './shared/args.mjs';

const API_GEN = '/v1/images/generations';
const API_OMNI = '/v1/images/omni-image';

function normalizeModelName(v) {
  return String(v || '').trim();
}

function normalizeAliasKey(v) {
  return String(v || '').trim().toLowerCase().replace(/[\s_]+/g, '-');
}

function getImageModelAliasTarget(v) {
  const key = normalizeAliasKey(v);
  const aliasMap = new Map([
    ['omni3', 'kling-v3-omni'],
    ['omni-3', 'kling-v3-omni'],
    ['omni-v3', 'kling-v3-omni'],
    ['v3-omni', 'kling-v3-omni'],
    ['o3', 'kling-v3-omni'],
    ['O3', 'kling-v3-omni'],
    ['kling-image-o3', 'kling-v3-omni'],
    ['kling-o3', 'kling-v3-omni'],
    ['omni1', 'kling-image-o1'],
    ['omni-1', 'kling-image-o1'],
    ['o1', 'kling-image-o1'],
    ['kling-o1', 'kling-image-o1'],
  ]);
  return aliasMap.get(key) || '';
}

function validateModelAliasInput(rawModel) {
  if (!rawModel) return;
  const model = normalizeModelName(rawModel).toLowerCase();
  const target = getImageModelAliasTarget(rawModel);
  if (!target || model === target) return;
  throw new Error(
    `Invalid --model alias / --model 使用了别名: ${rawModel}\n`
    + `Use canonical name / 请改用标准名: ${target}\n`
    + 'Alias mapping / 别名映射: omni3 | omni v3 | o3 -> kling-v3-omni; image o1/omni1 -> kling-image-o1',
  );
}

function validateModelForRoute(apiPath, args) {
  validateModelAliasInput(args.model);
  const model = normalizeModelName(args.model);
  if (!model) return;

  // We only validate what we can be sure about from public enums.
  // - omni-image: only kling-v3-omni / kling-image-o1
  // - generations: must not use omni-only models
  if (apiPath === API_OMNI) {
    const allowed = new Set(['kling-v3-omni', 'kling-image-o1']);
    if (!allowed.has(model)) {
      throw new Error(
        `Invalid --model for omni-image / omni-image 不支持该模型: ${model}\n`
        + `Allowed / 允许: kling-v3-omni, kling-image-o1`,
      );
    }
  } else {
    const forbidden = new Set(['kling-v3-omni', 'kling-image-o1', 'kling-video-o1']);
    if (forbidden.has(model)) {
      throw new Error(
        `Invalid --model for generations / generations 不支持该模型: ${model}\n`
        + `Hint / 提示: remove --model or use kling-v3`,
      );
    }
  }
}

function parseImageInputs(rawImageArg) {
  if (!rawImageArg) return [];
  const parts = String(rawImageArg).split(',').map(s => s.trim());
  if (parts.some(p => !p)) {
    throw new Error(
      'Invalid --image list / --image 列表中存在空值；请移除空项并确保每个 image 非空。',
    );
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

function validateOmniRefCount(imageInputs, elementIds) {
  const totalRefs = imageInputs.length + elementIds.length;
  if (totalRefs > 10) {
    throw new Error(
      `Too many refs for omni-image / omni-image 参考图与主体总数超限: max 10 (current ${totalRefs})`,
    );
  }
}

function printHelp() {
  console.log(`Kling AI image generation

Usage:
  node kling.mjs image --prompt <text> [options]           # Text/image-to-image
  node kling.mjs image --prompt "..." [--resolution 4k]     # 4K / series / subject → Omni
  node kling.mjs image --model kling-v3-omni --prompt "..."  # explicit Omni model → omni-image (t2i / i2i)
  node kling.mjs image --task_id <id> [--download]         # Query/download

Submit (common):
  --prompt          Image description (required). Omni: <<<image_1>>> / <<<element_1>>>
  --resolution      1k / 2k / 4k (4k uses Omni)
  --aspect_ratio    Aspect ratio (default: 16:9 basic, auto for Omni)
  --n               Number of images 1-9
  --output_dir      Output dir (default: ./output)
  --no-wait         Submit only, do not wait
  --wait            Wait for completion (default)

Basic API:
  --negative_prompt Negative prompt
  --model           Model (default: kling-v3)

Omni (4K/series/subject):
  --model           kling-v3-omni / kling-image-o1
  --result_type     single / series (default: single)
  --series_amount   Series count 2-9 (when result_type=series)
  --image           Reference image path or URL, comma-separated for multiple
  --element_ids     Subject IDs, comma-separated
  (omni refs)       image count + element count <= 10

Query/download:
  --task_id         Task ID
  --download        Download if task succeeded

Env:
  credentials file  ~/.config/kling/.credentials (access_key_id, secret_access_key)
  KLING_TOKEN       Session-only Bearer (optional override)
  KLING_MEDIA_ROOTS Comma-separated extra dirs for --image / --output_dir (default: cwd only)
  KLING_ALLOW_ABSOLUTE_PATHS=1  Allow any local path (e.g. WSL downloads)`);
}

function useOmniApi(args) {
  // Match video.mjs chooseApiPath: explicit Omni image models → omni-image (incl. plain text-to-image).
  const m = normalizeModelName(args.model).toLowerCase();
  if (m === 'kling-v3-omni' || m === 'kling-image-o1') return true;
  if (args.element_ids) return true;
  if (args.result_type === 'series') return true;
  if ((args.resolution || '').toLowerCase() === '4k') return true;
  if ((args.aspect_ratio || '').toLowerCase() === 'auto') return true;
  if (args.image && args.image.includes(',')) return true;
  return false;
}

async function queryTaskAnyPath(taskId, token) {
  for (const apiPath of [API_OMNI, API_GEN]) {
    try {
      const data = await queryTask(apiPath, taskId, token);
      if (data && (data.task_status === 'succeed' || data.task_status === 'failed' || data.task_status === 'processing' || data.task_status === 'submitted')) {
        return { apiPath, data };
      }
    } catch (_) { /* try next */ }
  }
  throw new Error(`Task not found / 未找到任务: ${taskId}`);
}

function collectImageUrls(taskResult) {
  const urls = [];
  const append = (list) => {
    if (!Array.isArray(list)) return;
    for (const item of list) {
      if (item?.url) urls.push(item.url);
    }
  };
  append(taskResult?.images);
  append(taskResult?.series_images);
  if (urls.length === 0 && taskResult?.url) urls.push(taskResult.url);
  return urls;
}

async function pollAndDownloadImages(apiPath, taskId, outputDir, opts = {}) {
  const data = await pollTask(apiPath, taskId, opts);
  const urls = collectImageUrls(data?.task_result || {});
  if (urls.length === 0) {
    throw new Error('Task succeeded but missing image urls / 任务成功但未返回图片 URL');
  }
  const outPaths = [];
  for (let i = 0; i < urls.length; i++) {
    const outPath = join(outputDir, urls.length === 1 ? `${taskId}.png` : `${taskId}_${i}.png`);
    await downloadFile(urls[i], outPath);
    outPaths.push(outPath);
  }
  return outPaths;
}

export async function main() {
  const args = parseArgs(process.argv);
  if (args.help) { printHelp(); return; }
  validateModelAliasInput(args.model);

  const token = await getTokenOrExit();
  const outputDir = resolveAllowedOutputDir(args.output_dir || './output');
  const queryHint = `node kling.mjs image --task_id`;

  if (args.task_id && !args.prompt) {
    try {
      const { apiPath, data } = await queryTaskAnyPath(args.task_id, token);
      console.log(`Task ID / 任务 ID: ${args.task_id}`);
      console.log(`Status / 状态: ${data?.task_status || 'unknown'}`);
      const result = data?.task_result || {};
      const imageUrls = collectImageUrls(result);
      imageUrls.forEach((url, i) => {
        console.log(`Image / 图片[${i}]: ${url}`);
      });
      if (args.download && imageUrls.length > 0) {
        const { mkdir } = await import('node:fs/promises');
        await mkdir(outputDir, { recursive: true });
        for (let i = 0; i < imageUrls.length; i++) {
          const outPath = join(outputDir, imageUrls.length === 1 ? `${args.task_id}.png` : `${args.task_id}_${i}.png`);
          await downloadFile(imageUrls[i], outPath);
        }
      }
    } catch (e) {
      console.error(`Error / 错误: ${e.message}`);
      process.exit(1);
    }
    return;
  }

  if (!args.prompt) {
    console.error('Error / 错误: --prompt or --task_id required');
    console.error('Use --help / 使用 --help 查看帮助');
    process.exit(1);
  }

  const apiPath = useOmniApi(args) ? API_OMNI : API_GEN;
  const imageInputs = parseImageInputs(args.image);
  const elementIds = parseElementIds(args.element_ids);

  try {
    validateModelForRoute(apiPath, args);

    if (apiPath === API_GEN) {
      const payload = {
        model_name: args.model || 'kling-v3',
        prompt: args.prompt,
        negative_prompt: args.negative_prompt || '',
        n: parseInt(args.n || '1', 10),
        aspect_ratio: args.aspect_ratio || '16:9',
        resolution: args.resolution || '1k',
        callback_url: '',
      };
      if (imageInputs.length > 0) {
        payload.image = await readMediaAsValue(imageInputs[0]);
      }
      const result = await submitTask(API_GEN, payload, token);
      console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
      console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
      if (args.wait !== false) {
        console.log();
        const outPaths = await pollAndDownloadImages(API_GEN, result.taskId, outputDir, { token });
        console.log(`\n✓ Done / 完成: ${outPaths.length} image(s)`);
        outPaths.forEach((p) => console.log(`  - ${p}`));
      }
      return;
    }

    const payload = {
      model_name: args.model || 'kling-v3-omni',
      prompt: args.prompt,
      resolution: (args.resolution || '1k').toLowerCase(),
      aspect_ratio: (args.aspect_ratio || 'auto').toLowerCase(),
      result_type: args.result_type || 'single',
      callback_url: '',
    };
    if (payload.result_type === 'series') {
      if (imageInputs.length === 0) {
        throw new Error(
          'Invalid --result_type series without --image / 组图仅支持 i2i，请提供 --image（t2i 不支持 series）。',
        );
      }
      payload.series_amount = parseInt(args.series_amount || '4', 10);
    } else {
      payload.n = parseInt(args.n || '1', 10);
    }
    validateOmniRefCount(imageInputs, elementIds);
    if (imageInputs.length > 0) {
      payload.image_list = [];
      for (const img of imageInputs) {
        payload.image_list.push({ image: await readMediaAsValue(img) });
      }
    }
    if (elementIds.length > 0) {
      payload.element_list = elementIds.map(id => ({ element_id: id }));
    }

    const result = await submitTask(API_OMNI, payload, token);
    console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
    console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
    if (args.wait !== false) {
      console.log();
      const outPaths = await pollAndDownloadImages(API_OMNI, result.taskId, outputDir, { token });
      console.log(`\n✓ Done / 完成: ${outPaths.length} image(s)`);
      outPaths.forEach((p) => console.log(`  - ${p}`));
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
