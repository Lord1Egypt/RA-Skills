---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502201f7c72bd301637e5be5d6e2faf70f9a774b448ef1656634a5df7e84a2fd73cad022100d5758ed4f4dd76f81e7f6bd181edfb053ac02ed19d3d0ab0c800e66499001826
    ReservedCode2: 30460221008b35c223d1386e33e0d1935beea4fd5d1d92589b8ff103e8f4d9ca7936da49a1022100d4a5ac827703fed96f3981214dd31a5007a3f32ecdab9adb9f3a10f9a31dd137
---

# 断点续跑详细方案

## 核心问题

执行一个耗时任务，执行到 90% 崩溃了，重启后从头开始 → 浪费资源，可能永远跑不完。

## 解决方案：任务状态持久化

### 三层持久化策略

| 层级 | 适用场景 | 实现方式 |
|------|----------|----------|
| 文件 | 单机、轻量任务 | JSON 文件 |
| Redis | 分布式、关键任务 | 消息队列 |
| 数据库 | 复杂状态、查询需求 | PostgreSQL/MySQL |

---

## 一、文件方式（最简单）

```js
const fs = require('fs');
const path = require('path');

const DATA_DIR = '/home/openclaw/data';
const PROGRESS_FILE = path.join(DATA_DIR, 'task_progress.json');
const STATE_FILE = path.join(DATA_DIR, 'heartbeat-state.json');

// 确保目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

/**
 * 保存任务进度
 * @param {string} taskId - 任务ID
 * @param {object} progress - 进度数据
 */
function saveProgress(taskId, progress) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  data[taskId] = {
    ...progress,
    updatedAt: new Date().toISOString(),
    updatedAtMs: Date.now(),
  };
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data, null, 2));
}

/**
 * 读取任务进度
 * @param {string} taskId
 * @returns {object|null}
 */
function loadProgress(taskId) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  return data[taskId] || null;
}

/**
 * 清除任务进度（任务完成后调用）
 * @param {string} taskId
 */
function clearProgress(taskId) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  delete data[taskId];
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data, null, 2));
}

/**
 * 获取所有任务进度
 * @returns {object}
 */
function getAllProgress() {
  return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
}

/**
 * 心跳状态持久化
 */
function saveHeartbeatState(key, value) {
  const data = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8') || '{}');
  data[key] = { value, updatedAt: Date.now() };
  fs.writeFileSync(STATE_FILE, JSON.stringify(data, null, 2));
}

function loadHeartbeatState(key) {
  const data = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8') || '{}');
  return data[key] || null;
}

module.exports = {
  saveProgress,
  loadProgress,
  clearProgress,
  getAllProgress,
  saveHeartbeatState,
  loadHeartbeatState,
  PROGRESS_FILE,
  STATE_FILE,
};
```

---

## 二、Redis 方式（分布式/关键任务）

```js
const Redis = require('ioredis');

// 连接 Redis
const redis = new Redis({ host: 'localhost', port: 6379, password: process.env.REDIS_PASSWORD });

const QUEUE_NAME = 'openclaw_tasks';

/**
 * 任务入队（持久化保证不丢失）
 */
async function enqueueTask(name, data, options = {}) {
  const job = {
    id: `${name}:${Date.now()}:${Math.random().toString(36).slice(2)}`,
    name,
    data,
    attempts: 0,
    maxAttempts: options.maxAttempts || 3,
    backoff: options.backoff || { type: 'exponential', delay: 2000 },
    createdAt: Date.now(),
    status: 'pending',
  };
  await redis.rpush(QUEUE_NAME, JSON.stringify(job));
  return job.id;
}

/**
 * 任务出队（阻塞等待）
 */
async function dequeueTask(timeout = 5) {
  const result = await redis.blpop(QUEUE_NAME, timeout);
  if (!result) return null;
  return JSON.parse(result[1]);
}

/**
 * 任务重试
 */
async function retryTask(job) {
  job.attempts += 1;
  job.status = 'retry';
  const delay = job.backoff.type === 'exponential'
    ? job.backoff.delay * Math.pow(2, job.attempts - 1)
    : job.backoff.delay;
  setTimeout(async () => {
    await redis.rpush(QUEUE_NAME, JSON.stringify(job));
  }, delay);
}

/**
 * 保存任务进度到 Redis
 */
async function saveTaskProgress(taskId, progress) {
  await redis.set(
    `task:progress:${taskId}`,
    JSON.stringify({ ...progress, updatedAt: Date.now() }),
    'EX', 86400 * 7  // 7 天过期
  );
}

async function loadTaskProgress(taskId) {
  const data = await redis.get(`task:progress:${taskId}`);
  return data ? JSON.parse(data) : null;
}

module.exports = {
  enqueueTask,
  dequeueTask,
  retryTask,
  saveTaskProgress,
  loadTaskProgress,
};
```

---

## 三、任务断点续跑使用模式

### 模式一：批处理任务

```js
async function processLargeDataset(dataset, taskId) {
  // 1. 检查是否有保存的进度
  const saved = loadProgress(taskId);
  const startIndex = saved?.lastIndex || 0;
  console.log(`[${taskId}] 从 index ${startIndex} 继续，共 ${dataset.length} 条`);

  for (let i = startIndex; i < dataset.length; i++) {
    try {
      await processItem(dataset[i]);

      // 2. 每 100 条保存一次进度
      if (i % 100 === 0) {
        saveProgress(taskId, {
          lastIndex: i,
          total: dataset.length,
          percent: ((i / dataset.length) * 100).toFixed(1),
        });
      }
    } catch (error) {
      console.error(`[${taskId}] 处理第 ${i} 条失败:`, error.message);
      // 记录失败条目，稍后重试
      saveProgress(taskId + ':failed', {
        lastIndex: i,
        failedItems: [...(loadProgress(taskId + ':failed')?.failedItems || []), { index: i, error: error.message }],
      });
    }
  }

  // 3. 完成后清除进度
  clearProgress(taskId);
  console.log(`[${taskId}] 全部完成！`);
}
```

### 模式二：定时心跳任务

```js
const { saveHeartbeatState, loadHeartbeatState } = require('./task-resume');

async function runScheduledTask() {
  const LAST_RUN_KEY = 'last_email_check';
  const INTERVAL = 3600000; // 1 小时

  const state = loadHeartbeatState(LAST_RUN_KEY);

  if (state && (Date.now() - state.value.updatedAt) < INTERVAL) {
    console.log('距上次执行不足 1 小时，跳过');
    return;
  }

  console.log('执行邮件检查...');
  await checkEmails();

  saveHeartbeatState(LAST_RUN_KEY, { updatedAt: Date.now() });
}
```

---

## 四、断点续跑检查清单

- [ ] 进度保存频率合理（不要太频繁影响性能，也不要太久丢失太多）
- [ ] 任务开始前检查是否有保存的进度
- [ ] 任务完成后清除进度记录
- [ ] 失败条目单独记录，便于排查
- [ ] 进度文件有备份（可考虑 JSON+时间戳命名）
- [ ] 心跳任务使用持久化状态，不依赖内存计时器
