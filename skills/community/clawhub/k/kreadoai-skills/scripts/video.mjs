#!/usr/bin/env node
/**
 * KreadoAI — 数字人视频生成：提交任务、查询结果、列表、详情、表情模板
 */
import { kreadoPost } from './shared/client.mjs';
import { parseArgs, getTokenOrExit, pollTask } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_SUBMIT_LIP = '/apis/open/video/v3/submitLipTask';
const API_SUBMIT_SYSTEM_LIP = '/apis/open/video/v3/submitSystemLipTask';
const API_GET_RESULT = '/apis/open/video/v3/getLipVideoResult';
const API_VIDEO_LIST = '/apis/open/video/v3/list';
const API_VIDEO_DETAIL = '/apis/open/video/v3/detail';
const API_EMO_LIST = '/apis/open/video/v3/emoList';

function printHelp() {
  console.log(`KreadoAI video — 数字人视频生成

用法：
  node kreado.mjs video [选项]

操作：
  --submit-lip           提交通用视频生成任务
  --submit-system        提交数字人视频生成任务
  --query <jobId>        查询视频任务结果
  --list                 视频列表（默认）
  --detail <taskId>      获取视频详情
  --emo-list             获取表情模板

--submit-lip 参数：
  --task_name <name>     任务名称（必填）
  --video_url <url>      视频文件 URL（必填）
  --audio_url <url>      音频文件 URL（必填）
  --audio_id <id>        音频 ID（用于系统声音）
  --wait                 轮询等待直到完成

--submit-system 参数：
  --task_name <name>     任务名称（必填）
  --video_ratio <1|2>    1=16:9, 2=9:16（必填）
  --digital_human_id <id> 数字人 ID（必填）
  --audio_url <url>      音频文件 URL（必填）
  --audio_id <id>        音频 ID（用于系统声音）
  --mask <0|1|2>         0=无遮罩, 1=圆形, 2=矩形
  --x <n>               位置 X 坐标
  --y <n>               位置 Y 坐标
  --resize <ratio>       头像缩放比例（默认：1.00）
  --template_id <id>     表情模板 ID（照片数字人）
  --bg_type <302|303>    背景：302=纯色, 303=自定义
  --bg_color <rgb>       背景颜色（如 "rgb(0,255,0)"）
  --bg_image <url>       背景图片 URL
  --wait                 轮询等待直到完成

--query 参数：
  --job_id <id>          任务 ID

--list 参数：
  --status <1-5>         按状态筛选
  --page <n>             页码（默认：1）
  --page_size <n>        每页数量（默认：10）

--detail 参数：
  --task_id <id>         视频任务 ID

--emo-list 参数：
  --page <n>             页码（默认：1）
  --page_size <n>        每页数量（默认：10）

示例：
  node kreado.mjs video --submit-lip --task_name "test" --video_url "https://..." --audio_url "https://..."
  node kreado.mjs video --submit-system --task_name "test" --video_ratio 2 --digital_human_id 9 --audio_url "https://..."
  node kreado.mjs video --query --job_id 1861664658419253250
  node kreado.mjs video --list --page 1 --page_size 5
  node kreado.mjs video --detail --task_id 122164
  node kreado.mjs video --emo-list`);
}

async function submitLipTask(args, token) {
  if (!args.task_name) { console.error('错误：--task_name 为必填项'); process.exit(1); }
  if (!args.video_url) { console.error('错误：--video_url 为必填项'); process.exit(1); }
  if (!args.audio_url) { console.error('错误：--audio_url 为必填项'); process.exit(1); }

  const body = {
    taskName: args.task_name,
    videoUrl: args.video_url,
    audioUrl: args.audio_url,
  };
  if (args.audio_id) body.audioId = parseInt(args.audio_id, 10);

  const data = await kreadoPost(API_SUBMIT_LIP, body, token);
  console.error('✓ 任务已提交');
  console.log(JSON.stringify(data, null, 2));

  if (args.wait && data.jobId) {
    console.error('\n轮询结果...');
    const result = await pollTask(
      () => kreadoPost(API_GET_RESULT, { jobId: data.jobId }, token),
      { interval: 10000, timeout: 900000 },
    );
    console.error('✓ 视频完成');
    console.log(JSON.stringify(result, null, 2));
  }
}

