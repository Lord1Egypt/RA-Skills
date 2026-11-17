#!/usr/bin/env node
/**
 * Kling AI voice management — create, query, list, delete custom voices
 * Node.js 18+, zero external deps
 *
 * Official: POST/GET /v1/general/custom-voices, GET presets-voices, POST delete-voices.
 * Model-independent (same API for 2.6 / 3.0 / O1 / 4.0). Create accepts a public
 * voice_url or an existing video_id — not a local file.
 */
import { submitTask, queryTask, pollTask } from './shared/task.mjs';
import { klingGet, klingPost } from './shared/client.mjs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs, getTokenOrExit } from './shared/args.mjs';

const API_PATH = '/v1/general/custom-voices';
const API_PATH_PRESETS = '/v1/general/presets-voices';
const API_PATH_DELETE = '/v1/general/delete-voices';

function isHttpUrl(value) {
  return /^https?:\/\//i.test(String(value || '').trim());
}

function printVoices(voices) {
  for (const voice of voices) {
    const id = voice.voice_id || voice.id || '';
    const name = voice.voice_name || voice.name || '';
    console.log(`  Voice ID / 音色 ID: ${id}`);
    if (name) console.log(`  Name / 名称: ${name}`);
    if (voice.trial_url || voice.url) console.log(`  Trial / 试听: ${voice.trial_url || voice.url}`);
    if (voice.owned_by) console.log(`  Owned by / 来源: ${voice.owned_by}`);
  }
}

function printHelp() {
  console.log(`Kling AI voice management (create/query/list/delete)

Usage:
  node kling.mjs voice --action create --name <text> (--voice_url <https> | --video_id <id>)
  node kling.mjs voice --action query --task_id <id>
  node kling.mjs voice --action list [--page_num 1] [--page_size 30]
  node kling.mjs voice --action list-presets [--page_num 1] [--page_size 30]
  node kling.mjs voice --action delete --voice_id <id>

Actions:
  --action create       Create custom voice (async; returns voice_id)
  --action query        Query creation task status
  --action list         List custom voices
  --action list-presets List official preset voices
  --action delete       Delete a custom voice (presets cannot be deleted)

Create options:
  --name              Voice name (required, ≤20 chars)
  --voice_url         Public http(s) URL of .mp3 / .wav / .mp4 / .mov (one speaker, 5–30 s)
  --video_id          Existing work ID (2.6 with sound on, avatar, or lip-sync only)
  --no-wait           Submit only, do not wait

  Provide exactly one of --voice_url or --video_id. Local files are not accepted
  (the API takes a fetchable URL, not base64).

Query:
  --task_id           Creation task ID

List:
  --page_num          Page 1-1000 (default: 1)
  --page_size         Page size 1-1000 (default: 30)

Delete:
  --voice_id          Custom voice ID to delete

Use the returned voice_id in video via --voice_ids (kling-4.0 Omni / kling-2.6 image-to-video).

Env:
  credentials file    ~/.config/kling/.credentials (api_key)
  KLING_API_KEY       Session-only Bearer (optional override)`);
}

async function actionCreate(args, token) {
  const name = String(args.name || '').trim();
  if (!name) { console.error('Error / 错误: --name required'); process.exit(1); }
  if ([...name].length > 20) {
    console.error('Error / 错误: --name 最多 20 个字符');
    process.exit(1);
  }

  const voiceUrl = String(args.voice_url || '').trim();
  const videoId = String(args.video_id || '').trim();
  if (voiceUrl && videoId) {
    console.error('Error / 错误: --voice_url 与 --video_id 只能传一个');
    process.exit(1);
  }
  if (!voiceUrl && !videoId) {
    console.error('Error / 错误: 须提供 --voice_url（公网 URL）或 --video_id');
    process.exit(1);
  }
  if (voiceUrl && !isHttpUrl(voiceUrl)) {
    console.error(
      'Error / 错误: --voice_url 须为公网 http(s) URL。官方接口不接受本地文件或 base64。',
    );
    process.exit(1);
  }

  const payload = { voice_name: name, callback_url: '' };
  if (voiceUrl) payload.voice_url = voiceUrl;
  if (videoId) payload.video_id = videoId;

  const result = await submitTask(API_PATH, payload, token);
  console.log(`\nTask ID / 任务 ID: ${result.taskId}`);

  if (args.wait !== false) {
    console.log();
    const data = await pollTask(API_PATH, result.taskId, { token });
    const voices = data?.task_result?.voices || [];
    if (voices.length > 0) {
      console.log('\n✓ Created / 已创建:');
      printVoices(voices);
    }
  }
}

async function actionQuery(args, token) {
  if (!args.task_id) { console.error('Error / 错误: --task_id required'); process.exit(1); }
  const data = await queryTask(API_PATH, args.task_id, token);
  console.log(`Task ID / 任务 ID: ${args.task_id}`);
  console.log(`Status / 状态: ${data?.task_status || 'unknown'}`);
  if (data?.task_status_msg) console.log(`Message / 消息: ${data.task_status_msg}`);
  printVoices(data?.task_result?.voices || []);
}

async function actionList(args, token, presets) {
  const path = presets ? API_PATH_PRESETS : API_PATH;
  const pageNum = args.page_num || '1';
  const pageSize = args.page_size || '30';
  const data = await klingGet(`${path}?pageNum=${pageNum}&pageSize=${pageSize}`, token);

  const items = Array.isArray(data) ? data : [data];
  const label = presets ? 'Preset / 官方音色' : 'Custom / 自定义音色';
  console.log(`${label} (page ${pageNum}):\n`);

  for (const item of items) {
    const voices = item?.task_result?.voices || [];
    if (voices.length === 0 && item?.task_id) {
      console.log(`  Task / 任务 ${item.task_id}: ${item.task_status || 'unknown'}`);
      continue;
    }
    for (const voice of voices) {
      const id = voice.voice_id || voice.id || '';
      const name = voice.voice_name || voice.name || '';
      console.log(`  [${id}] ${name}`);
    }
  }
}

async function actionDelete(args, token) {
  if (!args.voice_id) { console.error('Error / 错误: --voice_id required'); process.exit(1); }
  const data = await klingPost(API_PATH_DELETE, { voice_id: String(args.voice_id) }, token);
  console.log(`✓ Deleted / 已删除: ${args.voice_id}`);
  if (data?.task_status) console.log(`  Status / 状态: ${data.task_status}`);
}

export async function main() {
  const args = parseArgs(process.argv, ['no-wait']);
  if (args.help) { printHelp(); return; }

  const token = await getTokenOrExit();
  const action = args.action;

  if (!action) {
    console.error('Error / 错误: --action required (create / query / list / list-presets / delete)');
    process.exit(1);
  }

  try {
    switch (action) {
      case 'create':       await actionCreate(args, token); break;
      case 'query':         await actionQuery(args, token); break;
      case 'list':          await actionList(args, token, false); break;
      case 'list-presets':  await actionList(args, token, true); break;
      case 'delete':        await actionDelete(args, token); break;
      default:
        console.error(`Error / 错误: unknown action "${action}". Use: create / query / list / list-presets / delete`);
        process.exit(1);
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
