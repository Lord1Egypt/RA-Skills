/**
 * OpenClaw Connect Enterprise - Node Server v3.0
 * Can run standalone OR be mounted on Hub under /node prefix
 */

import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import fastifyStatic from '@fastify/static';
import axios from 'axios';
import * as os from 'os';
import * as path from 'path';
import * as fs from 'fs';
import { execSync, execFileSync } from 'child_process';

// ─── Configuration ───────────────────────────────────────────────
const HUB_URL = process.env.HUB_URL || '';
const APP_ID = process.env.NODE_APP_ID || process.env.APP_ID || '';
const APP_KEY = process.env.NODE_APP_KEY || process.env.APP_KEY || '';
const APP_TOKEN = process.env.NODE_TOKEN || process.env.APP_TOKEN || '';
const NODE_NAME = process.env.NODE_NAME || os.hostname();

// Resolved Hub URL (env var overrides persisted config)
function resolvedHubUrl() {
  return HUB_URL || persistedConfig.hubUrl || '';
}
const NODE_PORT = parseInt(process.env.NODE_PORT || '3200');
const DATA_DIR = process.env.DATA_DIR || path.join(process.cwd(), 'data');
const NODE_VERSION = '0.1.5';
const startTime = Date.now();

// ─── Persistent Node Config ───────────────────────────────────────
// Credentials are saved to disk after successful Hub registration
// so the node can reconnect after restarts without manual re-entry
const NODE_CONFIG_PATH = path.join(os.homedir(), '.openclaw-node', 'node.json');

interface NodeConfig {
  hubUrl: string;
  appId: string;
  appKey: string;
  appToken: string;
  nodeId: string;
  sessionToken: string;
  registeredAt: string;
}

function loadNodeConfig(): Partial<NodeConfig> {
  try {
    if (fs.existsSync(NODE_CONFIG_PATH)) {
      const raw = fs.readFileSync(NODE_CONFIG_PATH, 'utf-8');
      return JSON.parse(raw);
    }
  } catch {}
  return {};
}

