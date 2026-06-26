#!/usr/bin/env node
const fsp = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');

const MEDIA_EXTENSIONS = new Set([
  '.mp4', '.mov', '.m4v', '.mkv', '.avi', '.wmv',
  '.mp3', '.wav', '.aac', '.m4a', '.flac',
  '.jpg', '.jpeg', '.png', '.webp', '.bmp'
]);

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config || process.env.SKILL_CONFIG || 'config.json');
  const config = await loadConfig(configPath);

  validateConfig(config, [
    'api_base_url',
    'api_key',
    'project_type',
    'aspect_ratio',
    'material_path',
    'template_id',
    'subtitle_mode',
    'music_policy',
    'pace_policy',
    'output_mode',
    'jianying_draft_path',
    'draft_version',
    'export_mode'
  ]);

  const materials = await scanMaterials(path.resolve(config.material_path));
  if (materials.length === 0) {
    throw new Error(`No supported media files found in ${config.material_path}`);
  }

  const api = new ApiClient(config.api_base_url, config.api_key, config.request_timeout_ms);
  const task = await createTask(api, config, materials, 'jianying-auto-editor');
  const taskId = task.id;

  await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/material-index`, {
    materials,
    summary: buildMaterialSummary(materials)
  });

  const planBundle = await fetchPlanBundle(api, taskId, config, materials);
  const execution = await buildJianyingDraft({ config, materials, taskId, planBundle });

  await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/execute-report`, execution.report);
  console.log(JSON.stringify({
    ok: true,
    taskId,
    outputDir: execution.outputDir,
    generatedFiles: execution.report.generatedFiles,
    segmentCount: execution.report.summary.segmentCount
  }, null, 2));
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (current === '--config') {
      args.config = argv[index + 1];
      index += 1;
      continue;
    }
    if (current === '--help' || current === '-h') {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(
    'Usage: node scripts/index.js --config <path-to-config.json>\n\n' +
    'Reads local media, requests a cloud editing plan, and writes Jianying draft output.'
  );
}

async function loadConfig(configPath) {
  try {
    const raw = await fsp.readFile(configPath, 'utf8');
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Failed to load config at ${configPath}: ${error.message}`);
  }
}

function validateConfig(config, requiredFields) {
  const missing = requiredFields.filter((field) => {
    const value = config[field];
    return value === undefined || value === null || value === '';
  });
  if (missing.length > 0) {
    throw new Error(`Missing required config fields: ${missing.join(', ')}`);
  }
  if (!['overwrite', 'task-subdir'].includes(config.export_mode)) {
    throw new Error('export_mode must be either overwrite or task-subdir');
  }
}

async function scanMaterials(rootDir) {
  const rootStats = await fsp.stat(rootDir).catch(() => null);
  if (!rootStats || !rootStats.isDirectory()) {
    throw new Error(`material_path does not exist or is not a directory: ${rootDir}`);
  }

  const results = [];

  async function walk(currentDir) {
    const entries = await fsp.readdir(currentDir, { withFileTypes: true });
    entries.sort((left, right) => left.name.localeCompare(right.name));
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }
      const extension = path.extname(entry.name).toLowerCase();
      if (!MEDIA_EXTENSIONS.has(extension)) {
        continue;
      }
      const stats = await fsp.stat(fullPath);
      results.push({
        id: crypto.createHash('sha1').update(fullPath).digest('hex').slice(0, 12),
        name: entry.name,
        extension,
        kind: classifyMedia(extension),
        absolutePath: fullPath,
        relativePath: path.relative(rootDir, fullPath).replace(/\\/g, '/'),
        sizeBytes: stats.size,
        modifiedAt: stats.mtime.toISOString()
      });
    }
  }

  await walk(rootDir);
  return results;
}

function classifyMedia(extension) {
  if (['.mp4', '.mov', '.m4v', '.mkv', '.avi', '.wmv'].includes(extension)) {
    return 'video';
  }
  if (['.mp3', '.wav', '.aac', '.m4a', '.flac'].includes(extension)) {
    return 'audio';
  }
  return 'image';
}

function buildMaterialSummary(materials) {
  const summary = { total: materials.length, video: 0, audio: 0, image: 0 };
  for (const material of materials) {
    summary[material.kind] += 1;
  }
  return summary;
}

class ApiClient {
  constructor(baseUrl, apiKey, timeoutMs = 15000) {
    this.baseUrl = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
    this.apiKey = apiKey;
    this.timeoutMs = timeoutMs;
  }

  async get(endpoint) {
    return this.request('GET', endpoint);
  }

  async post(endpoint, body) {
    return this.request('POST', endpoint, body);
  }

  async request(method, endpoint, body) {
    const url = new URL(endpoint.replace(/^\//, ''), this.baseUrl);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const response = await fetch(url, {
        method,
        headers: {
          'content-type': 'application/json',
          'authorization': `Bearer ${this.apiKey}`,
          'user-agent': 'jianying-auto-editor/0.1.0'
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal
      });
      const text = await response.text();
      const parsed = text ? JSON.parse(text) : {};
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${parsed.message || text}`);
      }
      return parsed;
    } finally {
      clearTimeout(timer);
    }
  }
}

async function createTask(api, config, materials, executor) {
  const response = await api.post('/v1/tasks/create', {
    executor,
    taskName: config.task_name || `${executor}-${Date.now()}`,
    projectType: config.project_type,
    aspectRatio: config.aspect_ratio,
    templateId: config.template_id,
    outputMode: config.output_mode,
    webhookUrl: config.webhook_url || null,
    extraMetadata: config.extra_metadata || {},
    materialSummary: buildMaterialSummary(materials)
  });

  const task = response.task || response.data?.task || response.data || response;
  if (!task.id) {
    throw new Error('Cloud task creation response did not include task.id');
  }
  return task;
}

