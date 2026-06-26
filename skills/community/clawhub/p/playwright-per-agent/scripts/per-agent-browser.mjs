// per-agent-browser.mjs
// Per-agent isolated Playwright browser pool.
//
// 三种 profile 模式:
//   - shared      : 所有 agent 共享一个 chrome 实例（节省资源，登录态共享）
//   - per-agent   : 每个 agent 独立 chrome（隔离 cookies/storage/CDP 端口/进程）
//   - ephemeral   : 一次性，关闭后 profile 目录删除（不保留任何状态）
//
// Subagent 支持:
//   - inherit: true  → 继承父 agent 的 chrome 实例
//   - inherit: false → 独立 subagent 实例
//   - 不指定 → 默认 inherit（避免资源浪费）
//
// 扩展性:
//   - 自动从 ~/.openclaw/openclaw.json 读 agents.list
//   - 动态 registerAgent(name, meta) 支持运行时新增 agent
//
// 跨进程 attach:
//   - /tmp/agent-browser-registry.json 持久化 port+profileDir
//   - 不同进程可 connectOverCDP attach 到已存在的实例
//
// 用法:
//   import { AgentBrowser } from './per-agent-browser.mjs';
//
//   const ab = new AgentBrowser({ mode: 'per-agent' });
//   const { page, profileDir, cdpPort } = await ab.getBrowser('agent-a');
//   await page.goto('https://example.com');
//   await ab.closeAll();

import { chromium } from 'playwright';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join, dirname, resolve } from 'node:path';
import { homedir } from 'node:os';

const DEFAULT_CHROME_PATHS = [
  // user-local playwright cache
  `${process.env.HOME || '/root'}/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`,
  `${process.env.HOME || '/root'}/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome`,
  // system browsers
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  // macOS
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
];
const BASE_PORT = parseInt(process.env.AGENT_BROWSER_BASE_PORT || '19300', 10);
const MAX_PORT = parseInt(process.env.AGENT_BROWSER_MAX_PORT || '19999', 10);
const PROFILE_ROOT = process.env.AGENT_BROWSER_ROOT || join(homedir(), '.cache', 'agent-browser');
const REGISTRY = process.env.AGENT_BROWSER_REGISTRY || '/tmp/agent-browser-registry.json';
const DEFAULT_CHROMIUM_ARGS = [
  '--no-sandbox',
  '--disable-dev-shm-usage',
  '--use-gl=angle',
  '--use-angle=gl',
  '--enable-unsafe-swiftshader',
  '--use-vulkan=swiftshader',
  '--enable-features=Vulkan',
];

function findChrome() {
  for (const p of DEFAULT_CHROME_PATHS) if (existsSync(p)) return p;
  throw new Error(`No Chrome/Chromium executable found. Searched: ${DEFAULT_CHROME_PATHS.join(', ')}. Set chromePath option or AGENT_BROWSER_CHROME env var.`);
}

function findOpenclawConfig() {
  const candidates = [
    process.env.OPENCLAW_CONFIG,
    join(homedir(), '.openclaw', 'openclaw.json'),
    '/root/.openclaw/openclaw.json',
  ].filter(Boolean);
  for (const c of candidates) if (existsSync(c)) return c;
  return null;
}

function loadOpenclawAgents() {
  const cfgPath = findOpenclawConfig();
  if (!cfgPath) return [];
  try {
    const cfg = JSON.parse(readFileSync(cfgPath, 'utf8'));
    const list = cfg?.agents?.list || [];
    return list.filter(a => a && typeof a === 'object' && a.id).map(a => ({
      id: a.id,
      workspace: a.workspace,
      role: a.role,
    }));
  } catch {
    return [];
  }
}

function hashAgentId(agentId) {
  return parseInt(
    createHash('sha256').update(String(agentId)).digest('hex').slice(0, 8),
    16
  );
}

function isPortInUse(port) {
  try {
    const r = execSync(
      `(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null) | grep -E ":${port} " || true`,
      { encoding: 'utf8' }
    );
    return r.trim().length > 0;
  } catch {
    return false;
  }
}

function pickPort(agentId, usedPorts = new Set()) {
  const preferred = BASE_PORT + (hashAgentId(agentId) % (MAX_PORT - BASE_PORT));
  for (let p = preferred; p < MAX_PORT; p++) {
    if (!isPortInUse(p) && !usedPorts.has(p)) return p;
  }
  for (let p = BASE_PORT; p < preferred; p++) {
    if (!isPortInUse(p) && !usedPorts.has(p)) return p;
  }
  throw new Error('No free port for agent browser');
}

function ensureProfileDir(agentId, root = PROFILE_ROOT) {
  const safe = String(agentId).replace(/[^a-zA-Z0-9._-]/g, '_');
  const dir = join(root, safe);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  return dir;
}

function loadRegistry() {
  try {
    if (existsSync(REGISTRY)) return JSON.parse(readFileSync(REGISTRY, 'utf8'));
  } catch {}
  return {};
}

