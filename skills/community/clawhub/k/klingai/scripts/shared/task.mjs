/**
 * Kling AI task helpers (zero external deps)
 * Submit → poll status → download result
 */
import { writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { klingPost, klingGet, makeKlingHeaders } from './client.mjs';

const TASKS_QUERY_PATH = '/tasks';

function isTasksQueryPath(apiPath) {
  return apiPath === TASKS_QUERY_PATH || String(apiPath || '').startsWith(`${TASKS_QUERY_PATH}?`);
}

function asTaskList(data) {
  if (Array.isArray(data)) return data;
  if (data && typeof data === 'object') return [data];
  return [];
}

/** New video APIs: data.id / data.status=succeeded; /v1 image+element: data.task_id / task_status=succeed */
export function taskIdOf(data) {
  return data?.id || data?.task_id || '';
}

export function taskStatusOf(data) {
  return data?.status || data?.task_status || '';
}

export function taskMessageOf(data) {
  return data?.message || data?.task_status_msg || '';
}

export function isTaskSucceeded(status) {
  return status === 'succeeded' || status === 'succeed';
}

export function isTaskFailed(status) {
  return status === 'failed';
}

export function resultUrlOf(data, urlField = 'url') {
  const outputs = data?.outputs;
  if (Array.isArray(outputs)) {
    const video = outputs.find((item) => item?.type === 'video' && item?.[urlField]);
    if (video?.[urlField]) return video[urlField];
    const any = outputs.find((item) => item?.[urlField]);
    if (any?.[urlField]) return any[urlField];
  }
  const output = data?.task_result || {};
  return output[urlField]
    || output?.videos?.[0]?.[urlField]
    || output?.images?.[0]?.url
    || (typeof output === 'string' ? output : null);
}

/**
 * 提交任务
 * @param {string} apiPath  如 /text-to-video/kling-3.0 或 /v1/images/generations
 * @param {object} payload  请求体
 * @param {string} [token]
 * @returns {Promise<{taskId: string, status: string, data: object}>}
 */
export async function submitTask(apiPath, payload, token) {
  const data = await klingPost(apiPath, payload, token);
  const taskId = taskIdOf(data);
  if (!taskId) throw new Error('API did not return task id / API 未返回任务 ID');
  const status = taskStatusOf(data) || 'submitted';
  console.log(`Task submitted / 任务已提交: ${taskId}`);
  console.log(`Status / 状态: ${status}`);
  return { taskId, status, data };
}

/**
 * 查询任务状态
 * 新视频接口：GET /tasks?task_ids=
 * 图片/主体 /v1：GET {apiPath}/{taskId}
 * @param {string} apiPath
 * @param {string} taskId
 * @param {string} [token]
 * @returns {Promise<object>} task data
 */
export async function queryTask(apiPath, taskId, token) {
  if (isTasksQueryPath(apiPath)) {
    const data = await klingGet(
      `${TASKS_QUERY_PATH}?task_ids=${encodeURIComponent(taskId)}`,
      token,
      { contentType: 'application/json' },
    );
    const list = asTaskList(data);
    const hit = list.find((item) => String(taskIdOf(item)) === String(taskId)) || list[0];
    if (!hit) throw new Error(`Task not found / 未找到任务: ${taskId}`);
    return hit;
  }
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
    const status = taskStatusOf(data);
    console.log(`Status / 状态: ${status}`);
    if (isTaskSucceeded(status)) return data;
    if (isTaskFailed(status)) {
      throw new Error(`Task failed / 任务失败: ${taskMessageOf(data) || 'Unknown error'}`);
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
  const url = resultUrlOf(data, urlField);
  if (!url) throw new Error(`Task succeeded but missing ${urlField} / 任务成功但未返回 ${urlField}`);
  await mkdir(outputDir, { recursive: true });
  const outPath = join(outputDir, `${taskId}${ext}`);
  await downloadFile(url, outPath);
  return outPath;
}
