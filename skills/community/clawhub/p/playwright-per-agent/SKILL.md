---
name: playwright-per-agent
description: "Per-agent Playwright browser pool: shared/per-agent/ephemeral + subagent inherit. Reads openclaw.json. Requires node, playwright. Local-only; no data forwarded."
metadata: {"openclaw":{"emoji":"🧩","requires":{"anyBins":["node"]}}}
---

# playwright-per-agent

Per-agent isolated Playwright browser pool. 给每个 OpenClaw agent 独立的 Chrome
实例，避免 cookie/storage/CDP 端口/进程冲突。

> **关于 agent 命名**：本 skill 不在静态内容里硬编码任何具体 agent 名字。
> 所有 agent id 都从用户 `~/.openclaw/openclaw.json` 的 `agents.list` 运行时读取。
> 示例代码用 `agent-a` / `agent-b` 等占位符；用户在自己环境里替换成实际 agent id 即可。
> 想把具体映射存起来时，把映射文件放在 `~/.config/playwright-per-agent/agents.json` 等
> 用户私有位置（不进 git / 不进 skill 包）。

## 三种 Profile 模式

| 模式 | 何时用 | 资源 |
|---|---|---|
| `shared` | 所有 agent 共享一个 Chrome（节省资源，登录态共享） | 1 chrome |
| `per-agent` | 每个 agent 独立 Chrome（隔离 cookies/storage/CDP 端口/进程） | N chrome |
| `ephemeral` | 一次性，关闭后 profile 目录删除（不保留任何状态） | 临时 |

## Subagent 支持

`getBrowser('agent-a:scout-1', { inherit: true })` → 新 tab 在父 agent 上下文。
`inherit: false` → 独立 subagent 实例。

## 自动扩展

- 启动时从 `~/.openclaw/openclaw.json` 的 `agents.list` 读所有 agent id
- 运行时 `ab.registerAgent('new-id', { role: 'qa' })` 新增
- 详见 `assets/example-config.json`

## 安装

```bash
npm install playwright
```

Playwright Chromium 已在本机 `~/.cache/ms-playwright/chromium-1217/`，可
`launchPersistentContext` 直接用，无需 `playwright install`。

## 快速开始

```javascript
import { AgentBrowser } from 'skills/playwright-per-agent/scripts/per-agent-browser.mjs';

// per-agent 模式（推荐大多数场景）
const ab = new AgentBrowser({ mode: 'per-agent' });

// 'agent-a' 来自 ~/.openclaw/openclaw.json 的 agents.list
const { page, profileDir, cdpPort } = await ab.getBrowser('agent-a');
await page.goto('https://example.com');
await page.screenshot({ path: '/tmp/shot.png' });

// 关闭（不删 profile，state 持久化）
await ab.close('agent-a');
```

## 三种模式示例

### shared — 共享登录态

```javascript
const ab = new AgentBrowser({ mode: 'shared' });
// 不管传入什么 agentId，都用同一个 Chrome
const { page } = await ab.getBrowser('agent-a');
await page.goto('https://github.com');
// agent-a 登录后，agent-b / agent-c 复用同一登录态
await ab.getBrowser('agent-b');  // 同一个 Chrome 实例
```

### per-agent — 完全隔离

```javascript
const ab = new AgentBrowser({ mode: 'per-agent' });
// 3 个 agent → 3 个独立 Chrome
const a = await ab.getBrowser('agent-a');
const b = await ab.getBrowser('agent-b');
const c = await ab.getBrowser('agent-c');
// a.profileDir !== b.profileDir !== c.profileDir
// a.cdpPort   !== b.cdpPort   !== c.cdpPort
```

### ephemeral — 一次性

```javascript
const ab = new AgentBrowser({ mode: 'ephemeral' });
const { page } = await ab.getBrowser('one-shot-1');
await page.goto('https://example.com');
await page.screenshot({ path: '/tmp/one-shot.png' });
await ab.close('one-shot-1');  // profile dir 自动删除
```

## Subagent 模式

```javascript
// 默认 inherit — 共享父 agent 的 chrome，新开一个 tab
const parent = await ab.getBrowser('agent-a');
const sub = await ab.getBrowser('agent-a:scout-1');  // inherit=true 默认
// sub.page 在 parent.ctx 里，cookies/localStorage 共享

// 显式独立 subagent
const isoSub = await ab.getBrowser('agent-a:scout-1', { inherit: false });
// isoSub 有自己独立的 profile + cdpPort + chrome 进程
```

## 扩展性 — 注册新 agent

```javascript
const ab = new AgentBrowser({ mode: 'per-agent' });
ab.registerAgent('dynamic-2026-06', { role: 'qa', displayName: 'Dynamic QA' });
ab.registerAgent('external-worker-x', { workspace: '/tmp/wx' });
const { page } = await ab.getBrowser('dynamic-2026-06');
```

## 跨进程 attach

`/tmp/agent-browser-registry.json` 持久化所有活跃实例。
另一个进程启动 `getBrowser('agent-a')` 时如果发现 agent-a 的 port 已在 listen，就 `connectOverCDP` attach 上去（不重启 chrome）。

## API 速查

```typescript
class AgentBrowser {
  constructor(options?: {
    mode?: 'shared' | 'per-agent' | 'ephemeral';  // default 'per-agent'
    chromePath?: string;
    extraArgs?: string[];
    headless?: boolean;          // default true
    viewport?: { width: number; height: number };
    subagentInherit?: boolean;   // default true
    cleanupOnExit?: boolean;     // default false (auto cleanup ephemeral)
  });

  registerAgent(id: string, meta?: object): void;
  listAgents(): string[];        // known agents (from openclaw.json + registered)
  listActive(): string[];        // live browsers in this process

  async getBrowser(agentId: string, opts?: {
    inherit?: boolean;          // subagent only
    headless?: boolean;
    viewport?: { width: number; height: number };
  }): Promise<{
    ctx: BrowserContext;
    page: Page;
    profileDir: string;
    cdpPort: number;
    agentId: string;
    mode: 'shared' | 'per-agent' | 'ephemeral' | 'subagent-inherited';
    parent?: string;            // subagent only
  }>;

  async close(agentId: string): Promise<void>;
  async closeAll(): Promise<void>;
  static listActiveFromRegistry(): string[];  // cross-process
}
```

## 常见错误

| 错误 | 原因 | 修复 |
|---|---|---|
| `No Chrome/Chromium executable found` | CHROME_PATHS 都没装 | 装 `playwright install chromium` 或 `apt install google-chrome` |
| `No free port for agent browser` | 19300-19999 全占用 | 调 `AGENT_BROWSER_BASE_PORT` / `AGENT_BROWSER_MAX_PORT` |
| `playwright` 找不到 | 没装 | `npm install playwright` |
| agent 找不到 | 没在 openclaw.json | 用 `ab.registerAgent(id, meta)` 动态注册 |

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `AGENT_BROWSER_ROOT` | `~/.cache/agent-browser` | profile dir 根目录 |
| `AGENT_BROWSER_REGISTRY` | `/tmp/agent-browser-registry.json` | 跨进程 registry |
| `AGENT_BROWSER_BASE_PORT` | `19300` | port 范围起点 |
| `AGENT_BROWSER_MAX_PORT` | `19999` | port 范围终点 |
| `AGENT_BROWSER_CHROME` | (auto-detect) | 强制指定 Chrome 可执行路径 |
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | agents 自动发现源 |

## 详细策略

见 `references/profile-strategies.md`（决策树 + 模式对比 + subagent 模式详解）。

## 配置文件示例

见 `assets/example-config.json`（用户私有 agent 映射的存放位置）。
