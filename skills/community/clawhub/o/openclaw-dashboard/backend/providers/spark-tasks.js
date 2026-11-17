/**
 * spark-tasks.js — Dashboard backend provider
 * Proxies requests to Local API Hub /spark/* endpoints.
 * Routes:
 *   GET /api/spark-tasks/summary    → today's task summary
 *   GET /api/spark-tasks/list       → recent task list (query: ?type=&status=&limit=)
 *   GET /api/spark-tasks/gpu        → GPU timeline (query: ?hours=24)
 *   GET /dashboard/spark/today      → dashboard-friendly Spark daily summary/value view
 */

const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const HUB_HOST = '127.0.0.1';
const HUB_PORT = 3456;
const NFS_SPARK_TODAY = path.join(os.homedir(), 'spark-nfs', 'spark-agent', 'state', 'spark-dashboard-today.json');

function hubGet(path) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: HUB_HOST, port: HUB_PORT, path, timeout: 8000 }, res => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch (e) { reject(new Error('Invalid JSON from hub')); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Hub timeout')); });
  });
}

async function getSummary() {
  try {
    return await hubGet('/spark/tasks/summary');
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

async function getTaskList(type, status, limit = 20) {
  const qs = new URLSearchParams();
  if (type)   qs.set('type', type);
  if (status) qs.set('status', status);
  qs.set('limit', limit);
  try {
    return await hubGet(`/spark/tasks?${qs}`);
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

async function getGpuTimeline(hours = 24) {
  try {
    return await hubGet(`/spark/gpu/timeline?hours=${hours}`);
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

function estimateCloudCostUsd(totalTokens) {
  // Rough blended estimate for "what cloud would have cost" across Spark workload.
  // Keep simple and explicit; can be replaced by model-aware pricing later.
  const perMillion = 3.0;
  return (Number(totalTokens || 0) / 1_000_000) * perMillion;
}

async function getDashboardSparkToday() {
  // Prefer NFS-backed precomputed summary generated on Spark node itself.
  try {
    if (fs.existsSync(NFS_SPARK_TODAY)) {
      const stat = fs.statSync(NFS_SPARK_TODAY);
      const raw = JSON.parse(fs.readFileSync(NFS_SPARK_TODAY, 'utf8'));
      return {
        ...raw,
        source: 'nfs-file',
        filePath: NFS_SPARK_TODAY,
        fileMtime: stat.mtime.toISOString(),
      };
    }
  } catch (e) {
    // fall through to live aggregation
  }

  const [summary, list, gpu] = await Promise.all([
    getSummary(),
    getTaskList(undefined, undefined, 100),
    getGpuTimeline(24),
  ]);
  if (!summary?.ok) return { ok: false, error: summary?.error || 'spark summary unavailable' };

  const tasks = list?.tasks || [];
  const byType = summary.tasks?.byType || [];
  const byStatus = summary.tasks?.byStatus || [];
  const timeline = gpu?.timeline || [];

  const totalTokens = byType.reduce((s, r) => s + Number(r.total_tokens || 0), 0);
  const completedTasks = byStatus.reduce((s, r) => s + ((r.status === 'done' || r.status === 'completed') ? Number(r.count || 0) : 0), 0);
  const runningTasks = byStatus.reduce((s, r) => s + (r.status === 'running' ? Number(r.count || 0) : 0), 0);
  const failedTasks = byStatus.reduce((s, r) => s + (r.status === 'error' ? Number(r.count || 0) : 0), 0);
  const totalTasks = byStatus.reduce((s, r) => s + Number(r.count || 0), 0);
  const busyPoints = timeline.filter(p => Number(p.gpu_pct || 0) > 0 || Number(p.slots_busy || 0) > 0 || p.active_task);
  const totalPoints = timeline.length;
  const busyMinutes = busyPoints.length * 5;
  const totalMinutes = totalPoints * 5;
  const idleMinutes = Math.max(0, totalMinutes - busyMinutes);
  const gpuUtilizationPct = totalMinutes > 0 ? (busyMinutes / totalMinutes) * 100 : 0;
  const estimatedCloudCostUsd = estimateCloudCostUsd(totalTokens);
  const byTaskType = byType.map(r => ({
    taskType: r.task_type,
    runs: Number(r.count || 0),
    tokens: Number(r.total_tokens || 0),
    avgDurationSec: Number(r.avg_duration_s || 0),
    estimatedCloudCostUsd: estimateCloudCostUsd(Number(r.total_tokens || 0)),
  })).sort((a, b) => b.tokens - a.tokens);

  return {
    ok: true,
    date: summary.date || null,
    source: 'live-fallback',
    summary: {
      totalTasks,
      completedTasks,
      runningTasks,
      failedTasks,
      totalTokens,
      gpuBusyMinutes: busyMinutes,
      gpuIdleMinutes: idleMinutes,
      gpuUtilizationPct,
      estimatedCloudCostUsd,
      estimatedSavingsUsd: estimatedCloudCostUsd,
    },
    byTaskType,
    recent: summary.recent || tasks.slice(0, 10),
    gpu: {
      avgGpu: Number(summary.gpu?.avg_gpu || 0),
      maxGpu: Number(summary.gpu?.max_gpu || 0),
      busyPoints: busyPoints.length,
      totalPoints,
    }
  };
}

function register(router) {
  const { jsonReply } = require('../lib/http-helpers');

  router.add('GET', '/api/spark-tasks/summary', async (req, res) => {
    const data = await getSummary();
    jsonReply(res, 200, data);
  });

  router.add('GET', '/api/spark-tasks/list', async (req, res, q) => {
    const type   = q?.type   || '';
    const status = q?.status || '';
    const limit  = parseInt(q?.limit || '20', 10);
    const data   = await getTaskList(type || undefined, status || undefined, limit);
    jsonReply(res, 200, data);
  });

  router.add('GET', '/api/spark-tasks/gpu', async (req, res, q) => {
    const hours = parseInt(q?.hours || '24', 10);
    const data  = await getGpuTimeline(hours);
    jsonReply(res, 200, data);
  });

  router.add('GET', '/dashboard/spark/today', async (_req, res) => {
    const data = await getDashboardSparkToday();
    jsonReply(res, data.ok ? 200 : 500, data);
  });
}

module.exports = { register };