function saveNodeConfig(cfg: NodeConfig) {
  try {
    const dir = path.dirname(NODE_CONFIG_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(NODE_CONFIG_PATH, JSON.stringify(cfg, null, 2), 'utf-8');
  } catch (e: any) {
    console.error('[Node][WARN] 保存节点配置失败:', e.message);
  }
}

// Load persisted credentials at startup (env vars take priority)
const persistedConfig = loadNodeConfig();
// Allow env vars to override persisted values
const effectiveAppId = APP_ID || persistedConfig.appId || '';
const effectiveAppKey = APP_KEY || persistedConfig.appKey || '';
const effectiveAppToken = APP_TOKEN || persistedConfig.appToken || '';
// Use persisted nodeId/sessionToken if we have them (avoids re-registration)
if (persistedConfig.nodeId) nodeId = persistedConfig.nodeId;
if (persistedConfig.sessionToken) sessionToken = persistedConfig.sessionToken;

// ─── Connection State ────────────────────────────────────────────
let nodeId = '';
let sessionToken = '';
let connected = false;
let connecting = false;
let lastHeartbeat = '';
let registeredAt = '';
let connectionError = '';

interface ConnectionLog {
  time: string;
  type: 'info' | 'error' | 'success' | 'warning';
  message: string;
}
const MAX_CONNECTION_LOGS = 100;  // 🔐 限制连接日志数量，防止内存泄漏
const connectionLogs: ConnectionLog[] = [];
function addLog(type: ConnectionLog['type'], message: string) {
  connectionLogs.unshift({ time: new Date().toISOString(), type, message });
  if (connectionLogs.length > MAX_CONNECTION_LOGS) connectionLogs.length = MAX_CONNECTION_LOGS;
  console.log(`[Node][${type.toUpperCase()}] ${message}`);
}

// ─── Local Data (read/write) ─────────────────────────────────────
interface Memory {
  id: string;
  type: 'stm' | 'mtm' | 'ltm';
  content: string;
  source: string;
  importance: number;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

const localMemories = new Map<string, Memory>();
let memoryIdCounter = 1;

// ─── Synced Data (read-only) ─────────────────────────────────────
let syncedTasks: any[] = [];
let syncedSkills: any[] = [];
let syncedHubAgents: any[] = [];  // Fix 2: Hub 同步过来的 Agent 列表

// ─── Timers ──────────────────────────────────────────────────────
let heartbeatTimer: ReturnType<typeof setInterval> | null = null;
let taskSyncTimer: ReturnType<typeof setInterval> | null = null;
let skillSyncTimer: ReturnType<typeof setInterval> | null = null;
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

// ─── System Monitor ──────────────────────────────────────────────
let prevCpuTimes: { idle: number; total: number } | null = null;

function getCpuUsage(): number {
  const cpus = os.cpus();
  let totalIdle = 0, totalTick = 0;
  for (const cpu of cpus) {
    for (const type in cpu.times) totalTick += (cpu.times as any)[type];
    totalIdle += cpu.times.idle;
  }

  if (prevCpuTimes === null) {
    prevCpuTimes = { idle: totalIdle, total: totalTick };
    return 0; // First call: no baseline, return 0
  }

  const idleDelta = totalIdle - prevCpuTimes.idle;
  const totalDelta = totalTick - prevCpuTimes.total;
  prevCpuTimes = { idle: totalIdle, total: totalTick };

  if (totalDelta === 0) return 0;
  return Math.min(100, Math.round((1 - idleDelta / totalDelta) * 100));
}

function getMemoryUsage() {
  const total = os.totalmem();
  const free = os.freemem();
  const used = total - free;
  return {
    total: Math.round(total / 1024 / 1024 / 1024 * 100) / 100,
    used: Math.round(used / 1024 / 1024 / 1024 * 100) / 100,
    free: Math.round(free / 1024 / 1024 / 1024 * 100) / 100,
    percentage: Math.round(used / total * 100),
  };
}

function getDiskUsage() {
  try {
    const output = execSync("df -B1 / | tail -1").toString().trim();
    const parts = output.split(/\s+/);
    const total = parseInt(parts[1]);
    const used = parseInt(parts[2]);
    return {
      total: Math.round(total / 1024 / 1024 / 1024 * 100) / 100,
      used: Math.round(used / 1024 / 1024 / 1024 * 100) / 100,
      free: Math.round((total - used) / 1024 / 1024 / 1024 * 100) / 100,
      percentage: Math.round(used / total * 100),
    };
  } catch (err) {
    console.error('[Node][ERROR] getDiskUsage failed:', err);
    return { total: 0, used: 0, free: 0, percentage: 0 };
  }
}

function getSystemInfo() {
  return {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    cpuModel: os.cpus()[0]?.model || 'Unknown',
    cpuCores: os.cpus().length,
    nodeVersion: process.version,
    uptime: os.uptime(),
  };
}

// ─── Auto-register Local Agents ──────────────────────────────────
async function registerLocalAgents() {
  if (!nodeId || !sessionToken) return;
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return;

  const homeDir = process.env.HOME || '/root';

  // 扫描 SOUL.md 和 IDENTITY.md
  const soulPath = path.join(homeDir, '.openclaw/workspace/SOUL.md');
  const identityPath = path.join(homeDir, '.openclaw/workspace/IDENTITY.md');

  let agentName = os.hostname();
  let soulMd = '';
  let channel: string | null = null;
  let capabilities: string[] = [];
  let skills: string[] = [];

  // 读取 IDENTITY.md
  if (fs.existsSync(identityPath)) {
    const content = fs.readFileSync(identityPath, 'utf-8');
    const nameMatch = content.match(/\*\*Name:\*\*\s*(.+)/);
    if (nameMatch) agentName = nameMatch[1].trim();
  }

  // 读取 SOUL.md
  if (fs.existsSync(soulPath)) {
    soulMd = fs.readFileSync(soulPath, 'utf-8').slice(0, 2000);
  }

  // 扫描技能列表
  const skillsDir = path.join(homeDir, '.openclaw/workspace/skills');
  if (fs.existsSync(skillsDir)) {
    skills = fs.readdirSync(skillsDir).filter(d =>
      fs.existsSync(path.join(skillsDir, d, 'SKILL.md'))
    );
  }

  // 扫描渠道配置
  try {
    const configOutput = execSync('cat ~/.openclaw/config.yaml 2>/dev/null || echo ""').toString();
    if (configOutput.includes('feishu')) channel = 'feishu';
    else if (configOutput.includes('wecom')) channel = 'wecom';
    else if (configOutput.includes('telegram')) channel = 'telegram';
    else if (configOutput.includes('discord')) channel = 'discord';
  } catch (err) {
    addLog('warning', `扫描渠道配置失败: ${err}`);
  }

  capabilities = ['reasoning', 'coding', 'writing'];

  // 注册到 Hub
  try {
    const res = await axios.post(`${hubUrl}/api/nodes/${nodeId}/agents/register`, {
      name: agentName,
      role: 'worker',
      soulMd,
      channel,
      capabilities,
      skills,
    }, {
      headers: { Authorization: `Bearer ${sessionToken}` },
      timeout: 10000,
    });

    if (res.data?.code === 0) {
      addLog('success', `Agent "${agentName}" 已注册到 Hub`);
    }
  } catch (err: any) {
    console.error('[Node][ERROR] Agent 注册失败:', err);
  }
}

// ─── Hub Communication ───────────────────────────────────────────
function clearTimers() {
  if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
  if (taskSyncTimer) { clearInterval(taskSyncTimer); taskSyncTimer = null; }
  if (skillSyncTimer) { clearInterval(skillSyncTimer); skillSyncTimer = null; }
  if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  stopExecutor();
}

function startTimers() {
  clearTimers();
  heartbeatTimer = setInterval(sendHeartbeat, 30000);
  taskSyncTimer = setInterval(fetchTasks, 30000);
  skillSyncTimer = setInterval(fetchSkills, 60000);
}

async function registerWithHub(): Promise<boolean> {
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  const appId = effectiveAppId;
  const appKey = effectiveAppKey;
  const appToken = effectiveAppToken;

  if (!hubUrl || !appId || !appKey || !appToken) {
    addLog('warning', '未配置 HUB_URL / APP_ID / APP_KEY / APP_TOKEN，跳过注册');
    return false;
  }

  connecting = true;
  connectionError = '';
  addLog('info', `正在向 Hub 注册: ${hubUrl}`);

  try {
    const res = await axios.post(`${hubUrl}/api/nodes/register`, {
      appId,
      key: appKey,
      token: appToken,
      name: NODE_NAME,
      hostname: os.hostname(),
      port: NODE_PORT,
      platform: os.platform(),
      arch: os.arch(),
      capabilities: ['task-execution', 'monitoring'],
      nodeVersion: NODE_VERSION,
    }, { timeout: 10000 });

    if (res.data?.code === 0 && res.data?.data) {
      nodeId = res.data.data.nodeId;
      sessionToken = res.data.data.sessionToken;
      connected = true;
      connecting = false;
      registeredAt = new Date().toISOString();
      reconnectAttempts = 0; // Reset on successful connection
      addLog('success', `注册成功! nodeId=${nodeId}`);
      // 🔐 持久化凭证到本地磁盘，重启后无需重新配置
      saveNodeConfig({ hubUrl, appId, appKey, appToken, nodeId, sessionToken, registeredAt });
      startTimers();
      await fetchTasks();
      await fetchSkills();
      await registerLocalAgents();
      // Start task executor after everything is connected
      startExecutor().catch(e => addLog('error', `Executor 启动失败: ${e.message}`));
      return true;
    } else {
      throw new Error(res.data?.message || '注册返回异常');
    }
  } catch (err: any) {
    const msg = err.response?.data?.message || err.message;
    connectionError = msg;
    connected = false;
    connecting = false;
    addLog('error', `注册失败: ${msg}`);
    scheduleReconnect();
    return false;
  }
}

let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 300000; // 5 minutes max

function scheduleReconnect() {
  if (reconnectTimer) return;
  reconnectAttempts++;
  // Exponential backoff: 30s, 60s, 120s, 240s, 300s (cap)
  const delay = Math.min(30000 * Math.pow(2, reconnectAttempts - 1), MAX_RECONNECT_DELAY);
  const delaySec = Math.round(delay / 1000);
  if (reconnectAttempts >= 5) {
    addLog('error', `连续 ${reconnectAttempts} 次连接失败，${delaySec}秒后继续重试...`);
  } else {
    addLog('info', `将在 ${delaySec} 秒后重试连接 (第 ${reconnectAttempts} 次)...`);
  }
  reconnectTimer = setTimeout(async () => {
    reconnectTimer = null;
    await registerWithHub();
  }, delay);
}

async function sendHeartbeat() {
  if (!nodeId || !connected) return;
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return;
  try {
    // Collect workspace memories to sync with Hub
    const pendingMemories = collectWorkspaceMemories();
    
    const heartbeatPayload: any = {
      cpu: getCpuUsage(),
      memory: getMemoryUsage(),
      disk: getDiskUsage(),
      uptime: os.uptime(),
      timestamp: new Date().toISOString(),
      nodeVersion: NODE_VERSION,
    };
    
    // Include memories if we have any to sync
    if (pendingMemories.length > 0) {
      heartbeatPayload.memories = pendingMemories;
    }
    
    const res = await axios.post(`${hubUrl}/api/nodes/${nodeId}/heartbeat`, heartbeatPayload, {
      headers: { Authorization: `Bearer ${sessionToken}` },
      timeout: 10000,  // longer timeout when syncing memories
    });
    lastHeartbeat = new Date().toISOString();
    connected = true;
    
    // Check for memory warnings from Hub
    const memWarning = res.data?.data?.memoryWarning;
    if (memWarning) {
      addLog('warning', `Hub 告警: ${memWarning.message}`);
    }

    // Fix 2: Sync Hub-created agents so Node knows about newly assigned agents
    await fetchHubAgents();
  } catch (err: any) {
    addLog('error', `心跳失败: ${err.message}`);
    connected = false;
    clearTimers();
    scheduleReconnect();
  }
}

// ─── Workspace Memory Collector ───
// Reads MEMORY.md + memory/*.md from local OpenClaw workspace
// Returns array of memory objects to sync with Hub via heartbeat
const MAX_SYNCED_HASHES = 10000;  // 🔐 防止内存泄漏，限制 Set 大小
const syncedMemoryHashes = new Set<string>();

// 🔐 定期清理已同步的哈希，防止内存泄漏
setInterval(() => {
  if (syncedMemoryHashes.size > MAX_SYNCED_HASHES) {
    const entries = Array.from(syncedMemoryHashes);
    syncedMemoryHashes.clear();
    entries.slice(-MAX_SYNCED_HASHES / 2).forEach(h => syncedMemoryHashes.add(h));
    console.log('[Node] 🧹 Cleaned syncedMemoryHashes, now size:', syncedMemoryHashes.size);
  }
}, 10 * 60 * 1000);  // 每 10 分钟检查一次

function collectWorkspaceMemories(): any[] {
  const homeDir = os.homedir();
  const WORKSPACE = path.join(homeDir, '.openclaw/workspace');
  const MEMORY_MD = path.join(WORKSPACE, 'MEMORY.md');
  const MEMORY_DIR = path.join(WORKSPACE, 'memory');
  const results: any[] = [];

  function contentHash(content: string): string {
    const crypto = require('crypto');
    return crypto.createHash('md5').update(content.trim()).digest('hex');
  }

  function parseMarkdownSections(text: string): Array<{title: string; body: string}> {
    const sections: Array<{title: string; body: string}> = [];
    const lines = text.split('\n');
    let currentTitle = '';
    let currentBody: string[] = [];
    for (const line of lines) {
      const headingMatch = line.match(/^##\s+(.+)/);
      if (headingMatch) {
        if (currentTitle && currentBody.join('\n').trim()) {
          sections.push({ title: currentTitle, body: currentBody.join('\n').trim() });
        }
        currentTitle = headingMatch[1].trim();
        currentBody = [];
      } else {
        currentBody.push(line);
      }
    }
    if (currentTitle && currentBody.join('\n').trim()) {
      sections.push({ title: currentTitle, body: currentBody.join('\n').trim() });
    }
    return sections;
  }

  function addMemory(type: string, title: string, body: string, tags: string[]) {
    const content = `## ${title}\n${body}`;
    const hash = contentHash(content);
    if (syncedMemoryHashes.has(hash)) return; // Already synced
    syncedMemoryHashes.add(hash);
    results.push({
      type,
      content,
      importance: type === 'ltm' ? 8 : type === 'mtm' ? 5 : 3,
      tags,
      createdAt: new Date().toISOString(),
    });
  }

  try {
    // 1. MEMORY.md → LTM
    if (fs.existsSync(MEMORY_MD)) {
      const text = fs.readFileSync(MEMORY_MD, 'utf-8');
      const sections = parseMarkdownSections(text);
      for (const s of sections) {
        const cleanTitle = s.title.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu, '').trim();
        addMemory('ltm', s.title, s.body, cleanTitle ? ['workspace', cleanTitle] : ['workspace']);
      }
    }

    // 2. memory/*.md → STM (date files) or MTM (others)
    if (fs.existsSync(MEMORY_DIR)) {
      const files = fs.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.md'));
      const datePattern = /^\d{4}-\d{2}-\d{2}\.md$/;
      
      // Only sync recent files (last 7 days) to avoid massive payloads
      const now = Date.now();
      const sevenDaysAgo = now - 7 * 24 * 60 * 60 * 1000;
      
      for (const file of files) {
        const filePath = path.join(MEMORY_DIR, file);
        const stat = fs.statSync(filePath);
        if (stat.mtimeMs < sevenDaysAgo) continue; // Skip old files
        
        const type = datePattern.test(file) ? 'stm' : 'mtm';
        const text = fs.readFileSync(filePath, 'utf-8');
        const sections = parseMarkdownSections(text);
        for (const s of sections) {
          const cleanTitle = s.title.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu, '').trim();
          addMemory(type, s.title, s.body, cleanTitle ? [file.replace('.md',''), cleanTitle] : [file.replace('.md','')]);
        }
      }
    }
  } catch (err) {
    console.error('[Node][ERROR] collectWorkspaceMemories failed:', err);
  }

  return results;
}

// Fix 2: Fetch Hub's agent list so Node knows about newly assigned agents
async function fetchHubAgents() {
  if (!nodeId || !sessionToken) return;
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return;
  try {
    const res = await axios.get(`${hubUrl}/api/nodes/${nodeId}/agents`, {
      headers: { Authorization: `Bearer ${sessionToken}` },
      timeout: 10000,
    });
    if (res.data?.code === 0 && Array.isArray(res.data.data)) {
      const newAgents = (res.data.data as any[]).filter((a: any) => a.nodeId === nodeId);
      const existingIds = new Set(syncedHubAgents.map(a => a.id));
      const added = newAgents.filter(a => !existingIds.has(a.id));
      syncedHubAgents = newAgents;
      for (const agent of added) {
        addLog('info', `📋 从 Hub 同步新 Agent: ${agent.name} (${agent.id})`);
      }
    }
  } catch (err: any) {
    // Silent fail - agents sync is best-effort
    console.log('[Node] fetchHubAgents failed:', err.message);
  }
}

async function fetchTasks() {
  if (!nodeId || !sessionToken) return;
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return;
  try {
    const res = await axios.get(`${hubUrl}/api/nodes/${nodeId}/tasks`, {
      headers: { Authorization: `Bearer ${sessionToken}` },
      timeout: 10000,
    });
    if (res.data?.code === 0 && Array.isArray(res.data.data)) {
      syncedTasks = res.data.data;
    }
  } catch (err: any) {
    addLog('error', `拉取任务失败: ${err.message}`);
  }
}

async function fetchSkills() {
  if (!sessionToken) return;
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return;
  try {
    const res = await axios.get(`${hubUrl}/api/skills`, {
      headers: { Authorization: `Bearer ${sessionToken}` },
      timeout: 10000,
    });
    if (res.data?.code === 0 && Array.isArray(res.data.data)) {
      syncedSkills = res.data.data;
    }
  } catch (err: any) {
    addLog('error', `拉取技能失败: ${err.message}`);
  }
}

async function reportTaskAction(taskId: string, action: 'start' | 'complete' | 'fail', body?: any) {
  if (!sessionToken) throw new Error('未连接到 Hub');
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) throw new Error('未配置 Hub URL');
  // Fix 3: 报告时附带 nodeId，让 Hub 知道是哪个节点完成的任务
  const payload = { ...body, nodeId };
  // 🔐 使用节点专用端点 /node/api/tasks/ 而不是 /api/tasks/
  const res = await axios.post(`${hubUrl}/node/api/tasks/${taskId}/${action}`, payload, {
    headers: { Authorization: `Bearer ${sessionToken}` },
    timeout: 10000,
  });
  if (res.data?.code === 0) {
    await fetchTasks();
    return res.data;
  }
  throw new Error(res.data?.message || '操作失败');
}

