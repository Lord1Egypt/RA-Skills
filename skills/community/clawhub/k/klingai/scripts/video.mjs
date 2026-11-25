#!/usr/bin/env node
/**
 * Kling AI video generation — text-to-video, image-to-video, Omni, multi-shot
 * Node.js 18+, zero external deps
 *
 * Paths and body fields follow official docs:
 * https://klingai.com/document-api/llms.txt
 */
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  submitTask,
  queryTask,
  pollAndDownload,
  downloadFile,
  taskStatusOf,
  taskMessageOf,
  isTaskSucceeded,
  resultUrlOf,
} from './shared/task.mjs';
import { parseArgs, getTokenOrExit, readMediaAsValue, readOmniVideoRefUrl, resolveAllowedOutputDir } from './shared/args.mjs';

const API_TASKS = '/tasks';

const RANGE_3_15 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
const RANGE_3_10 = [3, 4, 5, 6, 7, 8, 9, 10];
const RANGE_3_20 = Array.from({ length: 18 }, (_, i) => i + 3);
const RANGE_3_30 = Array.from({ length: 28 }, (_, i) => i + 3);
const DURATION_5_10 = [5, 10];
const RES_720 = ['720p'];
const RES_720_1080 = ['720p', '1080p'];
const RES_720_1080_4K = ['720p', '1080p', '4k'];
const DYNAMIC_RANGES = ['sdr', 'hdr'];

/** Official video models (path-encoded). Source: klingai.com/document-api */
const BASIC_MODELS = {
  'kling-3.0': {
    t2v: '/text-to-video/kling-3.0',
    i2v: '/image-to-video/kling-3.0',
    durations: RANGE_3_15,
    resolutions: RES_720_1080_4K,
    audio: ['native', 'off'],
    multiShot: true,
    lastFrame: true,
    i2vElements: true,
    t2vPromptField: true,
  },
  'kling-3.0-turbo': {
    t2v: '/text-to-video/kling-3.0-turbo',
    i2v: '/image-to-video/kling-3.0-turbo',
    durations: RANGE_3_15,
    resolutions: RES_720_1080,
    audio: null,
    multiShot: false,
    lastFrame: false,
    t2vPromptField: true,
  },
  'kling-2.6': {
    t2v: '/text-to-video/kling-2.6',
    i2v: '/image-to-video/kling-2.6',
    durations: DURATION_5_10,
    resolutions: RES_720_1080,
    audio: ['native', 'off'],
    multiShot: false,
    lastFrame: true,
    t2vPromptField: true,
    audioRequires1080p: true,
    lastFrameRequires1080pSilent: true,
    maxVoices: 2,
  },
  'kling-2.5-turbo': {
    t2v: '/text-to-video/kling-2.5-turbo',
    i2v: '/image-to-video/kling-2.5-turbo',
    durations: DURATION_5_10,
    resolutions: RES_720_1080,
    audio: null,
    multiShot: false,
    lastFrame: true,
    t2vPromptField: true,
    lastFrameRequires1080p: true,
  },
  'kling-4.0': {
    t2v: '/text-to-video/kling-4.0',
    i2v: '/image-to-video/kling-4.0',
    durations: RANGE_3_30,
    resolutions: RES_720_1080_4K,
    dynamicRanges: DYNAMIC_RANGES,
    audio: null,
    multiShot: false,
    lastFrame: true,
    middleFrame: true,
    maxImages: 10,
    t2vPromptField: true,
  },
  'kling-4.0-flash': {
    t2v: '/text-to-video/kling-4.0-flash',
    i2v: '/image-to-video/kling-4.0-flash',
    durations: RANGE_3_20,
    resolutions: RES_720,
    audio: null,
    multiShot: false,
    lastFrame: false,
    t2vPromptField: true,
  },
};

const OMNI_MODELS = {
  'kling-3.0-omni': {
    path: '/omni-video/kling-3.0-omni',
    durations: RANGE_3_15,
    resolutions: RES_720_1080_4K,
    audio: ['native', 'original', 'off'],
    multiShot: true,
    lastFrame: true,
    maxImages: 7,
    maxImagesWithVideo: 4,
    maxRefs: 7,
    maxRefsWithVideo: 4,
    maxVideos: 1,
    frameMaxElements: 3,
  },
  'kling-o1': {
    path: '/omni-video/kling-o1',
    durations: RANGE_3_10,
    resolutions: RES_720_1080,
    audio: ['original', 'off'],
    multiShot: false,
    lastFrame: true,
    maxImages: 7,
    maxImagesWithVideo: 4,
    maxRefs: 7,
    maxRefsWithVideo: 4,
    maxVideos: 1,
    frameMaxElements: 3,
  },
  'kling-4.0': {
    path: '/omni-video/kling-4.0',
    durations: RANGE_3_30,
    defaultAspectRatio: '',
    resolutions: RES_720_1080_4K,
    dynamicRanges: DYNAMIC_RANGES,
    audio: ['original', 'native'],
    multiShot: false,
    lastFrame: true,
    middleFrame: true,
    maxImages: 10,
    maxImagesWithVideo: 10,
    maxVideos: 5,
    // images + videos + elements + voices <= 15
    maxRefs: 15,
    maxElements: 7,
    maxVoices: 3,
  },
  'kling-4.0-flash': {
    path: '/omni-video/kling-4.0-flash',
    durations: RANGE_3_20,
    defaultAspectRatio: '',
    resolutions: RES_720,
    audio: ['original', 'native'],
    multiShot: false,
    lastFrame: true,
    maxImages: 10,
    maxImagesWithVideo: 10,
    maxVideos: 5,
    // images + videos + elements <= 15. Create API has no contents type=voice.
    maxRefs: 15,
    maxElements: 7,
  },
};

