#!/usr/bin/env node
/**
 * Kling AI subject management — create, query, list, delete custom subjects
 * Node.js 18+, zero external deps
 */
import { submitTask, queryTask, pollTask } from './shared/task.mjs';
import { klingGet, klingPost } from './shared/client.mjs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs, getTokenOrExit, readMediaAsValue } from './shared/args.mjs';

const API_PATH = '/v1/general/advanced-custom-elements';
const API_PATH_PRESETS = '/v1/general/advanced-presets-elements';
const API_PATH_DELETE = '/v1/general/delete-elements';

function getElementType(el) {
  return el?.reference_type || el?.element_type || el?.ref_type || 'unknown';
}

function printHelp() {
  console.log(`Kling AI subject management (create/query/list/delete)

Usage:
  node kling.mjs element --action create [create options]
  node kling.mjs element --action query --task_id <id>
  node kling.mjs element --action list [--page_num 1] [--page_size 30]
  node kling.mjs element --action list-presets [--page_num 1] [--page_size 30]
  node kling.mjs element --action delete --element_id <id>

Actions:
  --action create       Create custom subject
  --action query        Query creation task status
  --action list         List custom subjects
  --action list-presets List preset subjects
  --action delete       Delete subject

Create options:
  --name              Subject name (required, ≤20 chars)
  --description       Subject description (required, ≤100 chars)
  --ref_type          image_refer / video_refer (required)
  --frontal_image     Front reference image path or URL (required for image_refer)
  --refer_images      Other reference images, comma-separated (optional, 1-3)
  --video             Reference video path or URL (required for video_refer)
  --voice_id          Voice ID (optional, video-based only)
  --tags              Tag IDs, comma-separated (e.g. "o_102,o_108")
  --no-wait           Submit only, do not wait

Query:
  --task_id           Task ID

List:
  --page_num          Page 1-1000 (default: 1)
  --page_size         Page size 1-500 (default: 30)

Delete:
  --element_id        Subject ID to delete

Env:
  credentials file    ~/.config/kling/.credentials (access_key_id, secret_access_key)
  KLING_TOKEN         Session-only Bearer (optional override)`);
}

async function actionCreate(args, token) {
  if (!args.name) { console.error('Error / 错误: --name required'); process.exit(1); }
  if (!args.description) { console.error('Error / 错误: --description required'); process.exit(1); }
  if (!args.ref_type) { console.error('Error / 错误: --ref_type required (image_refer / video_refer)'); process.exit(1); }

  const payload = {
    element_name: args.name,
    element_description: args.description,
    reference_type: args.ref_type,
    callback_url: '',
  };

  if (args.ref_type === 'image_refer') {
    if (!args.frontal_image) {
      console.error('Error / 错误: image_refer requires --frontal_image'); process.exit(1);
    }
    const imageList = {
      frontal_image: await readMediaAsValue(args.frontal_image),
    };
    if (args.refer_images) {
      const imgs = args.refer_images.split(',');
      imageList.refer_images = [];
      for (const img of imgs) {
        imageList.refer_images.push({ image_url: await readMediaAsValue(img.trim()) });
      }
    }
    payload.element_image_list = imageList;
  } else if (args.ref_type === 'video_refer') {
    if (!args.video) {
      console.error('Error / 错误: video_refer requires --video'); process.exit(1);
    }
    payload.element_video_list = {
      refer_videos: [{ video_url: await readMediaAsValue(args.video) }],
    };
  } else {
    console.error('Error / 错误: --ref_type must be image_refer or video_refer');
    process.exit(1);
  }

  if (args.voice_id) {
    payload.element_voice_id = args.voice_id;
  }

  if (args.tags) {
    payload.tag_list = args.tags.split(',').map(id => ({ tag_id: id.trim() }));
  }

  const result = await submitTask(API_PATH, payload, token);
  console.log(`\nTask ID / 任务 ID: ${result.taskId}`);

  if (args.wait !== false) {
    console.log();
    const data = await pollTask(API_PATH, result.taskId, { token });
    const elements = data?.task_result?.elements || [];
    if (elements.length > 0) {
      console.log('\n✓ Created / 已创建:');
      for (const el of elements) {
        console.log(`  Element ID / 主体 ID: ${el.element_id}`);
        console.log(`  Name / 名称: ${el.element_name}`);
        console.log(`  Description / 描述: ${el.element_description}`);
        console.log(`  Type / 类型: ${getElementType(el)}`);
      }
    }
  }
}

async function actionQuery(args, token) {
  if (!args.task_id) { console.error('Error / 错误: --task_id required'); process.exit(1); }
  const data = await queryTask(API_PATH, args.task_id, token);
  console.log(`Task ID / 任务 ID: ${args.task_id}`);
  console.log(`Status / 状态: ${data?.task_status || 'unknown'}`);
  if (data?.task_status_msg) console.log(`Message / 消息: ${data.task_status_msg}`);
  const elements = data?.task_result?.elements || [];
  for (const el of elements) {
    console.log(`\nElement ID / 主体 ID: ${el.element_id}`);
    console.log(`  Name / 名称: ${el.element_name}`);
    console.log(`  Description / 描述: ${el.element_description}`);
    console.log(`  Type / 类型: ${getElementType(el)}`);
    if (el.element_voice_info?.voice_id) {
      console.log(`  Voice / 音色: ${el.element_voice_info.voice_name} (${el.element_voice_info.voice_id})`);
    }
  }
}

async function actionList(args, token, presets) {
  const path = presets ? API_PATH_PRESETS : API_PATH;
  const pageNum = args.page_num || '1';
  const pageSize = args.page_size || '30';
  const data = await klingGet(`${path}?pageNum=${pageNum}&pageSize=${pageSize}`, token);

  const items = Array.isArray(data) ? data : [data];
  const label = presets ? 'Preset / 预设主体' : 'Custom / 自定义主体';
  console.log(`${label} (page ${pageNum}):\n`);

  for (const item of items) {
    const elements = item?.task_result?.elements || [];
    if (elements.length === 0 && item?.task_id) {
      console.log(`  Task / 任务 ${item.task_id}: ${item.task_status || 'unknown'}`);
      continue;
    }
    for (const el of elements) {
      console.log(`  [${el.element_id}] ${el.element_name} — ${el.element_description} (${getElementType(el)})`);
    }
  }
}

async function actionDelete(args, token) {
  if (!args.element_id) { console.error('Error / 错误: --element_id required'); process.exit(1); }
  const data = await klingPost(API_PATH_DELETE, { element_id: String(args.element_id) }, token);
  console.log(`✓ Deleted / 已删除: ${args.element_id}`);
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
      case 'create':      await actionCreate(args, token); break;
      case 'query':        await actionQuery(args, token); break;
      case 'list':         await actionList(args, token, false); break;
      case 'list-presets': await actionList(args, token, true); break;
      case 'delete':       await actionDelete(args, token); break;
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
