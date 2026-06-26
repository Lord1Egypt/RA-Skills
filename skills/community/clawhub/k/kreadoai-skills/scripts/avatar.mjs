#!/usr/bin/env node
/**
 * KreadoAI — 数字人形象：列表、上传照片、查询上传结果
 */
import { kreadoPost } from './shared/client.mjs';
import { parseArgs, getTokenOrExit, pollTask } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_AVATAR_LIST = '/apis/open/avatar/v3/list';
const API_UPLOAD_AVATAR = '/apis/open/avatar/v3/uploadAvatar';
const API_GET_UPLOAD_RESULT = '/apis/open/avatar/v3/getUploadCustomAvatar';

function printHelp() {
  console.log(`KreadoAI avatar — 数字人形象管理

用法：
  node kreado.mjs avatar [选项]

操作：
  --list（默认）         列出数字人形象
  --upload <url>         上传自定义照片作为数字人
  --query <jobId>        查询照片上传结果
  --wait                 轮询等待直到上传完成（配合 --upload 使用）

--list 参数：
  --type <100|101>       100=照片, 101=视频（默认：100）
  --clone <0|1>          查询克隆列表：0=否, 1=是（默认：0）
  --page <n>             页码（默认：1）
  --page_size <n>        每页数量（默认：10）
  --gender <210|211>     210=男性, 211=女性
  --style <137|138|139>  137=写实, 138=精品, 139=臻品
  --area <id>            地区：141=欧美, 140=亚洲, 142=日韩, 143=东南亚, 145=印度, 144=中东, 146=非洲

--upload 参数：
  --file_url <url>       公开图片 URL（jpg/jpeg/png/webp，<=10MB，360-4000px）

--query 参数：
  --job_id <id>          上传时返回的任务 ID

示例：
  node kreado.mjs avatar --list
  node kreado.mjs avatar --list --type 101 --page 1 --page_size 5
  node kreado.mjs avatar --upload --file_url "https://example.com/photo.jpg"
  node kreado.mjs avatar --upload --file_url "https://..." --wait
  node kreado.mjs avatar --query --job_id 1862021310686838786`);
}

async function listAvatars(args, token) {
  const body = {
    cloneDigitalHuman: parseInt(args.clone || '0', 10),
    supportTypeId: parseInt(args.type || '100', 10),
    digitalHumanId: args.digital_human_id ? parseInt(args.digital_human_id, 10) : null,
    tagIds: args.gender ? [parseInt(args.gender, 10)] : null,
    areaTypeIds: args.area ? [parseInt(args.area, 10)] : null,
    pageIndex: parseInt(args.page || '1', 10),
    pageSize: parseInt(args.page_size || '10', 10),
  };
  if (args.style) {
    body.tagIds = [...(body.tagIds || []), parseInt(args.style, 10)];
  }
  const data = await kreadoPost(API_AVATAR_LIST, body, token);
  console.log(JSON.stringify(data, null, 2));
}

async function uploadAvatar(args, token) {
  const fileUrl = args.file_url || args.upload;
  if (!fileUrl || fileUrl === true) {
    console.error('错误：--file_url 为上传必填项');
    process.exit(1);
  }
  const data = await kreadoPost(API_UPLOAD_AVATAR, { fileUrl }, token);
  console.error('✓ 上传已提交');
  console.log(JSON.stringify(data, null, 2));

  if (args.wait && data.jobId) {
    console.error('\n轮询上传结果...');
    const result = await pollTask(
      () => kreadoPost(API_GET_UPLOAD_RESULT, { jobId: String(data.jobId) }, token),
      { interval: 3000 },
    );
    console.error('✓ 上传完成');
    console.log(JSON.stringify(result, null, 2));
  }
}

async function queryUpload(args, token) {
  const jobId = args.job_id || args.query;
  if (!jobId || jobId === true) {
    console.error('错误：--job_id 为必填项');
    process.exit(1);
  }
  const data = await kreadoPost(API_GET_UPLOAD_RESULT, { jobId: String(jobId) }, token);
  console.log(JSON.stringify(data, null, 2));
}

export async function main() {
  const args = parseArgs(process.argv, ['list', 'upload', 'query', 'wait']);

  if (args.help) {
    printHelp();
    return;
  }

  const token = getTokenOrExit();

  if (args.upload) {
    await uploadAvatar(args, token);
  } else if (args.query) {
    await queryUpload(args, token);
  } else {
    await listAvatars(args, token);
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  });
}
