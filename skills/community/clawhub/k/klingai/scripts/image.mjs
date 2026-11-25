#!/usr/bin/env node
/**
 * Kling AI image generation — text-to-image, image-to-image, 4K, series, subject, long page
 * Node.js 18+, zero external deps
 */
import { submitTask, queryTask, pollTask, downloadFile } from './shared/task.mjs';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs, getTokenOrExit, readMediaAsValue, resolveAllowedOutputDir } from './shared/args.mjs';

const API_GEN = '/v1/images/generations';
const API_OMNI = '/v1/images/omni-image';
const API_IMAGE_40 = '/image-generation/kling-4.0';
const API_LONG = '/long-image-generation/kling-4.0';
const API_TASKS = '/tasks';
const IMAGE_40_RESOLUTIONS = ['2k', '4k', '8k'];
const LONG_RESOLUTIONS = ['1k', '2k'];
const LONG_LENGTHS = ['short', 'medium', 'long'];
const LONG_IMAGE_TYPES = ['refer_image', 'style_refer_image', 'subject_refer_image'];
const IMAGE_40_ASPECTS = ['16:9', '9:16', '1:1', '4:3', '3:4', '3:2', '2:3', '21:9', 'auto'];

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
    ['kling-image-4.0', 'kling-4.0'],
    ['image-4.0', 'kling-4.0'],
    ['kling-4.0-image', 'kling-4.0'],
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
    + 'Alias mapping / 别名映射: omni3 | omni v3 | o3 -> kling-v3-omni; image o1/omni1 -> kling-image-o1; kling-image-4.0 | image-4.0 -> kling-4.0',
  );
}

function validateModelForRoute(apiPath, args) {
  validateModelAliasInput(args.model);
  const model = normalizeModelName(args.model).toLowerCase();
  if (!model) return;

  // We only validate what we can be sure about from public enums.
  // - image 4.0: kling-4.0
  // - omni-image: only kling-v3-omni / kling-image-o1
  // - generations: must not use omni-only models
  if (apiPath === API_IMAGE_40 || apiPath === API_LONG) {
    if (model !== 'kling-4.0') {
      throw new Error(
        `Invalid --model for image 4.0 / 图片 4.0 不支持该模型: ${model}\n`
        + 'Allowed / 允许: kling-4.0',
      );
    }
    return;
  }
  if (apiPath === API_OMNI) {
    const allowed = new Set(['kling-v3-omni', 'kling-image-o1']);
    if (!allowed.has(model)) {
      throw new Error(
        `Invalid --model for omni-image / omni-image 不支持该模型: ${model}\n`
        + `Allowed / 允许: kling-v3-omni, kling-image-o1`,
      );
    }
  } else {
    const allowed = new Set(['kling-v3', 'kling-v2-1']);
    if (!allowed.has(model)) {
      throw new Error(
        `Invalid --model for generations / generations 不支持该模型: ${model}\n`
        + `Allowed / 允许: kling-v3, kling-v2-1`,
      );
    }
  }
}

function parseImageInputs(rawImageArg) {
  if (!rawImageArg) return [];
  if (rawImageArg === true) {
    throw new Error('Invalid --image / --image 不能为空');
  }
  const parts = String(rawImageArg).split(',').map(s => s.trim());
  if (parts.some(p => !p)) {
    throw new Error(
      'Invalid --image list / --image 列表中存在空值；请移除空项并确保每个 image 非空。',
    );
  }
  return parts;
}

function rejectUnsupportedImageFlags(args) {
  if (args.refer_image || args.style_refer_image || args.subject_refer_image) {
    throw new Error(
      'Unsupported flag / 请使用 --image 搭配 --image_types（refer_image / style_refer_image / subject_refer_image）传入参考图',
    );
  }
  if (args.dynamic_range !== undefined || args.hdr !== undefined) {
    throw new Error(
      'Unsupported --dynamic_range / --hdr for image / 图片生成不支持动态范围（HDR），--dynamic_range sdr|hdr 仅视频 kling-4.0 支持',
    );
  }
}