// ─── Task Executor ───────────────────────────────────────────────
// Automatically picks up pending tasks and executes via local OpenClaw Gateway.
// Compatible with OpenClaw 2026.3.x (CLI + REST fallback).
//
// Execution strategy (ordered by preference):
//   1. Gateway REST: POST /tools/invoke (fastest, 2026.3.x+)
//   2. Gateway Chat: POST /v1/chat/completions (if enabled, 2026.3.x+)
//   3. CLI fallback: openclaw agent -m "..." (universal, any version)
//
// Each strategy is probed once at startup; unavailable ones are skipped.

interface ExecutorConfig {
  enabled: boolean;
  maxConcurrent: number;          // Max simultaneous tasks
  minMemoryPct: number;           // Don't execute if memory% > this
  taskTimeoutMs: number;          // Per-task timeout
  pollIntervalMs: number;         // How often to check for pending tasks
  gatewayUrl: string;             // Local gateway URL
  gatewayToken: string;           // Gateway auth token
  openclawPath: string;           // Path to openclaw CLI binary
}

// Auto-detect gateway config from local OpenClaw installation
function detectExecutorConfig(): ExecutorConfig {
  const homeDir = os.homedir();
  let gatewayUrl = 'http://127.0.0.1:18789';
  let gatewayToken = '';
  let openclawPath = '';
  
  // 1. Try reading OpenClaw config for gateway port + token
  try {
    const configPaths = [
      path.join(homeDir, '.openclaw/openclaw.json'),
      path.join(homeDir, '.openclaw/config.json'),
    ];
    for (const cp of configPaths) {
      if (fs.existsSync(cp)) {
        const conf = JSON.parse(fs.readFileSync(cp, 'utf-8'));
        const gw = conf.gateway || {};
        const port = gw.port || 18789;
        const bind = gw.bind || 'loopback';
        const host = bind === 'loopback' ? '127.0.0.1' : '0.0.0.0';
        gatewayUrl = `http://${host}:${port}`;
        gatewayToken = gw.auth?.token || '';
        break;
      }
    }
  } catch (err) {
    console.error('[Node][ERROR] 读取 OpenClaw 配置失败:', err);
  }
  
  // 2. Env overrides
  if (process.env.OPENCLAW_GATEWAY_URL) gatewayUrl = process.env.OPENCLAW_GATEWAY_URL;
  if (process.env.OPENCLAW_GATEWAY_TOKEN) gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
  if (process.env.OPENCLAW_GATEWAY_PORT) {
    gatewayUrl = `http://127.0.0.1:${process.env.OPENCLAW_GATEWAY_PORT}`;
  }
  
  // 3. Find openclaw CLI binary
  const candidates = [
    path.join(homeDir, '.local/share/pnpm/openclaw'),
    '/usr/local/bin/openclaw',
    '/usr/bin/openclaw',
    path.join(homeDir, '.nvm/versions/node', 'openclaw'),  // won't match but safe
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) { openclawPath = c; break; }
  }
  // Fallback: try `which openclaw`
  if (!openclawPath) {
    try {
      openclawPath = execSync('which openclaw 2>/dev/null').toString().trim();
    } catch (err) {
      console.error('[Node][ERROR] 查找 openclaw CLI 失败:', err);
    }
  }
  
  return {
    enabled: process.env.TASK_EXECUTOR !== 'false',
    maxConcurrent: parseInt(process.env.TASK_MAX_CONCURRENT || '2'),
    minMemoryPct: parseInt(process.env.TASK_MIN_MEMORY_PCT || '90'),
    taskTimeoutMs: parseInt(process.env.TASK_TIMEOUT_MS || '300000'), // 5min
    pollIntervalMs: parseInt(process.env.TASK_POLL_MS || '30000'),   // 30s
    gatewayUrl,
    gatewayToken,
    openclawPath,
  };
}

