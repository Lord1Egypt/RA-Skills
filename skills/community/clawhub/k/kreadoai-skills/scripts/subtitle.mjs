#!/usr/bin/env node
/**
 * KreadoAI — 视频字幕/水印去除：提交任务、查询结果
 */
import { kreadoPost } from './shared/client.mjs';
import { parseArgs, getTokenOrExit, pollTask } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_SUBMIT_TASK = '/apis/open/subtitle_removal/v3/submitTask';
const API_TASK_RESULT = '/apis/open/subtitle_removal/v3/taskResult';

function printHelp() {
  console.log(`KreadoAI subtitle — 视频字幕和水印去除

用法：
  node kreado.mjs subtitle [选项]

操作：
  --submit               提交字幕/水印去除任务
  --query <jobId>        查询任务结果

--submit 参数：
  --task_name <name>     任务名称（必填，<=100 字符）
  --src_file_url <url>   视频 URL（必填，mp4/mov，>5秒，<200MB）
  --watermark <json>     水印区域坐标（JSON 数组）
  --subtitle_area <json> 字幕区域坐标（JSON 数组）
  --wait                 轮询等待直到完成

  坐标格式：[{"lt_x":0,"lt_y":0,"rb_x":400,"rb_y":200}]

--query 参数：
  --job_id <id>          任务 ID

示例：
  node kreado.mjs subtitle --submit --task_name "去除字幕" --src_file_url "https://..."
  node kreado.mjs subtitle --submit --task_name "test" --src_file_url "https://..." --watermark '[{"lt_x":0,"lt_y":0,"rb_x":400,"rb_y":200}]' --wait
  node kreado.mjs subtitle --query --job_id 1861664658419253250`);
}

async function submitTask(args, token) {
  if (!args.task_name) { console.error('错误：--task_name 为必填项'); process.exit(1); }
  if (!args.src_file_url) { console.error('错误：--src_file_url 为必填项'); process.exit(1); }

  const body = {
    taskName: args.task_name,
    srcFileUrl: args.src_file_url,
  };

  if (args.watermark) {
    try {
      body.customRectAreaList = JSON.parse(args.watermark);
    } catch {
      console.error('错误：--watermark 必须是合法的 JSON 数组');
      process.exit(1);
    }
  }

  if (args.subtitle_area) {
    try {
      body.rectAreaList = JSON.parse(args.subtitle_area);
    } catch {
      console.error('错误：--subtitle_area 必须是合法的 JSON 数组');
      process.exit(1);
    }
  }

  const data = await kreadoPost(API_SUBMIT_TASK, body, token);
  console.error('✓ 任务已提交');
  console.log(JSON.stringify(data, null, 2));

  if (args.wait && data.jobId) {
    console.error('\n轮询结果...');
    const result = await pollTask(
      () => kreadoPost(API_TASK_RESULT, { jobId: data.jobId }, token),
      { interval: 10000, timeout: 900000 },
    );
    console.error('✓ 去除完成');
    console.log(JSON.stringify(result, null, 2));
  }
}

async function queryResult(args, token) {
  const jobId = args.job_id || (typeof args.query === 'string' ? args.query : '');
  if (!jobId) {
    console.error('错误：--job_id 为必填项'); process.exit(1);
  }
  const data = await kreadoPost(API_TASK_RESULT, { jobId: parseInt(jobId, 10) }, token);
  console.log(JSON.stringify(data, null, 2));
}

export async function main() {
  const args = parseArgs(process.argv, ['submit', 'query', 'wait']);

  if (args.help) {
    printHelp();
    return;
  }

  const token = getTokenOrExit();

  if (args.submit) {
    await submitTask(args, token);
  } else if (args.query) {
    await queryResult(args, token);
  } else {
    printHelp();
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  });
}