function parseImageTypes(rawImageTypesArg, imageCount) {
  if (rawImageTypesArg === undefined || rawImageTypesArg === null || rawImageTypesArg === '') {
    return null;
  }
  if (rawImageTypesArg === true) {
    throw new Error(
      'Invalid --image_types / --image_types 不能为空。Allowed / 允许: refer_image, style_refer_image, subject_refer_image',
    );
  }
  if (imageCount === 0) {
    throw new Error(
      'Invalid --image_types without --image / 仅在传入 --image 时才能设置 --image_types',
    );
  }
  let parts = String(rawImageTypesArg).split(',').map((s) => s.trim().toLowerCase());
  for (const t of parts) {
    if (!t) continue;
    if (!LONG_IMAGE_TYPES.includes(t)) {
      throw new Error(
        `Invalid image type / 无效图片 type: ${t}. Allowed / 允许: refer_image, style_refer_image, subject_refer_image`,
      );
    }
  }
  if (parts.length === 1 && imageCount > 1 && parts[0] === 'refer_image') {
    parts = new Array(imageCount).fill('refer_image');
  }
  if (parts.length !== imageCount) {
    throw new Error(
      `Invalid --image_types / --image_types 数量需与 --image 一致: expected ${imageCount}, got ${parts.length}`,
    );
  }
  return parts;
}