type ExecutionMethod = 'tools-invoke' | 'chat-completions' | 'cli' | 'hub-execute' | null;

let executorConfig: ExecutorConfig;
let executorRunning = false;
let activeTaskCount = 0;
const executingTaskIds = new Set<string>();
let executorTimer: ReturnType<typeof setInterval> | null = null;
let availableMethod: ExecutionMethod = null;

// Probe which execution method is available
async function probeExecutionMethod(): Promise<ExecutionMethod> {
  const config = executorConfig;
  
  // Method 1: POST /tools/invoke (requires gateway + token)
  if (config.gatewayToken) {
    try {
      const res = await axios.post(`${config.gatewayUrl}/tools/invoke`, {
        tool: 'session_status',
        args: {},
      }, {
        headers: { Authorization: `Bearer ${config.gatewayToken}` },
        timeout: 5000,
      });
      if (res.data?.ok) {
        addLog('info', '✅ Task Executor: 使用 Gateway REST API (tools/invoke)');
        return 'tools-invoke';
      }
    } catch (err) {
      console.error('[Node][WARN] tools/invoke 探测失败:', err);
    }
  }
  

  // Method 2: POST /v1/chat/completions (needs to be enabled in config)
  if (config.gatewayToken) {
    try {
      const res = await axios.post(`${config.gatewayUrl}/v1/chat/completions`, {
        model: 'openclaw:main',
        messages: [{ role: 'user', content: 'ping' }],
      }, {
        headers: { Authorization: `Bearer ${config.gatewayToken}` },
        timeout: 10000,
      });
      if (res.data?.choices) {
        addLog('info', '✅ Task Executor: 使用 Gateway Chat API (v1/chat/completions)');
        return 'chat-completions';
      }
    } catch (err) {
      console.error('[Node][WARN] chat/completions 探测失败:', err);
    }
  }
  
  // Method 3: openclaw agent CLI (universal fallback)
  if (config.openclawPath && fs.existsSync(config.openclawPath)) {
    try {
      const version = execSync(`${config.openclawPath} --version 2>&1`).toString().trim();
      if (version.includes('OpenClaw')) {
        addLog('info', `✅ Task Executor: 使用 CLI 回退 (${version})`);
        return 'cli';
      }
    } catch (err) {
      console.error('[Node][WARN] CLI 版本检查失败:', err);
    }
  }
  
  // Method 4: Hub Execute API (node delegates to Hub's CLI)
  const hubOk = await probeHubExecute();
  if (hubOk) {
    addLog('info', '✅ Task Executor: 使用 Hub 执行代理 API');
    return 'hub-execute';
  }

  addLog('warning', '⚠️ Task Executor: 未找到可用的执行方法（Gateway 未运行或 CLI 不可用）');
  return null;
}