const FRAME_TYPES = ['first_frame', 'middle_frame', 'last_frame'];

const LEGACY_MODEL_RENAMES = new Map([
  ['kling-v3', 'kling-3.0'],
  ['kling-v3-omni', 'kling-3.0-omni'],
  ['kling-video-o1', 'kling-o1'],
  ['kling-v2-6', 'kling-2.6'],
  ['kling-v2-5-turbo', 'kling-2.5-turbo'],
]);

function normalizeModelName(v) {
  return String(v || '').trim();
}

function normalizeModelKey(v) {
  return normalizeModelName(v).toLowerCase();
}

function normalizeAliasKey(v) {
  return String(v || '').trim().toLowerCase().replace(/[\s_]+/g, '-');
}

function getVideoModelAliasTarget(v) {
  const key = normalizeAliasKey(v);
  const aliasMap = new Map([
    ['omni3', 'kling-3.0-omni'],
    ['omni-3', 'kling-3.0-omni'],
    ['omni-v3', 'kling-3.0-omni'],
    ['kling-video-o3', 'kling-3.0-omni'],
    ['v3-omni', 'kling-3.0-omni'],
    ['o3', 'kling-3.0-omni'],
    ['kling-o3', 'kling-3.0-omni'],
    ['omni1', 'kling-o1'],
    ['omni-1', 'kling-o1'],
    ['o1', 'kling-o1'],
    ['kling-video-o1', 'kling-o1'],
    ['kling-4.0-omni', 'kling-4.0'],
    ['kling-4.0-flash-omni', 'kling-4.0-flash'],
  ]);
  return aliasMap.get(key) || '';
}

function validateModelAliasInput(rawModel) {
  if (!rawModel) return;
  const model = normalizeModelKey(rawModel);
  const renamed = LEGACY_MODEL_RENAMES.get(model);
  if (renamed) {
    throw new Error(
      `Invalid --model / 请改用官网模型名: ${rawModel} → ${renamed}`,
    );
  }
  const target = getVideoModelAliasTarget(rawModel);
  if (!target || model === target) return;
  throw new Error(
    `Invalid --model alias / --model 使用了别名: ${rawModel}\n`
    + `Use canonical name / 请改用标准名: ${target}\n`
    + 'Alias mapping / 别名映射: omni3 | omni v3 | o3 -> kling-3.0-omni; o1 | omni1 -> kling-o1; '
    + 'kling-4.0-omni -> kling-4.0; kling-4.0-flash-omni -> kling-4.0-flash '
    + '(one name for T2V / I2V / Omni; route follows flags / 4.0、4.0 Flash 三种接口同名，按参数分流)',
  );
}

function parseBoolFlag(raw, flagName) {
  if (raw === undefined || raw === null || raw === '') return undefined;
  if (raw === true) return true;
  const s = String(raw).trim().toLowerCase();
  if (s === 'true' || s === '1' || s === 'yes') return true;
  if (s === 'false' || s === '0' || s === 'no') return false;
  throw new Error(`Invalid ${flagName} / ${flagName} 须为 true 或 false`);
}

function parseDuration(raw, fallback = 5) {
  if (raw == null || raw === '') {
    if (fallback == null) return null;
    raw = fallback;
  }
  const n = parseInt(String(raw), 10);
  if (!Number.isInteger(n)) {
    throw new Error('Invalid --duration / --duration 须为整数秒');
  }
  return n;
}

function parseResolution(raw) {
  if (!raw) return '';
  return String(raw).trim().toLowerCase();
}

function parseDynamicRange(raw) {
  if (raw === undefined || raw === null) return '';
  if (typeof raw !== 'string') {
    throw new Error('Invalid --dynamic_range / --dynamic_range 须为字符串枚举: sdr, hdr');
  }
  const s = raw.trim().toLowerCase();
  if (!s) {
    throw new Error('Invalid --dynamic_range / --dynamic_range 不能为空，允许值: sdr, hdr');
  }
  return s;
}

function parseAudio(raw) {
  if (!raw) return '';
  return String(raw).trim().toLowerCase();
}

function normalizeReferType(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return 'base';
  return s;
}

function isBaseVideoEdit(videoState) {
  return Boolean(videoState?.hasBase);
}