function resolveLongImageTypes(page, imageInputs, parsedTypes) {
  if (page === 'ecommerce') {
    if (parsedTypes && parsedTypes.some((t) => t && t !== 'refer_image')) {
      throw new Error(
        'Unsupported --image_types for ecommerce / 电商详情页参考图仅支持 refer_image，不支持 style_refer_image、subject_refer_image（网页设计专用）',
      );
    }
    if (imageInputs.length < 1 || imageInputs.length > 3) {
      throw new Error('Invalid --image for ecommerce / 电商详情页需要 1-3 张参考图（refer_image）');
    }
    return new Array(imageInputs.length).fill('refer_image');
  }

  if (imageInputs.length === 0) return [];
  if (!parsedTypes || parsedTypes.some((t) => !t)) {
    throw new Error(
      'Missing --image_types for webpage / 网页设计传入 --image 时须通过 --image_types 指定 style_refer_image 或 subject_refer_image（不支持 refer_image）',
    );
  }
  if (parsedTypes.includes('refer_image')) {
    throw new Error(
      'Unsupported refer_image for webpage / 网页设计不支持 refer_image（电商详情页专用），请改用 style_refer_image 或 subject_refer_image',
    );
  }
  const styleCount = parsedTypes.filter((t) => t === 'style_refer_image').length;
  const subjectCount = parsedTypes.filter((t) => t === 'subject_refer_image').length;
  if (styleCount > 1) {
    throw new Error(
      'Too many style_refer_image for webpage / 网页设计风格参考图 style_refer_image 最多 1 张',
    );
  }
  if (subjectCount > 1) {
    throw new Error(
      'Too many subject_refer_image for webpage / 网页设计主体参考图 subject_refer_image 最多 1 张',
    );
  }
  return parsedTypes;
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
  node kling.mjs image --prompt <text> [options]           # default kling-4.0
  node kling.mjs image --prompt "..." --resolution 4k      # 2k / 4k / 8k on kling-4.0
  node kling.mjs image --prompt "..." --result_type series --series_amount auto
  node kling.mjs image --page ecommerce --image a.jpg --prompt "..."   # 电商详情页
  node kling.mjs image --page webpage --prompt "..."                   # 网页设计
  node kling.mjs image --page webpage --image s.jpg --image_types style_refer_image --prompt "..."
  node kling.mjs image --task_id <id> [--download]         # Query/download

Submit (common):
  --prompt          Image description (required). kling-4.0: @image_1 / @element_1. Omni: <<<image_1>>> / <<<element_1>>>
  --model           kling-4.0 (default) / kling-v3 / kling-v2-1 / kling-v3-omni / kling-image-o1
  --resolution      2k (default) / 4k / 8k. 1k: kling-v3 or kling-v2-1
  --aspect_ratio    kling-4.0: 16:9 / 9:16 / 1:1 / 4:3 / 3:4 / 3:2 / 2:3 / 21:9 / auto (default auto)
  --n               Number of images 1-9 (single). Not used for kling-4.0 series
  --result_type     single (default) / series. kling-4.0 series allows text or image
  --series_amount   kling-4.0: 2-10 or auto. Omitted --result_type selects series
  --image           Reference image, or a comma-separated list on kling-4.0 / Omni
  --element_ids     kling-4.0: image subjects, with images total <= 10. kling-v3 / Omni: element_list
  --output_dir      Output dir (default: ./output)
  --no-wait         Submit only, do not wait
  --wait            Wait for completion (default)

Basic (1k or --negative_prompt):
  --negative_prompt Negative prompt (kling-v3 / kling-v2-1, not with --image)
  --model           kling-v3 / kling-v2-1

Long page — only 电商详情页 or 网页设计:
  --page            ecommerce (电商详情页, 1-3 refer_image) / webpage (网页设计, text or style/subject refer images)
  --image_types     Type list aligned with --image: refer_image / style_refer_image / subject_refer_image
                    ecommerce: refer_image only (1-3, default if omitted)
                    webpage: style_refer_image (0-1) and/or subject_refer_image (0-1) only; required with --image
  --length          ecommerce only: short / medium (default) / long
  --resolution      1k (default) / 2k
  --prompt          @image_1 in --image order. No subjects, aspect, n, or series

Named kling-v3-omni / kling-image-o1:
  --model           the named model
  (omni refs)       image count + element count <= 10

Query/download:
  --task_id         Task ID
  --download        Download if task succeeded

Env:
  credentials file  ~/.config/kling/.credentials (api_key)
  KLING_API_KEY     Session-only Bearer (optional override)
  KLING_MEDIA_ROOTS Comma-separated extra dirs for --image / --output_dir (default: cwd only)
  KLING_ALLOW_ABSOLUTE_PATHS=1  Allow any local path (e.g. WSL downloads)`);
}

function useImage40Api(args) {
  const m = normalizeModelName(args.model).toLowerCase();
  if (m === 'kling-4.0') return true;
  if (m) return false;
  if ((args.resolution || '').toLowerCase() === '1k') return false;
  if (args.negative_prompt) return false;
  return true;
}

function useOmniApi(args) {
  const m = normalizeModelName(args.model).toLowerCase();
  if (m === 'kling-v3-omni' || m === 'kling-image-o1') return true;
  if (args.result_type === 'series') return true;
  if ((args.resolution || '').toLowerCase() === '4k') return true;
  if ((args.aspect_ratio || '').toLowerCase() === 'auto') return true;
  if (args.image && args.image.includes(',')) return true;
  return false;
}

function defaultOmniImageModel(args) {
  if ((args.resolution || '').toLowerCase() === '4k') return 'kling-v3-omni';
  if (args.result_type === 'series') return 'kling-v3-omni';
  return 'kling-image-o1';
}

async function queryTaskAnyPath(taskId, token) {
  for (const apiPath of [API_OMNI, API_GEN, API_TASKS]) {
    try {
      const data = await queryTask(apiPath, taskId, token);
      const status = data?.status || data?.task_status || '';
      if (status === 'succeed' || status === 'succeeded' || status === 'failed' || status === 'processing' || status === 'submitted') {
        return { apiPath, data };
      }
    } catch (_) { /* try next */ }
  }
  throw new Error(`Task not found / 未找到任务: ${taskId}`);
}

function collectImageUrls(source) {
  const urls = [];
  const append = (list) => {
    if (!Array.isArray(list)) return;
    for (const item of list) {
      if (item?.url) urls.push(item.url);
    }
  };
  if (Array.isArray(source?.outputs)) {
    for (const item of source.outputs) {
      if (item?.type === 'image' && item?.url) urls.push(item.url);
    }
    if (urls.length > 0) return urls;
  }
  const taskResult = source?.task_result || source || {};
  append(taskResult.images);
  append(taskResult.series_images);
  if (urls.length === 0 && taskResult.url) urls.push(taskResult.url);
  return urls;
}

function resolveImageResultType(args) {
  const hasSeriesAmount = args.series_amount != null && String(args.series_amount).trim() !== '';
  if (args.result_type === 'single' && hasSeriesAmount) {
    throw new Error('Invalid --series_amount with --result_type single / --series_amount 只能用于组图');
  }
  if (args.result_type && args.result_type !== 'single' && args.result_type !== 'series') {
    throw new Error('Invalid --result_type / 须为 single 或 series');
  }
  if (args.result_type) return args.result_type;
  return hasSeriesAmount ? 'series' : 'single';
}

function image40Settings(args) {
  const resolution = (args.resolution || '2k').toLowerCase();
  if (!IMAGE_40_RESOLUTIONS.includes(resolution)) {
    throw new Error(
      `Invalid --resolution for kling-4.0 / 图片 4.0 清晰度须为: ${IMAGE_40_RESOLUTIONS.join(', ')}`,
    );
  }
  const aspectRatio = (args.aspect_ratio || 'auto').toLowerCase();
  if (!IMAGE_40_ASPECTS.includes(aspectRatio)) {
    throw new Error(
      `Invalid --aspect_ratio for kling-4.0 / 图片 4.0 宽高比须为: ${IMAGE_40_ASPECTS.join(', ')}`,
    );
  }
  const resultType = resolveImageResultType(args);
  const settings = { result_type: resultType, resolution, aspect_ratio: aspectRatio };
  if (resultType === 'series') {
    const rawSeries = String(args.series_amount || '4').trim().toLowerCase();
    if (rawSeries === 'auto') {
      settings.series_amount = 'auto';
    } else {
      const n = parseInt(rawSeries, 10);
      if (!Number.isInteger(n) || n < 2 || n > 10) {
        throw new Error('Invalid --series_amount / 图片 4.0 组图张数须为 2-10 或 auto');
      }
      settings.series_amount = n;
    }
  } else {
    const n = parseInt(args.n || '1', 10);
    if (!Number.isInteger(n) || n < 1 || n > 9) {
      throw new Error('Invalid --n / 图片 4.0 单图张数须为 1-9');
    }
    settings.n = n;
  }
  return settings;
}

function longImagePage(args) {
  const page = String(args.page || '').trim().toLowerCase();
  if (!page) return '';
  if (page !== 'ecommerce' && page !== 'webpage') {
    throw new Error('Invalid --page / 须为 ecommerce（电商详情页）或 webpage（网页设计）');
  }
  return page;
}

function assertLongImageOnly(args) {
  if (args.element_ids) {
    throw new Error('Unsupported --element_ids for --page / 电商详情页与网页设计不支持主体');
  }
  if (args.negative_prompt) {
    throw new Error('Unsupported --negative_prompt for --page / 请把限制写进 --prompt');
  }
  if (args.aspect_ratio) {
    throw new Error('Unsupported --aspect_ratio for --page / 电商详情页与网页设计不使用宽高比');
  }
  if (args.n) {
    throw new Error('Unsupported --n for --page / 长图每次只生成一张');
  }
  if (args.result_type || args.series_amount) {
    throw new Error('Unsupported series for --page / 电商详情页与网页设计不是组图');
  }
}

function longImageSettings(args, page) {
  const resolution = (args.resolution || '1k').toLowerCase();
  if (!LONG_RESOLUTIONS.includes(resolution)) {
    throw new Error('Invalid --resolution for --page / 电商详情页与网页设计清晰度须为 1k 或 2k');
  }
  const settings = { skill: page, resolution };
  if (page === 'ecommerce') {
    const length = (args.length || 'medium').toLowerCase();
    if (!LONG_LENGTHS.includes(length)) {
      throw new Error('Invalid --length / 电商详情页长度须为 short、medium 或 long');
    }
    settings.length = length;
  } else if (args.length) {
    throw new Error('Unsupported --length for webpage / 网页设计不支持页面长度');
  }
  return settings;
}

async function pollAndDownloadImages(apiPath, taskId, outputDir, opts = {}) {
  const data = await pollTask(apiPath, taskId, opts);
  const urls = collectImageUrls(data);
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
  rejectUnsupportedImageFlags(args);

  const token = await getTokenOrExit();
  const outputDir = resolveAllowedOutputDir(args.output_dir || './output');
  const queryHint = `node kling.mjs image --task_id`;

  if (args.task_id && !args.prompt) {
    try {
      const { apiPath, data } = await queryTaskAnyPath(args.task_id, token);
      console.log(`Task ID / 任务 ID: ${args.task_id}`);
      console.log(`Status / 状态: ${data?.status || data?.task_status || 'unknown'}`);
      const imageUrls = collectImageUrls(data);
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

  let apiPath = API_GEN;

  try {
    const imageInputs = parseImageInputs(args.image);
    const elementIds = parseElementIds(args.element_ids);
    const parsedImageTypes = parseImageTypes(args.image_types, imageInputs.length);
    const page = longImagePage(args);
    if (!page) {
      args.result_type = resolveImageResultType(args);
      const named = normalizeModelName(args.model).toLowerCase();
      if (args.result_type === 'series' && (named === 'kling-v3' || named === 'kling-v2-1')) {
        throw new Error('Unsupported series for kling-v3 / kling-v2-1 / 组图使用默认的图片 kling-4.0，或显式 --model kling-v3-omni');
      }
    }
    apiPath = page
      ? API_LONG
      : (useImage40Api(args) ? API_IMAGE_40 : (useOmniApi(args) ? API_OMNI : API_GEN));
    if (!page && parsedImageTypes) {
      if (parsedImageTypes.some((t) => t === 'style_refer_image' || t === 'subject_refer_image')) {
        throw new Error(
          'Unsupported --image_types without --page webpage / style_refer_image 与 subject_refer_image 仅用于网页设计（--page webpage）',
        );
      }
      if (apiPath !== API_IMAGE_40) {
        throw new Error(
          'Unsupported --image_types / --image_types 仅用于长图（--page）或图片 kling-4.0',
        );
      }
    }
    if (!page && (args.resolution || '').toLowerCase() === '8k' && apiPath !== API_IMAGE_40) {
      throw new Error('Invalid --resolution 8k / 8k 仅图片 kling-4.0 支持，请去掉其它模型或使用默认模型');
    }
    if (!page && args.negative_prompt && apiPath !== API_GEN) {
      throw new Error('Unsupported --negative_prompt / 负向提示词仅 kling-v3 / kling-v2-1 文生图，且不能带 --image');
    }
    validateModelForRoute(apiPath, args);

    if (apiPath === API_LONG) {
      assertLongImageOnly(args);
      const longTypes = resolveLongImageTypes(page, imageInputs, parsedImageTypes);
      const settings = longImageSettings(args, page);
      const contents = [{ type: 'prompt', text: args.prompt }];
      for (let i = 0; i < imageInputs.length; i++) {
        contents.push({
          type: longTypes[i],
          url: await readMediaAsValue(imageInputs[i]),
          id: `image_${i + 1}`,
        });
      }
      const result = await submitTask(API_LONG, { contents, settings }, token);
      console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
      console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
      if (args.wait !== false) {
        console.log();
        const outPaths = await pollAndDownloadImages(API_TASKS, result.taskId, outputDir, { token });
        console.log(`\n✓ Done / 完成: ${outPaths.length} image(s)`);
        outPaths.forEach((p) => console.log(`  - ${p}`));
      }
      return;
    }

    if (apiPath === API_IMAGE_40) {
      if (args.negative_prompt) {
        throw new Error('Unsupported --negative_prompt for kling-4.0 / 图片 4.0 无负向提示词字段，请写进 --prompt');
      }
      if (imageInputs.length + elementIds.length > 10) {
        throw new Error(
          `Too many refs for kling-4.0 / 图片 4.0 参考图与主体总数超限: max 10 (current ${imageInputs.length + elementIds.length})`,
        );
      }
      const settings = image40Settings(args);
      const contents = [{ type: 'prompt', text: args.prompt }];
      for (let i = 0; i < imageInputs.length; i++) {
        contents.push({
          type: 'refer_image',
          url: await readMediaAsValue(imageInputs[i]),
          id: `image_${i + 1}`,
        });
      }
      for (let i = 0; i < elementIds.length; i++) {
        contents.push({
          type: 'element',
          element_id: String(elementIds[i]),
          id: `element_${i + 1}`,
        });
      }
      const result = await submitTask(API_IMAGE_40, { contents, settings }, token);
      console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
      console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
      if (args.wait !== false) {
        console.log();
        const outPaths = await pollAndDownloadImages(API_TASKS, result.taskId, outputDir, { token });
        console.log(`\n✓ Done / 完成: ${outPaths.length} image(s)`);
        outPaths.forEach((p) => console.log(`  - ${p}`));
      }
      return;
    }

    if (apiPath === API_GEN) {
      if (resolveImageResultType(args) === 'series') {
        throw new Error('Unsupported series for kling-v3 / kling-v2-1 / 组图使用默认的图片 kling-4.0，或显式 --model kling-v3-omni');
      }
      const modelName = (args.model || 'kling-v3').toLowerCase();
      if (args.negative_prompt && imageInputs.length > 0) {
        throw new Error(
          'Unsupported --negative_prompt with --image / 官网：图生图不支持负向提示词',
        );
      }
      if (elementIds.length && modelName === 'kling-v2-1') {
        throw new Error(
          'Unsupported --element_ids for kling-v2-1 / 官网：kling-v2-1 无 element_list，请用 kling-v3 或 Omni',
        );
      }
      if (imageInputs.length + elementIds.length > 10) {
        throw new Error(
          `Too many refs for generations / 参考图与主体总数超限: max 10 (current ${imageInputs.length + elementIds.length})`,
        );
      }
      const payload = {
        model_name: modelName,
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
      if (elementIds.length > 0) {
        payload.element_list = elementIds.map((id) => ({ element_id: id }));
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

    const hasRefImage = imageInputs.length > 0;
    const requestedAspect = (args.aspect_ratio || '').toLowerCase();
    if (requestedAspect === 'auto' && !hasRefImage) {
      throw new Error(
        'Invalid --aspect_ratio auto / 无参考图时不支持 auto，请指定 16:9 等固定比例，或提供 --image',
      );
    }
    const payload = {
      model_name: (args.model || defaultOmniImageModel(args)).toLowerCase(),
      prompt: args.prompt,
      resolution: (args.resolution || '1k').toLowerCase(),
      aspect_ratio: requestedAspect || (hasRefImage ? 'auto' : '16:9'),
      result_type: resolveImageResultType(args),
      callback_url: '',
    };
    if ((args.resolution || '').toLowerCase() === '4k' && payload.model_name === 'kling-image-o1') {
      throw new Error(
        'Invalid --resolution 4k for kling-image-o1 / Image O1 支持 1k/2k。4k 使用 kling-4.0',
      );
    }
    if (payload.result_type === 'series' && payload.model_name === 'kling-image-o1') {
      throw new Error(
        'Invalid --result_type series for kling-image-o1 / Image O1 不支持组图。组图使用 kling-4.0',
      );
    }
    if (payload.result_type === 'series') {
      if (imageInputs.length === 0) {
        throw new Error(
          'Invalid --result_type series without --image / 组图仅支持 i2i，请提供 --image（t2i 不支持 series）。',
        );
      }
      const rawSeries = String(args.series_amount || '4').trim().toLowerCase();
      if (rawSeries === 'auto') {
        payload.series_amount = 'auto';
      } else {
        const n = parseInt(rawSeries, 10);
        if (!Number.isInteger(n) || n < 2 || n > 9) {
          throw new Error('Invalid --series_amount / 须为 2-9 或 auto');
        }
        payload.series_amount = n;
      }
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