function saveRegistry(reg) {
  writeFileSync(REGISTRY, JSON.stringify(reg, null, 2));
}

function parseAgentId(id) {
  // 'agent-a'                → { agent: 'agent-a', sub: null }
  // 'agent-a:sub-1'          → { agent: 'agent-a', sub: 'sub-1' }
  // 'agent-a.sub-1'          → { agent: 'agent-a', sub: 'sub-1' }  (alt separator)
  const idx = id.indexOf(':');
  if (idx < 0) return { agent: id, sub: null };
  return { agent: id.slice(0, idx), sub: id.slice(idx + 1) };
}

/**
 * AgentBrowser — main class
 * @param {object} options
 * @param {'shared' | 'per-agent' | 'ephemeral'} options.mode - profile mode
 * @param {string} [options.chromePath] - override Chrome path
 * @param {string[]} [options.extraArgs] - extra Chrome flags
 * @param {string} [options.defaultAgent] - default agent id when caller passes 'self' or 'current'
 * @param {boolean} [options.headless=true]
 * @param {object} [options.viewport] - default { width, height }
 * @param {boolean} [options.subagentInherit=true] - if subagent, inherit parent by default
 * @param {boolean} [options.cleanupOnExit=false] - auto cleanup ephemeral on process exit
 */
export class AgentBrowser {
  constructor(options = {}) {
    this.mode = options.mode || 'per-agent';
    this.chromePath = options.chromePath || findChrome();
    this.extraArgs = options.extraArgs || [];
    this.defaultAgent = options.defaultAgent || 'shared';
    this.headless = options.headless !== false;
    this.viewport = options.viewport || { width: 1280, height: 720 };
    this.subagentInherit = options.subagentInherit !== false;
    this.cleanupOnExit = options.cleanupOnExit === true;

    // live instances: agentId → { ctx, page, ... }
    this.liveInstances = new Map();
    // registered agents: agentId → { id, workspace, role, ... }
    this.registeredAgents = new Map();
    // known openclaw agents
    for (const a of loadOpenclawAgents()) {
      this.registeredAgents.set(a.id, a);
    }
    // shared mode special agent
    if (this.mode === 'shared') {
      this.registeredAgents.set(this.defaultAgent, { id: this.defaultAgent, role: 'shared' });
    }

    if (this.cleanupOnExit) {
      process.on('exit', () => { try { this.closeAllSync(); } catch {} });
    }
  }

  /** Register a new agent at runtime (extensibility) */
  registerAgent(id, meta = {}) {
    if (!id) throw new Error('agent id required');
    this.registeredAgents.set(String(id), { id: String(id), ...meta });
  }

  /** List all known agent ids */
  listAgents() {
    return Array.from(this.registeredAgents.keys());
  }

  /** List currently active (live) browser instances */
  listActive() {
    return Array.from(this.liveInstances.keys());
  }

  /**
   * Get a browser page for an agent.
   * @param {string} agentId - 'agent-a' / 'agent-b' / 'agent-a:sub-1' / 'shared' / 'ephemeral-xxx'
   * @param {object} [opts]
   * @param {boolean} [opts.inherit] - subagent only: inherit from parent? default subagentInherit
   * @param {boolean} [opts.headless] - override
   * @param {object} [opts.viewport] - override
   * @returns {Promise<{ctx, page, profileDir, cdpPort, agentId, mode, parent?}>}
   */
  async getBrowser(agentId, opts = {}) {
    const id = String(agentId || this.defaultAgent);
    const parsed = parseAgentId(id);
    const isSub = parsed.sub !== null;

    // subagent logic
    if (isSub) {
      const inherit = opts.inherit !== undefined ? opts.inherit : this.subagentInherit;
      if (inherit) {
        // attach to parent's instance
        const parent = await this.getBrowser(parsed.agent, { ...opts, inherit: false });
        // open a new tab in parent's context (NOT new context — share state)
        const page = await parent.ctx.newPage();
        return {
          ctx: parent.ctx,
          page,
          profileDir: parent.profileDir,
          cdpPort: parent.cdpPort,
          agentId: id,
          mode: 'subagent-inherited',
          parent: parsed.agent,
        };
      }
      // non-inherit subagent: build a new subagent-specific profile
      // fall through to normal flow with subagent-suffixed id
    }

    // cached live instance?
    if (this.liveInstances.has(id)) {
      const inst = this.liveInstances.get(id);
      try {
        if (inst.ctx && (await inst.ctx.pages()).length >= 0) {
          // for shared/per-agent: reuse page; caller can use newPage() if they want isolation
          return inst;
        }
      } catch {}
      this.liveInstances.delete(id);
    }

    // ephemeral: fresh profile, will be deleted on close
    if (this.mode === 'ephemeral') {
      return await this._launchEphemeral(id, opts);
    }

    // shared: all "agents" route to one instance
    if (this.mode === 'shared') {
      const sharedId = '__shared__';
      if (this.liveInstances.has(sharedId)) return this.liveInstances.get(sharedId);
      return await this._launchPerAgent(sharedId, opts, true);
    }

    // per-agent
    return await this._launchPerAgent(id, opts, false);
  }

