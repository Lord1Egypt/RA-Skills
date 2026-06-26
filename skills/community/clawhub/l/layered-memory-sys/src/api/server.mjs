// server.mjs - REST API 服务器 (v2.0)

import http from 'http';
import { URL } from 'url';
import { loadConfig } from '../db/config-loader.mjs';
import { listMemories, getMemoryById, createMemory, updateMemory, deleteMemory, getStats, getEvents, getDueReminders, exportMemories, importMemories } from '../db/repository.mjs';
import { search, highlightSnippet } from '../search/search-engine.mjs';
import { execDreamCycle } from '../dream/dream-cycle.mjs';
import { listJobs, runJob } from '../dream/scheduler.mjs';
import { emit, EVENTS } from '../events/event-bus.mjs';

let _server = null;

export function startServer(config) {
  config = config || loadConfig();
  const port = config?.api?.port || 3456;
  // 确保 config 传给 search

  _server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);
    const path = url.pathname;
    const method = req.method;

    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }

    // JSON body 解析
    let body = {};
    if (method === 'POST' || method === 'PATCH') {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      try { body = JSON.parse(Buffer.concat(chunks).toString()); } catch {}
    }

    try {
      const result = await route(path, method, url.searchParams, body, config);
      res.writeHead(result.status || 200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result.data || result));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
  });

  _server.listen(port);
  console.log(`✅ REST API 服务已启动: http://localhost:${port}`);
  return _server;
}

export function stopServer() {
  if (_server) {
    _server.close();
    _server = null;
    console.log('🛑 REST API 服务已停止');
  }
}

// 路由处理
async function route(path, method, query, body, config) {
  // 记忆 CRUD
  if (path === '/api/memories' && method === 'GET') {
    const { layer, status, limit, offset, orderBy, orderDir } = Object.fromEntries(query);
    return listMemories({ layer, status, limit: parseInt(limit) || 100, offset: parseInt(offset) || 0, orderBy, orderDir });
  }

  if (path.match(/^\/api\/memories\/[^/]+$/) && method === 'GET') {
    const id = path.split('/').pop();
    const mem = getMemoryById(id);
    if (!mem) return { status: 404, error: '记忆不存在' };
    return mem;
  }

  if (path === '/api/memories' && method === 'POST') {
    const mem = createMemory(body);
    emit(EVENTS.MEMORY_CREATED, mem);
    return { status: 201, data: mem };
  }

  if (path.match(/^\/api\/memories\/[^/]+$/) && method === 'PATCH') {
    const id = path.split('/').pop();
    const mem = updateMemory(id, body);
    if (!mem) return { status: 404, error: '记忆不存在' };
    emit(EVENTS.MEMORY_UPDATED, mem);
    return mem;
  }

  if (path.match(/^\/api\/memories\/[^/]+$/) && method === 'DELETE') {
    const id = path.split('/').pop();
    const ok = deleteMemory(id);
    if (!ok) return { status: 404, error: '记忆不存在' };
    emit(EVENTS.MEMORY_DELETED, { id });
    return { status: 204 };
  }

  // 搜索（支持 v1.2 增强）
  if (path === '/api/search' && method === 'POST') {
    const { query: q, limit, threshold, enrich, group } = body;
    let results = await search(q, { limit: parseInt(limit) || 20, threshold: parseFloat(threshold) || 0.01, config });
    for (const r of results) {
      r.snippet = highlightSnippet(r.summary || r.title, q);
    }
    // v1.2: Session 分组
    if (group) {
      const { groupBySession } = await import('../search/context-utils.mjs');
      return { results: groupBySession(results) };
    }
    return { results };
  }

  if (path === '/api/search/tfidf' && method === 'POST') {
    const { query: q, limit, threshold } = body;
    const results = await search(q, { limit: parseInt(limit) || 20, threshold: parseFloat(threshold) || 0.1, config, forceTfidf: true });
    for (const r of results) {
      r.snippet = highlightSnippet(r.summary || r.title, q);
    }
    return { results };
  }

  // 梦境模式
  if (path === '/api/dream/run' && method === 'POST') {
    const stats = await execDreamCycle(config);
    emit(EVENTS.DREAM_COMPLETED, stats);
    return { status: 200, data: stats };
  }

  if (path === '/api/dream/logs' && method === 'GET') {
    const stats = getStats();
    return { logs: stats.dreamLogs };
  }

  if (path === '/api/dream/stats' && method === 'GET') {
    return getStats();
  }

  // 提醒
  if (path === '/api/reminders' && method === 'GET') {
    return { reminders: getDueReminders() };
  }

  if (path === '/api/reminders' && method === 'POST') {
    const mem = createMemory({ ...body, layer: 'attention', type: 'recurring' });
    emit(EVENTS.MEMORY_CREATED, mem);
    return { status: 201, data: mem };
  }

  if (path.match(/^\/api\/reminders\/[^/]+$/) && method === 'DELETE') {
    const id = path.split('/').pop();
    deleteMemory(id);
    return { status: 204 };
  }

  // 调度器
  if (path === '/api/scheduler/jobs' && method === 'GET') {
    return { jobs: listJobs() };
  }

  if (path.match(/^\/api\/scheduler\/jobs\/[^/]+\/run$/) && method === 'POST') {
    const jobId = path.split('/')[3];
    await runJob(jobId, config);
    return { status: 200, data: { jobId, executed: true } };
  }

  //导入导出
  if (path === '/api/export' && method === 'GET') {
    const { layer, type, status } = Object.fromEntries(query);
    return exportMemories({ layer, type, status });
  }
  
  if (path === '/api/export/download' && method === 'GET') {
    const { layer, type, status } = Object.fromEntries(query);
    const data = exportMemories({ layer, type, status: status || 'all' });
    // 直接返回 JSON 字符串供下载
    return { filename: `memories-${new Date().toISOString().split('T')[0]}.json`, data: JSON.stringify(data, null, 2) };
  }
  
  if (path === '/api/import' && method === 'POST') {
    const { memories, mode } = body;
    if (!memories || !Array.isArray(memories)) {
      return { status: 400, error: '需要 memories 数组' };
    }
    return importMemories(memories, { mode: mode || 'append' });
  }

  // 系统
  if (path === '/api/health' && method === 'GET') {
    return { status: 'ok', version: '2.0.0' };
  }

  if (path === '/api/stats' && method === 'GET') {
    return getStats();
  }

  if (path === '/api/events' && method === 'GET') {
    const { type, limit } = Object.fromEntries(query);
    return { events: getEvents({ type, limit: parseInt(limit) || 50 }) };
  }

  return { status: 404, error: '路由不存在' };
}