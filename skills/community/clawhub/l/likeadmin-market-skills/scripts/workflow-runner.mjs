#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadConfiguration, poll, request, upload } from './api-client.mjs';

function firstString(value, paths) {
  for (const candidate of paths) {
    const result = candidate.split('.').reduce((current, key) => current?.[key], value);
    if (typeof result === 'string' && result.trim()) return result;
  }
  return null;
}

export function extractTaskId(payload) {
  return firstString(payload, ['task_id', 'data.task_id', 'data.id', 'data.taskId']);
}

export function extractMediaUrl(payload) {
  return firstString(payload, [
    'data.url',
    'data.audio_url',
    'data.video_url',
    'data.image_url',
    'data.output',
    'data.result.url',
    'data.result.output',
    'result.url',
    'result.output',
  ]);
}

export function extractResourceId(payload) {
  return firstString(payload, ['data.voice_id', 'data.model_id', 'data.reference_id', 'data.id', 'id']);
}

export function localMediaPath(value, workingDirectory) {
  if (typeof value !== 'string' || !value.trim()) throw new Error('A media path or public URL is required.');
  if (value.startsWith('blob:')) throw new Error('blob: URLs are not reachable by 算力超市. Provide a local file or public URL.');
  if (value.startsWith('file://')) return pathFromFileUrl(value);
  if (/^https?:\/\//i.test(value)) return null;
  return path.resolve(workingDirectory, value);
}

function pathFromFileUrl(value) {
  try {
    return new URL(value).pathname;
  } catch {
    throw new Error(`Invalid file URL: ${value}`);
  }
}

function optionalObject(value, field) {
  if (value === undefined) return {};
  if (!value || Array.isArray(value) || typeof value !== 'object') throw new Error(`${field} must be a JSON object.`);
  return value;
}

function requireString(input, field) {
  const value = input[field];
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${field} is required.`);
  return value.trim();
}

function saveState(state, file) {
  if (!file) return;
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  fs.writeFileSync(file, `${JSON.stringify(state, null, 2)}\n`, { mode: 0o600 });
  fs.chmodSync(file, 0o600);
}

async function resolveMedia(value, workingDirectory, configuration, localUploadConfirmed) {
  const local = localMediaPath(value, workingDirectory);
  if (!local) return value;
  const response = await upload(local, configuration, localUploadConfirmed);
  return response.data.url;
}

async function ensureApps(appCodes, configuration) {
  for (const appCode of new Set(appCodes)) await request(`apps/${encodeURIComponent(appCode)}`, {}, configuration);
}

async function submitApp(appCode, apiCode, body, configuration) {
  return request(`apps/${encodeURIComponent(appCode)}/${encodeURIComponent(apiCode)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }, configuration);
}

async function completeIfTask(payload, configuration, options) {
  const taskId = extractTaskId(payload);
  if (!taskId) return { submission: payload, completion: null, media_url: extractMediaUrl(payload) };
  const completion = await poll(taskId, options.poll_interval_seconds || 3, options.poll_timeout_seconds || 600, configuration);
  return { submission: payload, completion, media_url: extractMediaUrl(completion) };
}

function appendNode(state, name, result, stateFile) {
  const entry = {
    name,
    task_id: extractTaskId(result.submission || result) || null,
    resource_id: extractResourceId(result.submission || result) || null,
    media_url: result.media_url || extractMediaUrl(result) || null,
    completed: Boolean(result.completion),
  };
  state.nodes.push(entry);
  saveState(state, stateFile);
  return entry;
}

async function createVoice(input, directory, configuration, state, stateFile) {
  const audioUrl = await resolveMedia(requireString(input, 'reference_audio'), directory, configuration, input.confirm_local_upload === true);
  const payload = await submitApp('voice_tts', 'clone_voice', {
    title: requireString(input, 'voice_title'),
    audio_url: audioUrl,
    visibility: input.visibility || 'private',
    ...optionalObject(input.clone_options, 'clone_options'),
  }, configuration);
  const voiceId = extractResourceId(payload);
  if (!voiceId) throw new Error('Voice clone response did not include a voice/reference ID. Preserve the response and inspect the live contract.');
  appendNode(state, 'clone_voice', { submission: payload, media_url: null }, stateFile);
  return voiceId;
}

