#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import os from 'os';
import { execFileSync } from 'child_process';
import { resolveApiKey, createTask, pollResult, downloadFile } from './lib/client.mjs';
import { OCR_POLL_TIMEOUT_MS, IDPHOTO_POLL_TIMEOUT_MS, DEFAULT_POLL_TIMEOUT_MS } from './lib/constants.mjs';

const SKILL_REGISTRY = {
  'picwish-segmentation': {
    endpoint: '/api/tasks/visual/segmentation',
  },
  'picwish-face-cutout': {
    endpoint: '/api/tasks/visual/self-face-cutout',
  },
  'picwish-upscale': {
    endpoint: '/api/tasks/visual/scale',
  },
  'picwish-object-removal': {
    endpoint: '/api/tasks/visual/watermark',
  },
  'picwish-watermark-remove': {
    endpoint: '/api/tasks/visual/external/watermark-remove',
    imageFieldName: 'url',
    imageFileField: 'file',
    resultField: 'file',
  },
  'picwish-id-photo': {
    endpoint: '/api/tasks/visual/idphoto',
    pollTimeout: IDPHOTO_POLL_TIMEOUT_MS,
  },
  'picwish-colorize': {
    endpoint: '/api/tasks/visual/colorization',
  },
  'picwish-compress': {
    endpoint: '/api/tasks/visual/imgcompress',
  },
  'picwish-ocr': {
    endpoint: '/api/tasks/document/ocr',
    resultField: 'file',
    pollTimeout: OCR_POLL_TIMEOUT_MS,
  },
  'picwish-smart-crop': {
    endpoint: '/api/tasks/visual/correction',
  },
  'picwish-clothing-seg': {
    endpoint: '/api/tasks/visual/r-clothing-segmentation',
    resultField: 'class_masks',
  },
};

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--skill' && argv[i + 1]) {
      args.skill = argv[++i];
    } else if (argv[i] === '--input-json' && argv[i + 1]) {
      args.inputJson = argv[++i];
    } else if (argv[i] === '--output-dir' && argv[i + 1]) {
      args.outputDir = argv[++i];
    }
  }
  return args;
}

// Image formats accepted by PicWish APIs (union of all endpoint requirements).
// raw/rgb/jfif/lzw/bitmap are accepted by most visual endpoints per API docs.
const ALLOWED_IMAGE_EXTENSIONS = new Set([
  'jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff', 'tif',
  'bitmap', 'raw', 'rgb', 'jfif', 'lzw',
]);

// Home subdirectories that must never be read as image inputs.
const BLOCKED_HOME_SUBDIRS = [
  '.ssh', '.aws', '.gnupg', '.kube', '.azure', '.gcp',
  '.openclaw', '.picwish', '.config', '.npm', '.cursor',
  '.netrc', '.git', 'Library', 'AppData',
];

function validateImagePath(filePath) {
  const resolved = path.resolve(filePath);
  const ext = path.extname(resolved).slice(1).toLowerCase();

  if (!ALLOWED_IMAGE_EXTENSIONS.has(ext)) {
    throw new Error(
      `Rejected file path: ".${ext || '(no extension)'}" is not an allowed image format. ` +
      `Allowed: ${[...ALLOWED_IMAGE_EXTENSIONS].join(', ')}`
    );
  }

  const home = os.homedir();
  for (const dir of BLOCKED_HOME_SUBDIRS) {
    const blocked = path.join(home, dir);
    if (resolved === blocked || resolved.startsWith(blocked + path.sep)) {
      throw new Error(
        `Rejected file path: access to the "${dir}" directory is not permitted.`
      );
    }
  }

  return resolved;
}

function readFileAsBlob(filePath) {
  const buffer = fs.readFileSync(filePath);
  const ext = path.extname(filePath).slice(1) || 'png';
  const mimeMap = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', bmp: 'image/bmp', tiff: 'image/tiff', tif: 'image/tiff' };
  const mime = mimeMap[ext.toLowerCase()] || 'application/octet-stream';
  const blob = new Blob([buffer], { type: mime });
  const filename = path.basename(filePath);
  return { blob, filename };
}

