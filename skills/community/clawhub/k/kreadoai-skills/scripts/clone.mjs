#!/usr/bin/env node
/**
 * KreadoAI — 即时形象克隆：上传视频、查询结果
 */
import { kreadoPost } from './shared/client.mjs';
import { parseArgs, getTokenOrExit, pollTask } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_UPLOAD_CLONE = '/apis/open/video/v3/uploadCloneVideo';
const API_GET_CLONE_STATUS = '/apis/open/video/v3/getUploadCloneVideoStatus';

function printHelp() {
  console.log(`KreadoAI clone — 即时形象克隆

用法：
  node kreado.mjs clone [选项]

操作：
  --upload <video_url>   上传视频进行形象克隆
  --query <jobId>        查询克隆视频上传结果
  --wait                 轮询等待直到完成（配合 --upload 使用）

--upload 参数：
  --video_url <url>      视频文件 URL（mp4/mov，5秒-10分钟，<300MB）

--query 参数：
  --job_id <id>          上传时返回的任务 ID

示例：
  node kreado.mjs clone --upload --video_url "https://..."
  node kreado.mjs clone --upload --video_url "https://..." --wait
  node kreado.mjs clone --query --job_id 1863777383505321985`);
}

async function uploadClone(args, token) {
  const videoUrl = args.video_url || (typeof args.upload === 'string' ? args.upload : '');
  if (!videoUrl) {
    console.error('错误：--video_url 为必填项');
    process.exit(1);
  }
  const data = await kreadoPost(API_UPLOAD_CLONE, { videoUrl }, token);
  console.error('✓ 克隆视频上传已提交');
  console.log(JSON.stringify(data, null, 2));

  if (args.wait && data.jobId) {
    console.error('\n轮询结果...');
    const result = await pollTask(
      () => kreadoPost(API_GET_CLONE_STATUS, { jobId: String(data.jobId) }, token),
      { interval: 5000 },
    );
    console.error('✓ 克隆完成');
    console.log(JSON.stringify(result, null, 2));
  }
}

async function queryClone(args, token) {
  const jobId = args.job_id || (typeof args.query === 'string' ? args.query : '');
  if (!jobId) {
    console.error('错误：--job_id 为必填项');
    process.exit(1);
  }
  const data = await kreadoPost(API_GET_CLONE_STATUS, { jobId: String(jobId) }, token);
  console.log(JSON.stringify(data, null, 2));
}

export async function main() {
  const args = parseArgs(process.argv, ['upload', 'query', 'wait']);

  if (args.help) {
    printHelp();
    return;
  }

  const token = getTokenOrExit();

  if (args.upload) {
    await uploadClone(args, token);
  } else if (args.query) {
    await queryClone(args, token);
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