function shouldSendOmniAspectRatio(args, imageState, videoState) {
  if (args.aspect_ratio) return true;
  return !imageState.hasFirstFrame && !isBaseVideoEdit(videoState);
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
    if (t === 'end_frame') {
      throw new Error(
        'Invalid image type end_frame / 请改用 last_frame（官网枚举）',
      );
    }
    if (!FRAME_TYPES.includes(t) && t !== 'refer_image') {
      throw new Error(
        `Invalid image type / 无效图片 type: ${t}. Allowed / 允许: first_frame, middle_frame (kling-4.0), last_frame, refer_image, empty`,
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

function parseVoiceIds(rawVoiceIdsArg) {
  if (!rawVoiceIdsArg) return [];
  const parts = String(rawVoiceIdsArg).split(',').map(s => s.trim());
  if (parts.some(p => !p)) {
    throw new Error(
      'Invalid --voice_ids list / --voice_ids 列表中存在空值；请移除空项并确保每个 voice_id 非空。',
    );
  }
  return parts;
}

function validateVoices(route, model, spec, voiceIds) {
  if (!voiceIds.length) return;
  if (model === 'kling-4.0' && route !== 'omni') {
    throw new Error(
      `Unsupported --voice_ids for ${model} text/image-to-video / ${model} 音色仅 Omni 全能参考支持，文生视频和图生视频不要传 --voice_ids`,
    );
  }
  if (model === 'kling-2.6' && route !== 'i2v') {
    throw new Error(
      'Unsupported --voice_ids for kling-2.6 text-to-video / kling-2.6 音色仅图生视频支持，文生视频不要传 --voice_ids',
    );
  }
  if (!spec.maxVoices) {
    throw new Error(
      `Unsupported --voice_ids for ${model} / 音色仅 kling-4.0 的 Omni、kling-2.6 的图生视频支持（contents type=voice）`,
    );
  }
  if (voiceIds.length > spec.maxVoices) {
    throw new Error(
      `Too many voices / 音色数量超限: max ${spec.maxVoices} (current ${voiceIds.length})`,
    );
  }
}

function appendVoiceContents(contents, voiceIds) {
  for (let i = 0; i < voiceIds.length; i++) {
    contents.push({
      type: 'voice',
      voice_id: String(voiceIds[i]),
      id: String(i + 1),
    });
  }
}

function rejectRemovedVideoFlags(args) {
  if (args.mode) {
    throw new Error(
      'Removed --mode / --mode 已移除。请改用 --resolution 720p|1080p|4k（对应原 std/pro/4k）',
    );
  }
  if (args.sound) {
    throw new Error(
      'Removed --sound / --sound 已移除。请改用 --audio native|off|original',
    );
  }
  if (args.shot_type || args.multi_prompt) {
    throw new Error(
      'Removed --shot_type / --multi_prompt / 已移除。多镜头请用 --prompt「镜头 n, m, words;」并设置 --multi_shot true|false',
    );
  }
  if (args.keep_original_sound) {
    throw new Error(
      'Removed --keep_original_sound / 已移除。请改用 --audio original',
    );
  }
  if (args.negative_prompt) {
    throw new Error(
      'Unsupported --negative_prompt / 当前视频接口不支持 --negative_prompt',
    );
  }
  if (args.hdr !== undefined) {
    throw new Error(
      'Unsupported --hdr / 请改用 --dynamic_range sdr|hdr（kling-4.0，hdr 仅支持 1080p 或 4k）',
    );
  }
}

function printHelp() {
  console.log(`Kling AI video generation

Usage:
  node kling.mjs video --prompt <text> [options]               # Text-to-video
  node kling.mjs video --image <path|url> [--prompt ...]       # Image-to-video
  node kling.mjs video --prompt "..." [--image ...] [--element_ids ...]  # Omni
  node kling.mjs video --multi_shot true --prompt "镜头 1, 2, ...; 镜头 2, 3, ...;"
  node kling.mjs video --task_id <id> [--download]              # Query/download

Submit (common):
  --prompt          Video description (Omni / 4.0: @image_1 @element_1 @video_1; voice @1)
  --duration        Seconds; model-dependent (4.0: 3-30, 4.0-flash: 3-20, 3.0/turbo: 3-15, o1: 3-10, 2.6/2.5: 5|10).
                    kling-4.0: omitted duration is not sent. The server reads the prompt,
                    then base_video on Omni, otherwise its official 10.
                    kling-4.0-flash: omitted duration is not sent. Do not pass 10 to fill a default
                    (T2V / I2V: explicit, else prompt, else 10; Omni with base_video: explicit, else prompt, else that video, else 10).
                    Other models: omitted duration is sent as 5.
  --model           kling-4.0 / kling-4.0-flash / kling-3.0 / kling-3.0-turbo / kling-2.6 / kling-2.5-turbo / kling-3.0-omni / kling-o1
                    kling-4.0 and kling-4.0-flash are each one name for T2V / I2V / Omni; the route follows the flags below
  --resolution      720p / 1080p / 4k (4k: kling-4.0, kling-3.0, kling-3.0-omni; kling-4.0-flash: 720p only).
                    Official default: 1080p for kling-4.0, else 720p
  --dynamic_range   sdr / hdr (kling-4.0 only; official default: sdr, omitted is not sent).
                    hdr requires 1080p (or omitted resolution on kling-4.0) or 4k; rejected with 720p
  --aspect_ratio    16:9 / 9:16 / 1:1. kling-4.0 adds 4:3 / 3:4 / 21:9 (T2V / Omni) and adaptive (Omni).
                    kling-4.0-flash adds 4:3 / 3:4 / 21:9 (T2V / Omni) and adaptive (Omni).
                    Image-to-video has no aspect_ratio, so --image plus this flag routes to Omni
                    (including a first frame or kling-4.0 keyframes) and the value is submitted as given.
                    A first frame, or kling-4.0 frame-only keyframes, without this flag stays image-to-video.
                    Omni submits an explicit value even with a first frame or base video.
                    Omitted on Omni with no first frame and not a base edit: 16:9
                    (kling-4.0 / kling-4.0-flash: not sent, official adaptive).
  --audio           native / off / original (model-dependent; official default: off).
                    kling-4.0 / kling-4.0-flash Omni: original (keep input video sound) or native (new audio). T2V / I2V: not accepted.
                    original requires --video (reference video, not a video subject) and rejects --voice_ids.
                    kling-3.0-omni / kling-o1 feature video: off only; their base video cannot be native.
  --output_dir      Output dir (default: ./output)
  --no-wait         Submit only, do not wait
  --wait            Wait for completion (default)

Image-to-video / Omni:
  --image           Image path or URL (comma-separated for Omni refer images)
  --image_types     Optional type list aligned with --image: first_frame / middle_frame / last_frame / refer_image / empty
                    middle_frame: kling-4.0 only. Do not combine last_frame with --image_tail
                    kling-4.0: frame-only types (no refer_image) stay on image-to-video (max 10 images)
                    unless --aspect_ratio is set; image-to-video has no aspect_ratio, so that case goes Omni
                    kling-4.0-flash: only first_frame stays image-to-video; last_frame or --image_tail routes to Omni (no middle_frame)
  --image_tail      Last-frame image (maps to contents type last_frame). Do not combine with --image_types last_frame
  --element_ids     Subject IDs, comma-separated. I2V kling-3.0: contents type=element (max 3). Else Omni.
  --voice_ids       Voice IDs, comma-separated. contents type=voice.
                    kling-4.0: Omni only, max 3, voice_id plus id 1, prompt @1. --audio original is rejected.
                    T2V / I2V reject this flag. kling-4.0-flash rejects this flag.
                    kling-2.6: image-to-video only, max 2, id 1, prompt @1.
                    Omitted --audio becomes native and resolution 1080p. --audio off is rejected.
                    Not on 3.0 / 3.0-omni / turbo / 2.5 / o1. Does not change route by itself.
  --video           Omni reference video URL(s), comma-separated. Public http(s) only.
                    kling-4.0 / kling-4.0-flash: up to 5, prompt @video_1 @video_2 …. kling-3.0-omni / kling-o1: 1.
                    At most one base_video. kling-4.0 / kling-4.0-flash, no video-character subjects: max 5 videos.
                    With video-character subjects, those subjects plus videos total at most 5
                    (subject type is not known from an element id; the server checks that cap).
  --video_refer_type feature / base, or a list aligned with --video.
                    One URL and omitted type → base. Several URLs: list each type, or one feature for all.

Multi-shot:
  --multi_shot      true / false. Request field only on kling-3.0 / kling-3.0-omni (official default true; not kling-4.0 / kling-4.0-flash).
                    kling-3.0 / kling-3.0-omni base video edit: if omitted, CLI sends false (server default true would fail).
                    Turbo: write 镜头 n, m, words; in --prompt; do not pass --multi_shot.

Query/download:
  --task_id         Task ID
  --download        Download if task succeeded

Watermark:
  --watermark       Generate with watermark (options.watermark_info.enabled=true)

Env:
  credentials file  ~/.config/kling/.credentials (api_key)
  KLING_API_KEY     Session-only Bearer (optional override)
  KLING_MEDIA_ROOTS Comma-separated extra dirs for local media / --output_dir (default: cwd only)
  KLING_ALLOW_ABSOLUTE_PATHS=1  Allow any local path (e.g. WSL downloads outside project)`);
}

function isFrameOnlyList(imageTypes) {
  return imageTypes.length > 0 && imageTypes.every((t) => FRAME_TYPES.includes(t));
}

/**
 * Models in OMNI_MODELS only always go Omni. kling-4.0 and kling-4.0-flash are listed in both tables
 * and pick T2V / I2V / Omni from the flags, same as when --model is omitted.
 */
function chooseRoute(args, imageTypes = []) {
  const m = normalizeModelKey(args.model);
  const basicSpec = m ? BASIC_MODELS[m] : undefined;
  const sharedName = Boolean(basicSpec && OMNI_MODELS[m]);
  if (m && OMNI_MODELS[m] && !basicSpec) return 'omni';
  if (m && !basicSpec && !OMNI_MODELS[m]) {
    throw new Error(
      `Unknown --model / 未知模型: ${m}\n`
      + 'Allowed / 允许: kling-4.0, kling-4.0-flash, kling-3.0, kling-3.0-turbo, kling-2.6, kling-2.5-turbo, kling-3.0-omni, kling-o1',
    );
  }
    if (args.video) return 'omni';
  if (args.image) {
    const images = args.image.split(',').map(s => s.trim()).filter(Boolean);
    if (m === 'kling-4.0-flash' && (args.image_tail || imageTypes.includes('last_frame'))) return 'omni';
    if (args.aspect_ratio) return 'omni';
    if (images.length > 1 && basicSpec?.middleFrame && isFrameOnlyList(imageTypes) && !args.element_ids) {
      return 'i2v';
    }
    if (images.length > 1) return 'omni';
    if (args.element_ids) {
      const model = m || 'kling-4.0';
      if (BASIC_MODELS[model]?.i2vElements) return 'i2v';
      if (OMNI_MODELS[model]) return 'omni';
      if (BASIC_MODELS[model]) {
        throw new Error(
          `Unsupported --element_ids for ${model} / 官网图生视频仅 kling-3.0 的 contents 含 element；turbo/2.6/2.5 请去掉 --element_ids，或改用 kling-3.0 / kling-3.0-omni / kling-o1 / kling-4.0 / kling-4.0-flash`,
        );
      }
    }
    if (sharedName && imageTypes[0] === 'refer_image') return 'omni';
    return 'i2v';
  }
  if (args.element_ids) return 'omni';
  return 't2v';
}

function resolveModel(route, args) {
  const m = normalizeModelKey(args.model);
  if (route === 'omni') {
    if (!m) return 'kling-4.0';
    if (!OMNI_MODELS[m]) {
      throw new Error(
        `Invalid --model for Omni / Omni 不支持该模型: ${m}\n`
        + 'Allowed / 允许: kling-3.0-omni, kling-o1, kling-4.0, kling-4.0-flash',
      );
    }
    return m;
  }
  if (!m) return 'kling-4.0';
  if (!BASIC_MODELS[m]) {
    throw new Error(
      `Invalid --model for text/image-to-video / 文生/图生不支持该模型: ${m}\n`
      + 'Allowed / 允许: kling-3.0, kling-3.0-turbo, kling-2.6, kling-2.5-turbo, kling-4.0, kling-4.0-flash',
    );
  }
  return m;
}

function modelSpec(route, model) {
  return route === 'omni' ? OMNI_MODELS[model] : BASIC_MODELS[model];
}

function apiPathOf(route, model) {
  const spec = modelSpec(route, model);
  if (route === 'omni') return spec.path;
  return route === 't2v' ? spec.t2v : spec.i2v;
}

function buildSettings({ spec, duration, resolution, dynamicRange, aspectRatio, audio, multiShot, includeAspect }) {
  const settings = {};
  if (duration != null) settings.duration = duration;
  if (resolution) settings.resolution = resolution;
  if (dynamicRange && spec.dynamicRanges) settings.dynamic_range = dynamicRange;
  if (includeAspect && aspectRatio) settings.aspect_ratio = aspectRatio;
  if (audio && spec.audio) settings.audio = audio;
  if (spec.multiShot && multiShot !== undefined) settings.multi_shot = multiShot;
  return settings;
}

function buildOptions(args) {
  if (!args.watermark) return undefined;
  return { watermark_info: { enabled: true } };
}

function validateSettings(route, model, spec, args, ctx, voiceIds = [], videoState = { hasBase: false }) {
  const duration = parseDuration(
    args.duration,
    model === 'kling-4.0' || model === 'kling-4.0-flash' ? null : (spec.defaultDuration ?? 5),
  );
  if (duration != null && !spec.durations.includes(duration)) {
    throw new Error(
      `Invalid --duration for ${model} / 该模型时长须为: ${spec.durations.join(', ')}`,
    );
  }

  let resolution = parseResolution(args.resolution);
  if (resolution && !spec.resolutions.includes(resolution)) {
    throw new Error(
      `Invalid --resolution for ${model} / 该模型清晰度须为: ${spec.resolutions.join(', ')}`,
    );
  }

  const dynamicRange = parseDynamicRange(args.dynamic_range);
  if (dynamicRange) {
    if (!spec.dynamicRanges) {
      throw new Error(
        `Unsupported --dynamic_range for ${model} / 动态范围仅视频 kling-4.0 支持（sdr / hdr）`,
      );
    }
    if (!spec.dynamicRanges.includes(dynamicRange)) {
      throw new Error(
        `Invalid --dynamic_range for ${model} / 该模型 dynamic_range 须为: ${spec.dynamicRanges.join(', ')}`,
      );
    }
    if (dynamicRange === 'hdr' && (resolution || '1080p') === '720p') {
      throw new Error(
        'Invalid --dynamic_range hdr with 720p / HDR 仅支持 1080p 和 4k，不支持 720p',
      );
    }
  }

  let audio = parseAudio(args.audio);
  if (voiceIds.length && spec.audio?.includes('native')) {
    if (audio && audio !== 'native') {
      throw new Error(
        'Invalid --audio with --voice_ids / 指定音色时 audio 须为 native（不要用 off / original）',
      );
    }
    if (!audio && model !== 'kling-4.0' && model !== 'kling-4.0-flash') audio = 'native';
  }
  if (audio) {
    if (!spec.audio) {
      throw new Error(`Unsupported --audio for ${model} / 该模型接口无 audio 字段`);
    }
    if (!spec.audio.includes(audio)) {
      throw new Error(
        `Invalid --audio for ${model} / 该模型 audio 须为: ${spec.audio.join(', ')}`,
      );
    }
  }
  if (spec.audioRequires1080p && audio === 'native' && !resolution && voiceIds.length) {
    resolution = '1080p';
  }

  let multiShot = parseBoolFlag(args.multi_shot, '--multi_shot');
  if (multiShot !== undefined && !spec.multiShot) {
    throw new Error(
      `Unsupported --multi_shot for ${model} / 该模型请求体无 settings.multi_shot。`
      + (model === 'kling-3.0-turbo'
        ? ' 官网 Turbo 多镜头写在 --prompt：镜头 n, m, words;'
        : ''),
    );
  }
  if (spec.multiShot && multiShot === undefined && isBaseVideoEdit(videoState)) {
    multiShot = false;
  }

  if (spec.audioRequires1080p && audio === 'native' && (resolution || '720p') !== '1080p') {
    throw new Error(
      'Invalid --audio native / 官网：生成有声视频时仅支持 1080p。请设置 --resolution 1080p',
    );
  }

  if (ctx.hasLastFrame && !spec.lastFrame) {
    throw new Error(`Unsupported last_frame for ${model} / 该模型不支持尾帧`);
  }
  if (ctx.hasLastFrame && spec.lastFrameRequires1080p && (resolution || '720p') !== '1080p') {
    throw new Error('Invalid last_frame / 官网：该模型尾帧仅支持 1080p');
  }
  if (ctx.hasLastFrame && spec.lastFrameRequires1080pSilent) {
    if ((resolution || '720p') !== '1080p') {
      throw new Error('Invalid last_frame / 官网：kling-2.6 尾帧仅支持 1080p 且无声');
    }
    if (audio && audio !== 'off') {
      throw new Error('Invalid last_frame / 官网：kling-2.6 尾帧仅支持无声视频（--audio off）');
    }
  }

  if (model === 'kling-o1' && ctx.hasFirstFrame && !ctx.hasReferImage && !args.video && duration != null) {
    if (duration !== 5 && duration !== 10) {
      throw new Error(
        'Invalid --duration for kling-o1 first_frame / 官网：仅首帧且无 refer_image/参考视频时时长仅 5 或 10 秒',
      );
    }
  }

  return { duration, resolution, dynamicRange, audio, multiShot };
}

function parseVideoList(rawVideo, rawTypes) {
  if (!rawVideo || !String(rawVideo).trim()) {
    if (rawTypes) {
      throw new Error(
        'Invalid --video_refer_type without --video / 仅在传入 --video 时才能设置 --video_refer_type。',
      );
    }
    return { items: [], hasBase: false, hasFeature: false };
  }

  const urls = String(rawVideo).split(',').map((s) => s.trim());
  if (urls.some((url) => !url)) {
    throw new Error('Invalid --video / --video 列表中存在空值；请移除空项。');
  }
  const normalized = urls.map((url) => readOmniVideoRefUrl(url));

  let types;
  if (!rawTypes) {
    if (normalized.length > 1) {
      throw new Error(
        'Invalid --video_refer_type / 多段 --video 时须逐段指定 feature 或 base，也可只写一个 feature 表示全部为特征参考。最多 1 段 base_video',
      );
    }
    types = ['base'];
  } else {
    let parts = String(rawTypes).split(',').map((s) => s.trim().toLowerCase());
    if (parts.length === 1 && normalized.length > 1) {
      if (parts[0] !== 'feature') {
        throw new Error(
          'Invalid --video_refer_type / 多段参考视频里最多 1 段 base_video，其余须为 feature',
        );
      }
      parts = Array(normalized.length).fill('feature');
    }
    if (parts.length !== normalized.length) {
      throw new Error(
        `Invalid --video_refer_type / 数量需与 --video 一致: expected ${normalized.length}, got ${parts.length}`,
      );
    }
    types = parts.map((part) => {
      if (part !== 'feature' && part !== 'base') {
        throw new Error(
          `Invalid --video_refer_type / 无效 refer_type: ${part}. Allowed / 允许: feature, base`,
        );
      }
      return part;
    });
  }

  const baseCount = types.filter((type) => type === 'base').length;
  if (baseCount > 1) {
    throw new Error('Too many base videos / 待编辑视频 base_video 最多 1 段');
  }
  return {
    items: normalized.map((url, index) => ({ url, referType: types[index] })),
    hasBase: baseCount === 1,
    hasFeature: types.includes('feature'),
  };
}

function assertOmniVideoCount(model, spec, videoState) {
  const maxVideos = spec.maxVideos ?? 1;
  if (videoState.items.length > maxVideos) {
    throw new Error(
      `Too many reference videos for ${model} / 参考视频数量超限: max ${maxVideos} (current ${videoState.items.length})`,
    );
  }
}

function validateOmniImageListRules(args, imageInputs, imageTypes, hasTailArg, model, spec, videoState) {
  const maxImages = args.video ? spec.maxImagesWithVideo : spec.maxImages;
  const totalImages = imageInputs.length + (hasTailArg ? 1 : 0);
  if (totalImages > maxImages) {
    throw new Error(
      `Too many images for omni-video / Omni 图片数量超限: max ${maxImages} (current ${totalImages})`,
    );
  }

  const hasFirstFrame = imageTypes.includes('first_frame');
  const hasLastFrame = imageTypes.includes('last_frame') || hasTailArg;
  const hasReferImage = imageTypes.some((t) => (t || 'refer_image') === 'refer_image');

  if (hasLastFrame && !hasFirstFrame && model !== 'kling-4.0' && model !== 'kling-4.0-flash') {
    throw new Error(
      'Invalid image list: last_frame needs first_frame / 不支持仅尾帧，配置 last_frame 时必须同时有 first_frame。',
    );
  }

  if (model === 'kling-o1' && hasLastFrame && totalImages > 2) {
    throw new Error(
      'Invalid image list for kling-o1 / kling-o1 在图片数超过 2 时不支持 last_frame。',
    );
  }

  const hasFrame = hasFirstFrame || hasLastFrame;
  if (hasFrame && videoState.hasBase && (model === 'kling-3.0-omni' || model === 'kling-o1')) {
    throw new Error(
      'Invalid combo: frame images with video edit / 首帧或尾帧不能与视频编辑（--video_refer_type base）同时使用。',
    );
  }
  return { totalImages, hasFirstFrame, hasLastFrame, hasReferImage };
}

function validateOmniElementListRules(args, elementIds, imageState, model, spec, voiceIds = [], videoState = { items: [] }) {
  const hasFirstAndLast = imageState.hasFirstFrame && imageState.hasLastFrame;

  if (elementIds.length) {
    if (spec.maxElements && elementIds.length > spec.maxElements) {
      throw new Error(
        `Too many subjects for ${model} / 主体数量超限: max ${spec.maxElements} (current ${elementIds.length})`,
      );
    }

    if (spec.frameMaxElements
      && (imageState.hasFirstFrame || imageState.hasLastFrame)
      && elementIds.length > spec.frameMaxElements) {
      throw new Error(
        `Too many subjects with frame generation / 首帧或尾帧生视频时主体最多 ${spec.frameMaxElements} 个: current ${elementIds.length}`,
      );
    }

    if (hasFirstAndLast && model === 'kling-o1') {
      throw new Error(
        'Invalid element_list for kling-o1 / kling-o1 在首尾帧生视频场景不支持主体。',
      );
    }
  }

  if (model === 'kling-4.0' || model === 'kling-4.0-flash') {
    const total = imageState.totalImages + videoState.items.length + elementIds.length + voiceIds.length;
    if (total > spec.maxRefs) {
      const what = model === 'kling-4.0'
        ? '图片、参考视频、主体与音色总数超限'
        : '图片、参考视频与主体总数超限';
      throw new Error(
        `Too many refs for ${model} / ${what}: max ${spec.maxRefs} (current ${total})`,
      );
    }
    return;
  }

  if (!elementIds.length && !voiceIds.length) return;

  const totalRefs = imageState.totalImages + elementIds.length + voiceIds.length;
  const maxRefs = args.video ? spec.maxRefsWithVideo : spec.maxRefs;
  if (totalRefs > maxRefs) {
    throw new Error(
      `Too many refs for omni-video / Omni 参考图、主体与音色总数超限: max ${maxRefs} (current ${totalRefs})`,
    );
  }
}

function validateOmniAudioVideoRules(model, spec, audio, args, multiShot, imageState, videoState) {
  if (audio === 'original' && !videoState.items.length) {
    throw new Error(
      'Invalid --audio original without --video / original 为保留输入视频原声，须同时提供 --video（视频主体不算）',
    );
  }
  if (!videoState.items.length) return;

  const clipAudioLocked = model !== 'kling-4.0' && model !== 'kling-4.0-flash';
  if (videoState.hasFeature) {
    if (clipAudioLocked && audio && audio !== 'off') {
      throw new Error(
        'Invalid --audio with feature video / 官网：特征参考视频时 audio 只能为 off',
      );
    }
    if (multiShot === false) {
      throw new Error(
        'Invalid --multi_shot false with feature video / 官网：特征参考视频生成多镜头时 multi_shot 只能为 true',
      );
    }
    if (model === 'kling-o1' && imageState.hasLastFrame) {
      throw new Error(
        'Invalid last_frame with feature video / 官网：kling-o1 特征参考视频仅支持首帧，不支持尾帧',
      );
    }
  }
  if (videoState.hasBase) {
    if (clipAudioLocked && audio === 'native') {
      throw new Error(
        'Invalid --audio native with base video / 官网：待编辑视频 audio 不能为 native',
      );
    }
    if (multiShot === true) {
      throw new Error(
        'Invalid --multi_shot with base video / 官网：待编辑视频不支持多镜头',
      );
    }
    if ((model === 'kling-3.0-omni' || model === 'kling-o1') && (imageState.hasFirstFrame || imageState.hasLastFrame)) {
      throw new Error(
        'Invalid frames with base video / 官网：待编辑视频不支持定义首帧或尾帧',
      );
    }
  }
  if (!spec.audio?.includes('original') && audio === 'original') {
    throw new Error(`Invalid --audio original for this model / 该模型不支持 original`);
  }
}

async function queryExistingTask(taskId, token, outputDir, download) {
  const data = await queryTask(API_TASKS, taskId, token);
  const status = taskStatusOf(data) || 'unknown';
  console.log(`Task ID / 任务 ID: ${taskId}`);
  console.log(`Status / 状态: ${status}`);
  const msg = taskMessageOf(data);
  if (msg) console.log(`Message / 消息: ${msg}`);
  const url = resultUrlOf(data);
  if (url) {
    console.log(`Video URL / 视频链接: ${url}`);
    const wm = Array.isArray(data?.outputs)
      ? data.outputs.find((item) => item?.type === 'video' && item?.watermark_url)?.watermark_url
      : data?.task_result?.videos?.[0]?.watermark_url;
    if (wm) console.log(`Watermark URL / 水印视频: ${wm}`);
    if (download && isTaskSucceeded(status)) {
      const { mkdir } = await import('node:fs/promises');
      const { join } = await import('node:path');
      await mkdir(outputDir, { recursive: true });
      await downloadFile(url, join(outputDir, `${taskId}.mp4`));
    }
  }
}

export async function main() {
  const args = parseArgs(process.argv);
  if (args.help) { printHelp(); return; }
  validateModelAliasInput(args.model);
  rejectRemovedVideoFlags(args);

  const token = await getTokenOrExit();
  const outputDir = resolveAllowedOutputDir(args.output_dir || './output');

  if (args.task_id && !args.prompt && !args.image && args.multi_shot === undefined) {
    try {
      await queryExistingTask(args.task_id, token, outputDir, args.download);
    } catch (e) {
      console.error(`Error / 错误: ${e.message}`);
      process.exit(1);
    }
    return;
  }

  const imageInputs = parseImageInputs(args.image);
  const imageTypes = parseImageTypes(args.image_types, imageInputs.length);
  if (args.image_tail && imageTypes.includes('last_frame')) {
    throw new Error(
      'Invalid combo: --image_tail with --image_types last_frame / 尾帧只用 --image_tail 或 --image_types last_frame，不要同时传',
    );
  }
  if (args.image_tail && imageInputs.length > 0 && !imageTypes[0]) {
    imageTypes[0] = 'first_frame';
  }
  const elementIds = parseElementIds(args.element_ids);
  const voiceIds = parseVoiceIds(args.voice_ids);
  const videoState = parseVideoList(args.video, args.video_refer_type);
  const hasImage = imageInputs.length > 0;
  if (!args.prompt && !hasImage && args.multi_shot === undefined) {
    console.error('Error / 错误: --prompt, --image, or --multi_shot required');
    console.error('Use --help / 使用 --help 查看帮助');
    process.exit(1);
  }

  if (args.image_tail && !hasImage) {
    console.error('Error / 错误: --image_tail requires --image (first frame) / 首尾帧需要首帧 --image');
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

  try {
    const route = chooseRoute(args, imageTypes);
    const model = resolveModel(route, args);
    const spec = modelSpec(route, model);
    const apiPath = apiPathOf(route, model);
    const queryHint = `node kling.mjs video --task_id`;

    if (route === 'omni') assertOmniVideoCount(model, spec, videoState);
    if (imageTypes.includes('middle_frame') && !spec.middleFrame) {
      throw new Error(
        `Unsupported middle_frame for ${model} / 中间帧仅 kling-4.0 支持，请加 --model kling-4.0`,
      );
    }
    const totalImageCount = imageInputs.length + (args.image_tail ? 1 : 0);
    if (route === 'i2v' && spec.maxImages && totalImageCount > spec.maxImages) {
      throw new Error(
        `Too many images for image-to-video / 图生视频图片数量超限: max ${spec.maxImages} (current ${totalImageCount})`,
      );
    }

    let imageState = {
      totalImages: imageInputs.length + (args.image_tail ? 1 : 0),
      hasFirstFrame: imageTypes.includes('first_frame') || (route === 'i2v' && hasImage),
      hasLastFrame: imageTypes.includes('last_frame') || Boolean(args.image_tail),
      hasReferImage: imageTypes.some((t) => t === 'refer_image'),
    };
    if (route === 'omni' && (imageInputs.length > 0 || args.image_tail)) {
      imageState = validateOmniImageListRules(args, imageInputs, imageTypes, Boolean(args.image_tail), model, spec, videoState);
    }
    if (route === 'omni') validateOmniElementListRules(args, elementIds, imageState, model, spec, voiceIds, videoState);
    validateVoices(route, model, spec, voiceIds);

    const { duration, resolution, dynamicRange, audio, multiShot } = validateSettings(route, model, spec, args, imageState, voiceIds, videoState);
    if (route === 'omni') validateOmniAudioVideoRules(model, spec, audio, args, multiShot, imageState, videoState);

    const prompt = String(args.prompt || '').trim();
    if (route === 't2v' && !prompt) {
      throw new Error('text-to-video requires --prompt / 文生视频须提供 --prompt');
    }
    if (route === 'omni' && !prompt) {
      throw new Error('Omni requires non-empty --prompt / Omni 须提供非空 --prompt');
    }

    const includeAspect = route === 't2v'
      || (route === 'omni' && shouldSendOmniAspectRatio(args, imageState, videoState));
    const aspectRatio = args.aspect_ratio || (includeAspect ? (spec.defaultAspectRatio ?? '16:9') : '');
    const settings = buildSettings({
      spec,
      duration,
      resolution,
      dynamicRange,
      aspectRatio,
      audio,
      multiShot,
      includeAspect,
    });
    const options = buildOptions(args);

    let payload;
    if (route === 't2v') {
      payload = { prompt, settings };
      if (voiceIds.length) {
        const contents = [];
        appendVoiceContents(contents, voiceIds);
        payload.contents = contents;
      }
    } else if (route === 'i2v') {
      const contents = [];
      if (prompt) contents.push({ type: 'prompt', text: prompt });
      if (spec.middleFrame) {
        for (let i = 0; i < imageInputs.length; i++) {
          contents.push({
            type: imageTypes[i] || 'first_frame',
            url: await readMediaAsValue(imageInputs[i]),
            id: `image_${i + 1}`,
          });
        }
        if (args.image_tail) {
          contents.push({
            type: 'last_frame',
            url: await readMediaAsValue(args.image_tail),
            id: `image_${imageInputs.length + 1}`,
          });
        }
      } else {
        contents.push({ type: 'first_frame', url: await readMediaAsValue(imageInputs[0]) });
        if (args.image_tail) {
          contents.push({ type: 'last_frame', url: await readMediaAsValue(args.image_tail) });
        }
      }
      if (elementIds.length) {
        if (!spec.i2vElements) {
          throw new Error(
            `Unsupported --element_ids for ${model} / 官网图生视频仅 kling-3.0 的 contents 含 element`,
          );
        }
        if (elementIds.length > 3) {
          throw new Error(
            `Too many subjects for image-to-video / 官网：图生视频最多 3 个主体: current ${elementIds.length}`,
          );
        }
        for (let i = 0; i < elementIds.length; i++) {
          contents.push({
            type: 'element',
            element_id: String(elementIds[i]),
            id: `element_${i + 1}`,
          });
        }
      }
      appendVoiceContents(contents, voiceIds);
      payload = { contents, settings };
    } else {
      const contents = [];
      if (prompt) contents.push({ type: 'prompt', text: prompt });
      for (let i = 0; i < imageInputs.length; i++) {
        const type = imageTypes[i] || 'refer_image';
        contents.push({
          type,
          url: await readMediaAsValue(imageInputs[i]),
          id: `image_${i + 1}`,
        });
      }
      if (args.image_tail) {
        contents.push({
          type: 'last_frame',
          url: await readMediaAsValue(args.image_tail),
          id: `image_${imageInputs.length + 1}`,
        });
      }
      for (let i = 0; i < elementIds.length; i++) {
        contents.push({
          type: 'element',
          element_id: String(elementIds[i]),
          id: `element_${i + 1}`,
        });
      }
      for (let i = 0; i < videoState.items.length; i++) {
        const item = videoState.items[i];
        contents.push({
          type: item.referType === 'feature' ? 'feature_video' : 'base_video',
          url: item.url,
          id: `video_${i + 1}`,
        });
      }
      appendVoiceContents(contents, voiceIds);
      payload = { contents, settings };
    }
    if (options) payload.options = options;

    const result = await submitTask(apiPath, payload, token);
    console.log(`\nTask ID / 任务 ID: ${result.taskId}`);
    console.log(`Query / 查询: ${queryHint} ${result.taskId} [--download]`);
    if (args.wait !== false) {
      console.log();
      const outPath = await pollAndDownload(API_TASKS, result.taskId, outputDir, { token });
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