function saveBase64ToTemp(base64Data, ext) {
  const tmpDir = os.tmpdir();
  const tmpPath = path.join(tmpDir, `openclaw_input_${Date.now()}.${ext || 'png'}`);
  fs.writeFileSync(tmpPath, Buffer.from(base64Data, 'base64'));
  return tmpPath;
}

function buildFormFields(input, skillConfig) {
  const fields = {};
  const urlField = skillConfig.imageFieldName || 'image_url';
  const fileField = skillConfig.imageFileField || 'image_file';

  if (input.image_url || input.url) {
    fields[urlField] = input.image_url || input.url;
  } else if (input.image_base64) {
    const ext = input.image_ext || 'png';
    const tmpPath = saveBase64ToTemp(input.image_base64, ext);
    let blob, filename;
    try {
      ({ blob, filename } = readFileAsBlob(tmpPath));
    } finally {
      try { fs.unlinkSync(tmpPath); } catch { /* ignore cleanup error */ }
    }
    fields[fileField] = { blob, filename };
  } else if (input.image_file || input.file) {
    const filePath = validateImagePath(input.image_file || input.file);
    const { blob, filename } = readFileAsBlob(filePath);
    fields[fileField] = { blob, filename };
  }

  if (input.mask_url) fields.mask_url = input.mask_url;
  if (input.mask_file) {
    const maskPath = validateImagePath(input.mask_file);
    const { blob, filename } = readFileAsBlob(maskPath);
    fields.mask_file = { blob, filename };
  }

  const passthrough = [
    'type', 'output_type', 'crop', 'scale_factor',
    'size', 'format', 'bg_color',
    'quality', 'kbyte', 'width', 'height',
    'language', 'password',
    'detail_mode', 'class_type',
  ];
  for (const key of passthrough) {
    if (input[key] !== undefined && input[key] !== null && input[key] !== '') {
      fields[key] = input[key];
    }
  }

  return fields;
}

function resolveOpenClawHome() {
  if (process.env.OPENCLAW_HOME) return process.env.OPENCLAW_HOME;
  if (process.platform === 'win32' && process.env.LOCALAPPDATA) {
    return path.join(process.env.LOCALAPPDATA, 'openclaw');
  }
  return path.join(os.homedir(), '.openclaw');
}

function resolveOutputDir(skillName) {
  const ocHome = resolveOpenClawHome();
  const resolvedOcHome = path.resolve(ocHome);
  const home = os.homedir();

  // Only execute oc-workspace.mjs when ocHome is inside the user's home directory.
  // This blocks attacks where OPENCLAW_HOME is set to an arbitrary system path.
  const isOcHomeUnderHome = resolvedOcHome === home ||
    resolvedOcHome.startsWith(home + path.sep);

  if (isOcHomeUnderHome) {
    const ocScript = path.join(resolvedOcHome, 'workspace', 'scripts', 'oc-workspace.mjs');
    if (fs.existsSync(ocScript)) {
      // Resolve symlinks to verify the real script path hasn't escaped ocHome.
      let realScript;
      try { realScript = fs.realpathSync(ocScript); } catch { realScript = null; }
      if (realScript && realScript.startsWith(resolvedOcHome + path.sep)) {
        try {
          const out = execFileSync('node', [realScript, 'route-output', '--skill', skillName, '--name', 'tmp', '--ext', 'tmp'], {
            encoding: 'utf8',
            timeout: 5000,
          }).trim();
          if (out) return path.dirname(out);
        } catch { /* fallback below */ }
      }
    }
  }

  const hasOpenclawYaml = fs.existsSync(path.join(process.cwd(), 'openclaw.yaml'));
  if (hasOpenclawYaml) return path.join(process.cwd(), 'output');

  const localVisual = path.join(process.cwd(), 'visual');
  if (fs.existsSync(localVisual)) return path.join(localVisual, 'output', skillName);

  return path.join(os.homedir(), 'Downloads');
}

