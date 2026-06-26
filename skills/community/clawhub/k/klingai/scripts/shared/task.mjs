/**
 * Kling AI task helpers (zero external deps)
 * Submit → poll status → download result
 */
import { writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { klingPost, klingGet, makeKlingHeaders } from './client.mjs';

/**
 * 提交任务
 * @param {string} apiPath  如 /v1/videos/image2video
 * @param {object} payload  请求体
 * @param {string} [token]
 * @returns {Promise<{taskId: string, status: string, data: object}>}
 */
export async function submitTask(apiPath, payload, token) {
  const data = await klingPost(apiPath, payload, token);
  const taskId = data?.task_id;
  if (!taskId) throw new Error('API did not return task_id / API 未返回 task_id');
  console.log(`Task submitted / 任务已提交: ${taskId}`);
  console.log(`Status / 状态: ${data.task_status || 'submitted'}`);
  return { taskId, status: data.task_status || 'submitted', data };
}

/**
 * 查询任务状态
 * @param {string} apiPath  如 /v1/videos/image2video
 * @param {string} taskId
 * @param {string} [token]
 * @returns {Promise<object>} task data
 */
export async function queryTask(apiPath, taskId, token) {
  return klingGet(`${apiPath}/${taskId}`, token);
}

/**
 * 轮询任务直到完成
 * @param {string} apiPath
 * @param {string} taskId
 * @param {object} [opts]
 * @param {number} [opts.interval=10000]  轮询间隔(ms)
 * @param {string} [opts.token]
 * @returns {Promise<object>} 成功的 task data
 */
export async function pollTask(apiPath, taskId, opts = {}) {
  const interval = opts.interval || 10000;
  const token = opts.token;
  console.log('Waiting for task... / 等待任务完成...');
  while (true) {
    const data = await queryTask(apiPath, taskId, token);
    const status = data?.task_status;
    console.log(`Status / 状态: ${status}`);
    if (status === 'succeed') return data;
    if (status === 'failed') {
      throw new Error(`Task failed / 任务失败: ${data?.task_status_msg || 'Unknown error'}`);
    }
    await new Promise(r => setTimeout(r, interval));
  }
}

/**
 * 下载文件到本地
 * @param {string} url     下载 URL
 * @param {string} outPath 输出文件路径
 */
export async function downloadFile(url, outPath) {
  console.log('Downloading... / 正在下载...');
  const res = await fetch(url, { headers: makeKlingHeaders(null, null) });
  if (!res.ok) throw new Error(`Download failed / 下载失败: HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  await mkdir(join(outPath, '..'), { recursive: true });
  await writeFile(outPath, buf);
  console.log(`Saved / 已保存: ${outPath}`);
}

/**
 * 轮询并下载结果
 * @param {string} apiPath
 * @param {string} taskId
 * @param {string} outputDir
 * @param {object} [opts]
 * @param {string} [opts.urlField='url']  output 中的 URL 字段名
 * @param {string} [opts.ext='.mp4']  文件扩展名
 * @param {number} [opts.interval]
 * @param {string} [opts.token]
 * @returns {Promise<string>} 输出文件路径
 */
export async function pollAndDownload(apiPath, taskId, outputDir, opts = {}) {
  const data = await pollTask(apiPath, taskId, opts);
  const urlField = opts.urlField || 'url';
  const ext = opts.ext || '.mp4';
  const output = data?.task_result || {};
  // 支持多种输出结构
  const url = output[urlField]
    || output?.videos?.[0]?.[urlField]
    || output?.images?.[0]?.url
    || (typeof output === 'string' ? output : null);
  if (!url) throw new Error(`Task succeeded but missing ${urlField} / 任务成功但未返回 ${urlField}`);
  await mkdir(outputDir, { recursive: true });
  const outPath = join(outputDir, `${taskId}${ext}`);
  await downloadFile(url, outPath);
  return outPath;
}