// Probe: Check if Hub execute API is available (Method 4)
async function probeHubExecute(): Promise<boolean> {
  const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
  if (!hubUrl) return false;
  try {
    const res = await axios.post(`${hubUrl}/node/api/execute`, {
      taskId: '__probe__',
      prompt: 'reply with OK',
      timeoutMs: 30000,
    }, { timeout: 40000 });
    return res.data?.code === 0;
  } catch {
    return false;
  }
}

// Execute a task using the best available method
async function executeTaskContent(taskTitle: string, taskDescription: string): Promise<string> {
  const config = executorConfig;
  const prompt = taskDescription
    ? `任务: ${taskTitle}\n\n${taskDescription}`
    : `任务: ${taskTitle}`;
  
  // Re-probe if method was lost
  if (!availableMethod) {
    availableMethod = await probeExecutionMethod();
  }
  if (!availableMethod) {
    throw new Error('无可用执行方法：Gateway 未运行且 CLI 不可用');
  }
  
  if (availableMethod === 'tools-invoke') {
    // Use sessions_spawn to run as isolated sub-agent
    const res = await axios.post(`${config.gatewayUrl}/tools/invoke`, {
      tool: 'sessions_spawn',
      args: {
        task: prompt,
        mode: 'run',
        runtime: 'subagent',
        runTimeoutSeconds: Math.floor(config.taskTimeoutMs / 1000),
      },
    }, {
      headers: { Authorization: `Bearer ${config.gatewayToken}` },
      timeout: config.taskTimeoutMs + 10000,
    });
    
    if (res.data?.ok) {
      const result = res.data.result;
      // Extract text content
      if (typeof result === 'string') return result;
      if (result?.content) {
        const texts = result.content
          .filter((c: any) => c.type === 'text')
          .map((c: any) => c.text);
        return texts.join('\n') || JSON.stringify(result);
      }
      return JSON.stringify(result);
    }
    
    // If tools-invoke fails, try falling back
    availableMethod = null;
    throw new Error(res.data?.error?.message || 'tools/invoke 执行失败');
  }
  
  if (availableMethod === 'chat-completions') {
    const res = await axios.post(`${config.gatewayUrl}/v1/chat/completions`, {
      model: 'openclaw:main',
      messages: [{ role: 'user', content: prompt }],
    }, {
      headers: { Authorization: `Bearer ${config.gatewayToken}` },
      timeout: config.taskTimeoutMs + 10000,
    });
    
    const choice = res.data?.choices?.[0];
    if (choice?.message?.content) {
      return choice.message.content;
    }
    availableMethod = null;
    throw new Error('chat/completions 返回空响应');
  }
  
  if (availableMethod === 'cli') {
    // CLI fallback — 使用 execFileSync 避免 shell 注入
    const timeoutSec = Math.floor(config.taskTimeoutMs / 1000);
    let result: string;
    try {
      result = execFileSync(
        config.openclawPath,
        ['agent', '-m', prompt, '--timeout', String(timeoutSec), '--json'],
        { timeout: config.taskTimeoutMs + 10000, encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
      );
    } catch (cliErr: any) {
      // stderr 通常包含错误信息，提取其中有用部分
      const stderr = cliErr.stderr?.toString() || '';
      throw new Error(stderr.slice(0, 500) || cliErr.message);
    }
    
    try {
      const json = JSON.parse(result);
      return json.reply || json.content || json.text || result;
    } catch {
      return result.trim() || '(CLI 执行完成，无输出)';
    }
  }

  if (availableMethod === 'hub-execute') {
    const hubUrl = HUB_URL || persistedConfig.hubUrl || '';
    const res = await axios.post(`${hubUrl}/node/api/execute`, {
      taskId: 'node-exec',
      prompt,
      timeoutMs: config.taskTimeoutMs,
    }, { timeout: config.taskTimeoutMs + 30000 });

    if (res.data?.code === 0) {
      return typeof res.data.result === 'string'
        ? res.data.result
        : JSON.stringify(res.data.result);
    }
    availableMethod = null;
    throw new Error(res.data?.message || 'Hub 执行代理返回失败');
  }

  throw new Error('无可用执行方法');
}

// Main executor loop: pick pending tasks and run them
async function executorTick() {
  if (!executorConfig.enabled || !connected) return;
  
  // Memory safety check
  const memUsage = getMemoryUsage();
  const memPct = typeof memUsage === 'object' ? (memUsage as any).percentage : memUsage;
  if (memPct >= executorConfig.minMemoryPct) {
    addLog('warning', `⚠️ Executor: 内存过高 (${memPct}%)，暂停接取新任务`);
    return;
  }
  
  // Concurrency check
  if (activeTaskCount >= executorConfig.maxConcurrent) return;
  
  // Find pending/assigned tasks assigned to this node
  // Note: Hub sets status='assigned' after dispatch, so we check both pending and assigned
  const pendingTasks = syncedTasks.filter(t => 
    (t.status === 'pending' || t.status === 'assigned') && 
    !executingTaskIds.has(t.id)
  );
  
  if (pendingTasks.length === 0) return;
  
  // Sort by priority: high > medium > low
  const priorityOrder: Record<string, number> = { high: 3, medium: 2, low: 1 };
  pendingTasks.sort((a: any, b: any) => 
    (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0)
  );
  
  // Pick tasks up to concurrency limit
  const toExecute = pendingTasks.slice(0, executorConfig.maxConcurrent - activeTaskCount);
  
  for (const task of toExecute) {
    executeTask(task);  // Fire and forget, tracked via activeTaskCount
  }
}

// Execute a single task (async, tracks its own lifecycle)
async function executeTask(task: any) {
  const taskId = task.id;
  const title = task.title || task.userInput || '(无标题任务)';
  
  executingTaskIds.add(taskId);
  activeTaskCount++;
  addLog('info', `🚀 开始执行任务: ${title} (${taskId})`);
  
  try {
    // Report start to Hub
    await reportTaskAction(taskId, 'start');
    
    // Execute via best available method
    const result = await executeTaskContent(title, task.description || '');
    
    // Report success
    await reportTaskAction(taskId, 'complete', {
      result: { text: result.slice(0, 5000) },  // Truncate large results
    });
    addLog('info', `✅ 任务完成: ${title}`);
  } catch (err: any) {
    addLog('error', `❌ 任务失败: ${title} — ${err.message}`);
    // 🔐 上报失败添加重试机制（最多 3 次，指数退避）
    let retries = 0;
    const maxRetries = 3;
    while (retries < maxRetries) {
      try {
        await reportTaskAction(taskId, 'fail', {
          error: err.message?.slice(0, 1000),
        });
        break;  // 成功则退出重试循环
      } catch (reportErr) {
        retries++;
        console.error(`[Node][ERROR] 上报任务失败状态失败 (尝试 ${retries}/${maxRetries}):`, reportErr.message);
        if (retries >= maxRetries) {
          addLog('warn', `⚠️ 任务失败状态上报失败，已放弃重试`);
        } else {
          await new Promise(r => setTimeout(r, 1000 * Math.pow(2, retries)));  // 指数退避
        }
      }
    }
  } finally {
    executingTaskIds.delete(taskId);
    activeTaskCount--;
  }
}

// Start the executor (called after Hub connection is established)
async function startExecutor() {
  executorConfig = detectExecutorConfig();
  
  if (!executorConfig.enabled) {
    addLog('info', 'Task Executor: 已禁用 (TASK_EXECUTOR=false)');
    return;
  }
  
  // Probe available method
  availableMethod = await probeExecutionMethod();
  
  if (!availableMethod) {
    addLog('warning', 'Task Executor: 无可用执行方法，将在后续心跳中重试');
    // Still start the timer — will re-probe when a task arrives
  }
  
  // Start polling
  if (executorTimer) clearInterval(executorTimer);
  executorTimer = setInterval(executorTick, executorConfig.pollIntervalMs);
  executorRunning = true;
  
  addLog('info', `🤖 Task Executor 已启动 (最大并发: ${executorConfig.maxConcurrent}, 轮询: ${executorConfig.pollIntervalMs/1000}s, 内存上限: ${executorConfig.minMemoryPct}%)`);
}

function stopExecutor() {
  if (executorTimer) {
    clearInterval(executorTimer);
    executorTimer = null;
  }
  executorRunning = false;
}

// ─── Register Node API routes on a Fastify instance ──────────────
// This function registers all Node routes. Can be called on:
//   - The Hub's app with prefix '/node' (embedded mode)
//   - A standalone Fastify instance (standalone mode)
export function registerNodeRoutes(app: FastifyInstance) {

  // ═══ LOCAL READ/WRITE APIs ═══

  app.get('/api/status', async () => {
    const mem = getMemoryUsage();
    const disk = getDiskUsage();
    return {
      code: 0,
      data: {
        nodeId,
        nodeName: NODE_NAME,
        hubUrl: HUB_URL,
        appId: APP_ID,
        hubConnected: connected,
        connecting,
        connectionError,
        lastHeartbeat,
        registeredAt,
        system: { cpu: getCpuUsage(), memory: mem.percentage, disk: disk.percentage, uptime: os.uptime() },
        tasks: {
          pending: syncedTasks.filter(t => t.status === 'pending').length,
          running: syncedTasks.filter(t => t.status === 'running').length,
          completed: syncedTasks.filter(t => t.status === 'completed').length,
          failed: syncedTasks.filter(t => t.status === 'failed').length,
        },
        executor: {
          enabled: executorConfig?.enabled ?? false,
          running: executorRunning,
          method: availableMethod,
          activeTasks: activeTaskCount,
          maxConcurrent: executorConfig?.maxConcurrent ?? 0,
          memoryLimit: executorConfig?.minMemoryPct ?? 0,
        },
      }
    };
  });

  app.get('/api/monitor', async () => {
    return {
      code: 0,
      data: {
        cpu: getCpuUsage(),
        memory: getMemoryUsage(),
        disk: getDiskUsage(),
        system: getSystemInfo(),
        uptime: os.uptime(),
        timestamp: new Date().toISOString(),
      }
    };
  });

  // Memory (local CRUD)
  app.get('/api/memory', async (req) => {
    const { type, search } = req.query as any;
    let list = Array.from(localMemories.values());
    if (type) list = list.filter(m => m.type === type);
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(m => m.content.toLowerCase().includes(q) || m.tags.some((t: string) => t.toLowerCase().includes(q)));
    }
    list.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    return { code: 0, data: list, total: list.length };
  });

  // 🔐 安全修复: 输入验证
  const VALID_MEMORY_TYPES = ['stm', 'mtm', 'ltm'];
  const MAX_TAGS = 20;
  const MAX_TAG_LENGTH = 50;

  app.post('/api/memory', async (req) => {
    const { type, content, source, importance, tags } = req.body as any;
    if (!content) return { code: 400, message: '内容不能为空' };
    if (content.length > 10000) return { code: 400, message: '内容过长（最大 10000 字符）' };
    
    // 🔐 type 字段白名单验证
    const validType = type && VALID_MEMORY_TYPES.includes(type) ? type : 'stm';
    
    // 🔐 tags 数组验证
    let validTags: string[] = [];
    if (tags && Array.isArray(tags)) {
      validTags = tags.slice(0, MAX_TAGS).filter((t: any) => 
        typeof t === 'string' && t.length <= MAX_TAG_LENGTH
      );
    }
    
    const id = `mem-${memoryIdCounter++}`;
    const memory: Memory = {
      id, type: validType, content, source: source || 'manual',
      importance: importance || 5, tags: validTags,
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
    };
    localMemories.set(id, memory);
    return { code: 0, message: '记忆创建成功', data: memory };
  });

  app.put('/api/memory/:id', async (req) => {
    const id = (req.params as any).id;
    const memory = localMemories.get(id);
    if (!memory) return { code: 404, message: '记忆不存在' };
    const { type, content, importance, tags } = req.body as any;
    
    // 🔐 type 字段白名单验证
    if (type && VALID_MEMORY_TYPES.includes(type)) memory.type = type;
    if (content) {
      if (content.length > 10000) return { code: 400, message: '内容过长（最大 10000 字符）' };
      memory.content = content;
    }
    if (importance !== undefined) memory.importance = importance;
    if (tags && Array.isArray(tags)) {
      memory.tags = tags.slice(0, MAX_TAGS).filter((t: any) => 
        typeof t === 'string' && t.length <= MAX_TAG_LENGTH
      );
    }
    memory.updatedAt = new Date().toISOString();
    return { code: 0, message: '记忆更新成功', data: memory };
  });

  app.delete('/api/memory/:id', async (req) => {
    const id = (req.params as any).id;
    if (!localMemories.has(id)) return { code: 404, message: '记忆不存在' };
    localMemories.delete(id);
    return { code: 0, message: '记忆删除成功' };
  });

  // ═══ HUB-SYNCED READ-ONLY APIs ═══

  app.get('/api/tasks', async () => {
    return { code: 0, data: syncedTasks, total: syncedTasks.length };
  });

  app.post('/api/tasks/:id/start', async (req) => {
    try {
      const result = await reportTaskAction((req.params as any).id, 'start', { nodeId });
      return { code: 0, message: '任务已开始', data: result.data };
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  app.post('/api/tasks/:id/complete', async (req) => {
    try {
      const result = await reportTaskAction((req.params as any).id, 'complete', (req.body as any) || {});
      return { code: 0, message: '任务已完成', data: result.data };
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  app.post('/api/tasks/:id/fail', async (req) => {
    try {
      const result = await reportTaskAction((req.params as any).id, 'fail', { error: (req.body as any)?.error || '手动标记失败' });
      return { code: 0, message: '任务已标记失败', data: result.data };
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  app.get('/api/skills', async () => {
    return { code: 0, data: syncedSkills, total: syncedSkills.length };
  });

  // ═══ CONNECTION MANAGEMENT ═══

  app.get('/api/connection', async () => {
    return {
      code: 0,
      data: {
        hubUrl: HUB_URL,
        appId: APP_ID,
        nodeId,
        sessionToken: '***HIDDEN***',  // 🔐 完全隐藏 token
        connected,
        connecting,
        connectionError,
        lastHeartbeat,
        registeredAt,
        logs: connectionLogs.slice(0, 50),
      }
    };
  });

  app.post('/api/connection/reconnect', async () => {
    clearTimers();
    connected = false;
    connecting = false;
    nodeId = '';
    sessionToken = '';
    addLog('info', '手动触发重连...');
    const ok = await registerWithHub();
    return { code: 0, message: ok ? '重连成功' : '重连失败', data: { connected: ok } };
  });

  app.get('/health', async () => {
    return {
      status: 'ok',
      nodeId,
      nodeName: NODE_NAME,
      hubUrl: HUB_URL,
      connected,
      uptime: Math.round((Date.now() - startTime) / 1000),
      version: NODE_VERSION,
      timestamp: new Date().toISOString(),
    };
  });

  app.get('/api/health', async () => {
    return {
      status: 'ok',
      nodeId,
      nodeName: NODE_NAME,
      hubUrl: HUB_URL,
      connected,
      uptime: Math.round((Date.now() - startTime) / 1000),
      version: NODE_VERSION,
      timestamp: new Date().toISOString(),
    };
  });

  // ═══ AGENT MANAGEMENT ═══

  app.post('/api/agents', async (req) => {
    const { name, role, soulMd, capabilities, skills } = req.body as any;
    if (!name) return { code: 400, message: 'Agent 名称不能为空' };

    // 同时注册到 Hub
    if (sessionToken && nodeId) {
      try {
        const res = await axios.post(`${resolvedHubUrl()}/api/nodes/${nodeId}/agents/register`, {
          name, role, soulMd, capabilities, skills,
        }, {
          headers: { Authorization: `Bearer ${sessionToken}` },
          timeout: 10000,
        });
        return res.data;
      } catch (err: any) {
        return { code: 500, message: `注册到 Hub 失败: ${err.message}` };
      }
    }

    return { code: 503, message: '未连接到 Hub' };
  });

  app.get('/api/agents', async () => {
    if (!sessionToken || !nodeId) return { code: 503, message: '未连接到 Hub' };
    try {
      const res = await axios.get(`${resolvedHubUrl()}/api/nodes/${nodeId}/agents`, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // ============ Collaboration API (proxy to Hub) ============

  // Get messages for this node's agent
  app.get('/api/collaborations/messages', async () => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const res = await axios.get(`${resolvedHubUrl()}/api/collaborations/messages/agent-local?nodeId=${nodeId}`, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Send message via Hub
  app.post('/api/collaborations/messages', async (req) => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const body = req.body as any;
      body.fromNodeId = nodeId;
      const res = await axios.post(`${resolvedHubUrl()}/api/collaborations/messages`, body, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Mark message as read
  app.put('/api/collaborations/messages/:id/read', async (req) => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const { id } = req.params as any;
      const res = await axios.put(`${resolvedHubUrl()}/api/collaborations/messages/${id}/read`, {}, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Get collaboration tasks
  app.get('/api/collaborations/tasks', async () => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const res = await axios.get(`${resolvedHubUrl()}/api/collaborations/tasks`, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Get task details
  app.get('/api/collaborations/tasks/:taskId', async (req) => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const { taskId } = req.params as any;
      const res = await axios.get(`${resolvedHubUrl()}/api/collaborations/tasks/${taskId}`, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Update sub-task status
  app.put('/api/collaborations/subtasks/:subId/status', async (req) => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const { subId } = req.params as any;
      const res = await axios.put(`${resolvedHubUrl()}/api/collaborations/subtasks/${subId}/status`, req.body, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  // Get/Set shared state
  app.get('/api/collaborations/state', async () => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const res = await axios.get(`${resolvedHubUrl()}/api/collaborations/state`, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });

  app.put('/api/collaborations/state/:key', async (req) => {
    if (!sessionToken) return { code: 503, message: '未连接到 Hub' };
    try {
      const { key } = req.params as any;
      const res = await axios.put(`${resolvedHubUrl()}/api/collaborations/state/${key}`, req.body, {
        headers: { Authorization: `Bearer ${sessionToken}` },
        timeout: 10000,
      });
      return res.data;
    } catch (err: any) {
      return { code: 500, message: err.message };
    }
  });
}

// Export for Hub to call
export { registerWithHub };

// ─── Standalone Mode ─────────────────────────────────────────────
// When run directly (not imported by Hub), start its own Fastify server
async function startStandalone() {
  // Ensure DATA_DIR exists
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    addLog('info', `已创建数据目录: ${DATA_DIR}`);
  }

  const app = Fastify({ logger: true });
  // CORS: 限制来源，生产环境默认只允许 Hub 所在域名
  const allowedOrigins = process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',').map(s => s.trim())
    : HUB_URL ? [new URL(HUB_URL).origin] : [];
  await app.register(cors, {
    origin: allowedOrigins.length > 0 ? allowedOrigins : false,
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
  });

  const frontendDist = path.join(__dirname, '../../frontend/dist');
  if (fs.existsSync(frontendDist)) {
    await app.register(fastifyStatic, { root: frontendDist, prefix: '/', decorateReply: false });
  }

  // Register all node API routes
  registerNodeRoutes(app);

  // SPA fallback
  app.setNotFoundHandler(async (request, reply) => {
    if (request.url.startsWith('/api/') || request.url === '/health') {
      reply.code(404);
      return { code: 404, message: 'Not Found' };
    }
    const indexPath = path.join(frontendDist, 'index.html');
    if (fs.existsSync(indexPath)) {
      return reply.type('text/html').send(fs.readFileSync(indexPath));
    }
    reply.code(404);
    return { code: 404, message: '前端未构建' };
  });

  await app.listen({ port: NODE_PORT, host: '0.0.0.0' });
  addLog('info', `子节点服务已启动 (standalone): http://0.0.0.0:${NODE_PORT}`);
  addLog('info', `节点名称: ${NODE_NAME} | Hub: ${HUB_URL || '未配置'} | 数据目录: ${DATA_DIR}`);
  await registerWithHub();
}

// Auto-start standalone if this is the main module
const isMain = process.argv[1]?.includes('node/server');
if (isMain) {
  startStandalone().catch((err) => {
    console.error('[Node] 启动失败:', err);
    process.exit(1);
  });
}