async function fetchPlanBundle(api, taskId, config, materials) {
  let response = await api.post(`/v1/tasks/${encodeURIComponent(taskId)}/plan`, {
    projectType: config.project_type,
    aspectRatio: config.aspect_ratio,
    templateId: config.template_id,
    subtitleMode: config.subtitle_mode,
    musicPolicy: config.music_policy,
    pacePolicy: config.pace_policy,
    outputMode: config.output_mode,
    materials
  });

  const status = extractStatus(response);
  if (['queued', 'pending', 'processing'].includes(status)) {
    response = await pollUntilReady(
      api,
      taskId,
      config.task_timeout_ms || 60000,
      config.poll_interval_ms || 1500
    );
  }
  return response;
}

function extractStatus(payload) {
  return payload.status || payload.data?.status || payload.task?.status || 'ready';
}

async function pollUntilReady(api, taskId, timeoutMs, intervalMs) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const statusPayload = await api.get(`/v1/tasks/${encodeURIComponent(taskId)}/status`);
    const state = extractStatus(statusPayload);
    if (!['queued', 'pending', 'processing'].includes(state)) {
      return statusPayload.plan
        ? statusPayload
        : { ...statusPayload, plan: statusPayload.plan || statusPayload.data?.plan };
    }
    await sleep(intervalMs);
  }
  throw new Error(`Timed out waiting for task ${taskId} to become ready`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function buildJianyingDraft({ config, materials, taskId, planBundle }) {
  const outputDir = resolveOutputDir(config.jianying_draft_path, config.export_mode, taskId);
  await fsp.mkdir(outputDir, { recursive: true });

  const cloudPlan = planBundle.plan || planBundle.data?.plan || planBundle.data || planBundle;
  const segments = normalizeSegments(cloudPlan, materials);
  const draftMeta = {
    taskId,
    executor: 'jianying-auto-editor',
    generatedAt: new Date().toISOString(),
    draftVersion: config.draft_version,
    projectType: config.project_type,
    aspectRatio: config.aspect_ratio,
    templateId: config.template_id,
    subtitleMode: config.subtitle_mode,
    musicPolicy: config.music_policy,
    pacePolicy: config.pace_policy,
    outputMode: config.output_mode,
    materialSummary: buildMaterialSummary(materials)
  };
  const draftContent = {
    timeline: {
      name: config.task_name || `jianying-${taskId}`,
      ratio: config.aspect_ratio,
      subtitleMode: config.subtitle_mode,
      musicPolicy: config.music_policy,
      pacePolicy: config.pace_policy
    },
    materials,
    segments,
    planSummary: {
      timelineName: cloudPlan?.timelineName || config.task_name || `jianying-${taskId}`,
      segmentCount: segments.length,
      templateId: config.template_id
    }
  };

  const draftMetaPath = path.join(outputDir, 'draft-meta.json');
  const draftContentPath = path.join(outputDir, 'draft-content.json');
  const reportPath = path.join(outputDir, 'execution-report.json');

  await writeJson(draftMetaPath, draftMeta);
  await writeJson(draftContentPath, draftContent);

  const report = {
    taskId,
    executor: 'jianying-auto-editor',
    status: 'succeeded',
    generatedAt: new Date().toISOString(),
    outputDir,
    generatedFiles: [draftMetaPath, draftContentPath, reportPath],
    summary: {
      materialCount: materials.length,
      segmentCount: segments.length
    }
  };
  await writeJson(reportPath, report);

  return { outputDir, report };
}

function resolveOutputDir(baseDir, exportMode, taskId) {
  const rootDir = path.resolve(baseDir);
  if (exportMode === 'overwrite') {
    return rootDir;
  }
  return path.join(rootDir, taskId);
}

function normalizeSegments(cloudPlan, materials) {
  const planSegments = cloudPlan?.segments || cloudPlan?.timeline?.segments || [];
  if (Array.isArray(planSegments) && planSegments.length > 0) {
    return planSegments.map((segment, index) => ({
      id: segment.id || `segment-${index + 1}`,
      materialId: segment.materialId || materials[index % materials.length]?.id,
      relativePath: segment.relativePath || materials[index % materials.length]?.relativePath,
      clipInMs: segment.clipInMs ?? 0,
      clipOutMs: segment.clipOutMs ?? 5000,
      transition: segment.transition || 'cut',
      caption: segment.caption || '',
      notes: segment.notes || null
    }));
  }

  return materials.map((material, index) => ({
    id: `segment-${index + 1}`,
    materialId: material.id,
    relativePath: material.relativePath,
    clipInMs: 0,
    clipOutMs: 5000,
    transition: index === 0 ? 'none' : 'cut',
    caption: '',
    notes: 'Fallback segment generated locally because the cloud plan did not provide explicit segments.'
  }));
}

async function writeJson(targetPath, payload) {
  await fsp.writeFile(targetPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

main().catch(async (error) => {
  const payload = {
    ok: false,
    error: error.message,
    stack: error.stack,
    generatedAt: new Date().toISOString()
  };
  try {
    const configArg = parseArgs(process.argv.slice(2)).config;
    if (configArg) {
      const config = await loadConfig(path.resolve(configArg));
      if (config.jianying_draft_path) {
        const fallbackDir = path.resolve(config.jianying_draft_path);
        await fsp.mkdir(fallbackDir, { recursive: true });
        await writeJson(path.join(fallbackDir, 'execution-report.json'), payload);
      }
    }
  } catch (_) {
    // Best effort only.
  }
  console.error(payload.error);
  process.exit(1);
});