async function submitSystemLipTask(args, token) {
  if (!args.task_name) { console.error('错误：--task_name 为必填项'); process.exit(1); }
  if (!args.video_ratio) { console.error('错误：--video_ratio 为必填项'); process.exit(1); }
  if (!args.digital_human_id) { console.error('错误：--digital_human_id 为必填项'); process.exit(1); }
  if (!args.audio_url) { console.error('错误：--audio_url 为必填项'); process.exit(1); }

  const body = {
    taskName: args.task_name,
    videoRatio: parseInt(args.video_ratio, 10),
    digitalHuman: {
      digitalHumanId: parseInt(args.digital_human_id, 10),
    },
    audio: {
      audioUrl: args.audio_url,
    },
  };
  if (args.audio_id) body.audio.audioId = parseInt(args.audio_id, 10);
  if (args.mask) body.digitalHuman.mask = parseInt(args.mask, 10);
  if (args.x) body.digitalHuman.x = parseInt(args.x, 10);
  if (args.y) body.digitalHuman.y = parseInt(args.y, 10);
  if (args.resize) body.digitalHuman.resize = args.resize;
  if (args.template_id) body.digitalHuman.templateId = parseInt(args.template_id, 10);

  if (args.bg_type) {
    body.background = { type: parseInt(args.bg_type, 10) };
    if (args.bg_color) body.background.color = args.bg_color;
    if (args.bg_image) {
      body.background.backgroundElements = [{
        elementType: 330,
        fileUrl: args.bg_image,
      }];
    }
  }

  const data = await kreadoPost(API_SUBMIT_SYSTEM_LIP, body, token);
  console.error('✓ 任务已提交');
  console.log(JSON.stringify(data, null, 2));

  if (args.wait && data.jobId) {
    console.error('\n轮询结果...');
    const result = await pollTask(
      () => kreadoPost(API_GET_RESULT, { jobId: data.jobId }, token),
      { interval: 10000, timeout: 900000 },
    );
    console.error('✓ 视频完成');
    console.log(JSON.stringify(result, null, 2));
  }
}

async function queryResult(args, token) {
  const jobId = args.job_id || args.query;
  if (!jobId || jobId === true) {
    console.error('错误：--job_id 为必填项'); process.exit(1);
  }
  const data = await kreadoPost(API_GET_RESULT, { jobId }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function listVideos(args, token) {
  const body = {
    pageIndex: parseInt(args.page || '1', 10),
    pageSize: parseInt(args.page_size || '10', 10),
  };
  if (args.status) body.status = parseInt(args.status, 10);
  const data = await kreadoPost(API_VIDEO_LIST, body, token);
  console.log(JSON.stringify(data, null, 2));
}

async function getDetail(args, token) {
  const taskId = args.task_id || args.detail;
  if (!taskId || taskId === true) {
    console.error('错误：--task_id 为必填项'); process.exit(1);
  }
  const data = await kreadoPost(API_VIDEO_DETAIL, { taskId: parseInt(taskId, 10) }, token);
  console.log(JSON.stringify(data, null, 2));
}

async function getEmoList(args, token) {
  const body = {
    pageIndex: parseInt(args.page || '1', 10),
    pageSize: parseInt(args.page_size || '10', 10),
  };
  if (args.id) body.id = parseInt(args.id, 10);
  const data = await kreadoPost(API_EMO_LIST, body, token);
  console.log(JSON.stringify(data, null, 2));
}

export async function main() {
  const args = parseArgs(process.argv, ['submit-lip', 'submit-system', 'query', 'list', 'detail', 'emo-list', 'wait']);

  if (args.help) {
    printHelp();
    return;
  }

  const token = getTokenOrExit();

  if (args['submit-lip']) {
    await submitLipTask(args, token);
  } else if (args['submit-system']) {
    await submitSystemLipTask(args, token);
  } else if (args.query) {
    await queryResult(args, token);
  } else if (args.detail) {
    await getDetail(args, token);
  } else if (args['emo-list']) {
    await getEmoList(args, token);
  } else {
    await listVideos(args, token);
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  });
}