  async _launchPerAgent(id, opts, isShared = false) {
    const cdpPort = pickPort(id, new Set());
    const profileDir = ensureProfileDir(id);
    const headless = opts.headless !== undefined ? opts.headless : this.headless;
    const args = [
      ...DEFAULT_CHROMIUM_ARGS,
      `--remote-debugging-port=${cdpPort}`,
      ...this.extraArgs,
    ];

    console.log(`[agent-browser] launching ${isShared ? 'shared' : 'per-agent'}: ${id} → port ${cdpPort}, profile ${profileDir}`);
    const ctx = await chromium.launchPersistentContext(profileDir, {
      executablePath: this.chromePath,
      headless,
      args,
      viewport: opts.viewport || this.viewport,
    });
    const page = ctx.pages()[0] || await ctx.newPage();

    const inst = {
      ctx, page, agentId: id,
      profileDir, cdpPort,
      mode: isShared ? 'shared' : 'per-agent',
    };
    this.liveInstances.set(id, inst);

    // registry
    const reg = loadRegistry();
    reg[id] = { port: cdpPort, profileDir, startedAt: new Date().toISOString(), mode: isShared ? 'shared' : 'per-agent' };
    saveRegistry(reg);

    return inst;
  }

  async _launchEphemeral(id, opts) {
    const cdpPort = pickPort(id, new Set());
    // unique profile under ephemeral/, named with timestamp+random
    const stamp = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const profileDir = join(PROFILE_ROOT, 'ephemeral', `${id}-${stamp}`);
    mkdirSync(profileDir, { recursive: true });
    const headless = opts.headless !== undefined ? opts.headless : this.headless;
    const args = [
      ...DEFAULT_CHROMIUM_ARGS,
      `--remote-debugging-port=${cdpPort}`,
      ...this.extraArgs,
    ];
    console.log(`[agent-browser] launching ephemeral: ${id} → port ${cdpPort}, profile ${profileDir} (will be deleted on close)`);
    const ctx = await chromium.launchPersistentContext(profileDir, {
      executablePath: this.chromePath,
      headless,
      args,
      viewport: opts.viewport || this.viewport,
    });
    const page = ctx.pages()[0] || await ctx.newPage();

    const inst = {
      ctx, page, agentId: id,
      profileDir, cdpPort,
      mode: 'ephemeral',
      _ephemeral: true,
    };
    this.liveInstances.set(id, inst);
    return inst;
  }

  /** Close one agent's browser (or subagent's page) */
  async close(agentId) {
    const id = String(agentId);
    const inst = this.liveInstances.get(id);
    if (!inst) return;
    try {
      if (inst._ephemeral) {
        // close + delete profile dir
        await inst.ctx.close();
        if (existsSync(inst.profileDir)) {
          rmSync(inst.profileDir, { recursive: true, force: true });
          console.log(`[agent-browser] ephemeral profile deleted: ${inst.profileDir}`);
        }
      } else if (inst.mode === 'subagent-inherited') {
        // only close the page, parent stays
        try { await inst.page.close(); } catch {}
      } else {
        await inst.ctx.close();
        const reg = loadRegistry();
        delete reg[id];
        saveRegistry(reg);
      }
    } catch (e) {
      console.warn(`[agent-browser] close ${id} error:`, e.message);
    }
    this.liveInstances.delete(id);
    console.log(`[agent-browser] closed ${id}`);
  }

  /** Close all live instances */
  async closeAll() {
    const ids = Array.from(this.liveInstances.keys());
    for (const id of ids) await this.close(id);
  }

  /** Sync close for process.exit handler (best-effort) */
  closeAllSync() {
    for (const [, inst] of this.liveInstances) {
      try { inst.ctx.close(); } catch {}
    }
  }

  /** List active agents via registry (cross-process) */
  static listActiveFromRegistry() {
    return Object.keys(loadRegistry());
  }
}

// ===== CLI demo =====
if (import.meta.url === `file://${process.argv[1]}`) {
  const cmd = process.argv[2] || 'demo';
  if (cmd === 'list') {
    console.log('active agents:', AgentBrowser.listActiveFromRegistry());
  } else if (cmd === 'agents') {
    const ab = new AgentBrowser({ mode: 'per-agent' });
    console.log('known agents:', ab.listAgents());
  } else if (cmd === 'close-all') {
    const ab = new AgentBrowser({ mode: 'per-agent' });
    await ab.closeAll();
  } else if (cmd === 'demo') {
    const mode = process.argv[3] || 'per-agent';
    const agentId = process.argv[4] || 'demo-agent';
    const ab = new AgentBrowser({ mode });
    const { page, profileDir, cdpPort } = await ab.getBrowser(agentId, { headless: false });
    console.log(`agent ${agentId} (mode=${mode}) → profile ${profileDir}, port ${cdpPort}`);
    await page.goto('https://example.com');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: `/tmp/agent-${agentId}.png` });
    console.log('screenshot saved');
  }
}