async function synthesizeSpeech(input, referenceId, configuration, state, stateFile) {
  const text = requireString(input, 'text');
  const apiCode = input.tts_api || (text.length > 500 ? 'tts_async' : 'tts');
  if (!['tts', 'tts_async', 'tts_live'].includes(apiCode)) throw new Error('tts_api must be tts, tts_async, or tts_live.');
  const payload = await submitApp('voice_tts', apiCode, {
    text,
    ...(referenceId ? { reference_id: referenceId } : {}),
    ...optionalObject(input.tts_options, 'tts_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  if (!completed.media_url) throw new Error('TTS completed without an audio URL. Inspect the returned task result before continuing.');
  appendNode(state, `voice_tts/${apiCode}`, completed, stateFile);
  return completed.media_url;
}

async function createLipsync(input, audioUrl, directory, configuration, state, stateFile) {
  const videoUrl = await resolveMedia(requireString(input, 'source_video'), directory, configuration, input.confirm_local_upload === true);
  const payload = await submitApp('lipsync', 'submit', {
    audio_url: audioUrl,
    video_url: videoUrl,
    ...optionalObject(input.lipsync_options, 'lipsync_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  appendNode(state, 'lipsync/submit', completed, stateFile);
  return completed;
}

async function createImageAvatar(input, directory, configuration, state, stateFile) {
  const portraitUrl = await resolveMedia(requireString(input, 'portrait_image'), directory, configuration, input.confirm_local_upload === true);
  const audioUrl = await resolveMedia(requireString(input, 'driving_audio'), directory, configuration, input.confirm_local_upload === true);
  const payload = await submitApp('image_human', 'submit', {
    file_url: portraitUrl,
    ref_file_url: audioUrl,
    ...optionalObject(input.avatar_options, 'avatar_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  if (!completed.media_url) throw new Error('Image-avatar task completed without a video URL.');
  appendNode(state, 'image_human/submit', completed, stateFile);
  return completed.media_url;
}

async function createRealmanClip(input, videoUrl, directory, configuration, state, stateFile) {
  const styleId = requireString(input, 'style_id');
  const payload = await submitApp('smart_clip', 'realman_broadcast', {
    styleId,
    videoUrl,
    ...optionalObject(input.smart_clip_options, 'smart_clip_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  appendNode(state, 'smart_clip/realman_broadcast', completed, stateFile);
  return completed;
}

async function createMaterialClip(input, directory, configuration, state, stateFile) {
  const audioUrl = await resolveMedia(requireString(input, 'audio'), directory, configuration, input.confirm_local_upload === true);
  const materials = await Promise.all((input.materials || []).map(async (item) => ({
    ...item,
    fileUrl: await resolveMedia(requireString(item, 'file'), directory, configuration, input.confirm_local_upload === true),
  })));
  if (!materials.length) throw new Error('materials must contain at least one image or video.');
  const payload = await submitApp('smart_clip', 'broadcast_mixcut', {
    styleId: requireString(input, 'style_id'),
    audioUrl,
    materials,
    ...optionalObject(input.smart_clip_options, 'smart_clip_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  appendNode(state, 'smart_clip/broadcast_mixcut', completed, stateFile);
  return completed;
}

async function createNewsClip(input, directory, configuration, state, stateFile) {
  const materials = await Promise.all((input.materials || []).map(async (item) => ({
    ...item,
    fileUrl: await resolveMedia(requireString(item, 'file'), directory, configuration, input.confirm_local_upload === true),
  })));
  if (!materials.length) throw new Error('materials must contain at least one image or video.');
  const payload = await submitApp('smart_clip', 'news_mixcut', {
    styleId: requireString(input, 'style_id'),
    title: requireString(input, 'title'),
    materials,
    ...optionalObject(input.smart_clip_options, 'smart_clip_options'),
  }, configuration);
  const completed = await completeIfTask(payload, configuration, input);
  appendNode(state, 'smart_clip/news_mixcut', completed, stateFile);
  return completed;
}

export async function runWorkflow(recipe, input, options = {}) {
  const configuration = options.configuration || loadConfiguration();
  const directory = options.workingDirectory || process.cwd();
  const stateFile = options.stateFile || null;
  const state = { recipe, started_at: new Date().toISOString(), nodes: [] };
  const recipes = {
    'clone-voice': ['voice_tts'],
    tts: ['voice_tts'],
    lipsync: ['lipsync'],
    'clone-voice-lipsync': ['voice_tts', 'lipsync'],
    'image-avatar': ['image_human'],
    'realman-smart-clip': ['smart_clip'],
    'avatar-smart-clip': ['image_human', 'smart_clip'],
    'material-smart-clip': ['smart_clip'],
    'news-smart-clip': ['smart_clip'],
  };
  if (!recipes[recipe]) throw new Error(`Unsupported recipe: ${recipe}`);
  await ensureApps(recipes[recipe], configuration);
  saveState(state, stateFile);

  let result;
  if (recipe === 'clone-voice') result = { voice_id: await createVoice(input, directory, configuration, state, stateFile) };
  if (recipe === 'tts') result = { audio_url: await synthesizeSpeech(input, input.reference_id || null, configuration, state, stateFile) };
  if (recipe === 'lipsync') {
    const audioUrl = await resolveMedia(requireString(input, 'audio'), directory, configuration, input.confirm_local_upload === true);
    result = await createLipsync(input, audioUrl, directory, configuration, state, stateFile);
  }
  if (recipe === 'clone-voice-lipsync') {
    const voiceId = await createVoice(input, directory, configuration, state, stateFile);
    const audioUrl = await synthesizeSpeech(input, voiceId, configuration, state, stateFile);
    result = { voice_id: voiceId, audio_url: audioUrl, ...(await createLipsync(input, audioUrl, directory, configuration, state, stateFile)) };
  }
  if (recipe === 'image-avatar') result = { video_url: await createImageAvatar(input, directory, configuration, state, stateFile) };
  if (recipe === 'realman-smart-clip') {
    const videoUrl = await resolveMedia(requireString(input, 'source_video'), directory, configuration, input.confirm_local_upload === true);
    result = await createRealmanClip(input, videoUrl, directory, configuration, state, stateFile);
  }
  if (recipe === 'avatar-smart-clip') {
    const videoUrl = await createImageAvatar(input, directory, configuration, state, stateFile);
    result = await createRealmanClip(input, videoUrl, directory, configuration, state, stateFile);
  }
  if (recipe === 'material-smart-clip') result = await createMaterialClip(input, directory, configuration, state, stateFile);
  if (recipe === 'news-smart-clip') result = await createNewsClip(input, directory, configuration, state, stateFile);
  state.completed_at = new Date().toISOString();
  state.result = result;
  saveState(state, stateFile);
  return { ...result, state };
}

function parseArguments(args) {
  const [recipe, inputFile, ...rest] = args;
  if (!recipe || !inputFile) throw new Error('Usage: workflow-runner.mjs <recipe> <input.json> [--state <state.json>]');
  let stateFile = null;
  if (rest.length) {
    if (rest.length !== 2 || rest[0] !== '--state') throw new Error('Usage: workflow-runner.mjs <recipe> <input.json> [--state <state.json>]');
    stateFile = path.resolve(rest[1]);
  }
  const absoluteInput = path.resolve(inputFile);
  const input = JSON.parse(fs.readFileSync(absoluteInput, 'utf8'));
  return { recipe, input, stateFile, workingDirectory: path.dirname(absoluteInput) };
}

async function main() {
  const args = parseArguments(process.argv.slice(2));
  const result = await runWorkflow(args.recipe, args.input, args);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  });
}