function makeUniqueFilename(dir, base, ext) {
  let name = `${base}.${ext}`;
  let full = path.join(dir, name);
  if (!fs.existsSync(full)) return full;
  for (let i = 1; i < 1000; i++) {
    name = `${base}_${i}.${ext}`;
    full = path.join(dir, name);
    if (!fs.existsSync(full)) return full;
  }
  return path.join(dir, `${base}_${Date.now()}.${ext}`);
}

async function main() {
  const { skill, inputJson, outputDir: cliOutputDir } = parseArgs(process.argv);

  if (!skill || !SKILL_REGISTRY[skill]) {
    console.log(JSON.stringify({
      ok: false,
      error_type: 'INVALID_SKILL',
      user_hint: `Unknown skill: ${skill || '(not specified)'}`,
      next_action: `Available skills: ${Object.keys(SKILL_REGISTRY).join(', ')}`,
    }));
    process.exit(1);
  }

  if (!inputJson) {
    console.log(JSON.stringify({
      ok: false,
      error_type: 'MISSING_INPUT',
      user_hint: 'Missing --input-json argument.',
      next_action: 'Please provide input parameters in JSON format.',
    }));
    process.exit(1);
  }

  let input;
  try {
    input = JSON.parse(inputJson);
  } catch {
    console.log(JSON.stringify({
      ok: false,
      error_type: 'INVALID_JSON',
      user_hint: 'Invalid --input-json format.',
      next_action: 'Please provide a valid JSON string.',
    }));
    process.exit(1);
  }

  const apiKey = resolveApiKey();
  const config = SKILL_REGISTRY[skill];
  const fields = buildFormFields(input, config);

  const taskData = await createTask(config.endpoint, fields, apiKey);
  const taskId = taskData.task_id;

  const pollTimeout = config.pollTimeout
    ?? parseInt(process.env.PICWISH_POLL_TIMEOUT_MS, 10)
    || DEFAULT_POLL_TIMEOUT_MS;

  const result = await pollResult(config.endpoint, taskId, apiKey, { timeout: pollTimeout });

  const resultField = config.resultField || 'image';
  const resultValue = result[resultField];

  const outputDir = cliOutputDir || resolveOutputDir(skill);
  fs.mkdirSync(outputDir, { recursive: true });
  const date = new Date().toISOString().slice(0, 10);

  if (resultField === 'class_masks') {
    const savedPaths = {};

    for (const [part, maskUrl] of Object.entries(resultValue)) {
      if (!maskUrl || typeof maskUrl !== 'string') continue;
      const dest = makeUniqueFilename(outputDir, `${date}_clothing-seg_${part}`, 'png');
      await downloadFile(maskUrl, dest);
      savedPaths[part] = dest;
    }

    if (result.clothes_masks) {
      const zipDest = makeUniqueFilename(outputDir, `${date}_clothing-seg_clothes`, 'zip');
      await downloadFile(result.clothes_masks, zipDest);
      savedPaths.clothes_zip = zipDest;
    }

    console.log(JSON.stringify({
      ok: true,
      skill,
      task_id: taskId,
      class_masks: resultValue,
      saved_paths: savedPaths,
    }));
  } else {
    const skillShort = skill.replace('picwish-', '');
    const ext = guessExtension(resultValue, input.format);
    const destPath = makeUniqueFilename(outputDir, `${date}_${skillShort}`, ext);

    await downloadFile(resultValue, destPath);

    console.log(JSON.stringify({
      ok: true,
      skill,
      task_id: taskId,
      result_url: resultValue,
      saved_path: destPath,
    }));
  }
}

function guessExtension(url, format) {
  if (format) {
    const f = format.toLowerCase();
    if (f === 'jpeg' || f === 'jpg') return 'jpg';
    return f;
  }
  if (typeof url === 'string') {
    const m = url.match(/\.(png|jpg|jpeg|webp|bmp|tiff|pdf|docx|xlsx|pptx|txt|zip)(\?|$)/i);
    if (m) return m[1].toLowerCase();
  }
  return 'png';
}

main().catch(err => {
  console.log(JSON.stringify({
    ok: false,
    error_type: 'UNEXPECTED_ERROR',
    user_hint: 'An unexpected error occurred.',
    next_action: err.message,
  }));
  process.exit(1);
});
