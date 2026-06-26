# 工具系统参考

## 工具策略
```json5
tools: {
  policy: "full",              // full|allowlist|deny
  allow: ["group:fs", "browser"],  // allowlist模式
  deny: ["browser"],           // deny优先于allow
  profile: "full",             // minimal|coding|messaging|full
  elevated: { mode: "on" }    // on|off|ask
}
```

### 工具配置文件
| 配置文件 | 包含工具 |
|----------|----------|
| `minimal` | session_status |
| `coding` | group:fs, group:runtime, group:sessions, group:memory, image |
| `messaging` | group:messaging, sessions_list/history/send, session_status |
| `full` | 无限制 |

### 工具组 (简写)
| 组 | 展开为 |
|----|--------|
| `group:runtime` | exec, bash, process |
| `group:fs` | read, write, edit, apply_patch |
| `group:sessions` | sessions_list/history/send/spawn, session_status |
| `group:memory` | memory_search, memory_get |
| `group:web` | web_search, web_fetch |
| `group:ui` | browser, canvas |
| `group:automation` | cron, gateway |
| `group:messaging` | message |
| `group:nodes` | nodes |

### 按提供商限制
```json5
tools: {
  profile: "coding",
  byProvider: {
    "google-antigravity": { profile: "minimal" }
  }
}
```

## exec 工具
```json5
// 配置
tools: {
  exec: {
    host: "sandbox",           // sandbox|gateway|node
    security: "allowlist",     // deny|allowlist|full
    ask: "on-miss",            // off|on-miss|always
    node: "mac-1",             // 默认节点
    notifyOnExit: true,
    pathPrepend: ["~/bin"],
    applyPatch: { enabled: false }
  }
}
```

### 参数
| 参数 | 说明 |
|------|------|
| `command` | 必填，shell命令 |
| `workdir` | 工作目录 |
| `yieldMs` | 自动后台化延迟(默认10000ms) |
| `background` | 立即后台运行 |
| `timeout` | 超时秒数(默认1800) |
| `pty` | 伪终端(TTY CLI用) |
| `host` | sandbox/gateway/node |
| `elevated` | 提升权限(沙箱→主机) |

### 会话覆盖
```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

## browser 工具
```json5
browser: {
  enabled: true,
  headless: true,
  defaultProfile: "chrome",
  executablePath: "/path/to/chrome",
  defaultViewport: { width: 1280, height: 720 },
  idleTimeoutMs: 300000
}
```

操作: status, start, stop, tabs, open, focus, close, snapshot, screenshot, act, navigate, console, pdf, upload, dialog, profiles, create-profile, delete-profile

## 子智能体 (Subagents)

### 配置
```json5
agents: { defaults: {
  subagents: {
    model: "provider/model",     // 子智能体默认模型
    maxConcurrent: 8,            // 最大并发
    archiveAfterMinutes: 60      // 自动归档
  }
}}
```

### sessions_spawn 参数
| 参数 | 说明 |
|------|------|
| `task` | 必填，任务描述 |
| `label` | 可选标签 |
| `agentId` | 可选，指定智能体 |
| `model` | 可选模型覆盖 |
| `thinking` | 可选思考级别 |
| `runTimeoutSeconds` | 超时(0=无限) |
| `cleanup` | delete/keep(默认keep) |

### 行为
- 非阻塞，立即返回 runId
- 完成后自动通告到请求者聊天
- 子智能体不能生成子智能体
- 默认无会话工具(sessions_*)
- 仅注入 AGENTS.md + TOOLS.md

### 斜杠命令
```
/subagents list|kill <id>|log <id>|info <id>|send <id> <msg>|steer <id> <msg>
/subagents spawn <agentId> <task> [--model <model>]
```

### 工具策略
```json5
tools: { subagents: { tools: {
  deny: ["gateway", "cron"],
  // allow: ["read", "exec"]  // 设置后变为仅允许模式
}}}
```

## Skills 系统

### 加载位置 (优先级从高到低)
1. `<workspace>/skills/` — 工作区级
2. `~/.openclaw/skills/` — 用户级
3. 内置 Skills — 随安装包

### SKILL.md 格式
```yaml
---
name: my-skill
description: "描述"
metadata:
  openclaw:
    requires:
      bins: ["uv"]
      env: ["API_KEY"]
      config: ["browser.enabled"]
    primaryEnv: "API_KEY"
---
```

### 配置
```json5
skills: {
  entries: {
    "my-skill": {
      enabled: true,
      apiKey: "KEY",
      env: { API_KEY: "KEY" }
    }
  },
  load: {
    extraDirs: ["/path/to/skills"],
    watch: true
  },
  allowBundled: ["skill1", "skill2"]  // 内置白名单
}
```

### ClawHub (公共注册表)
```bash
clawhub install <skill-slug>
clawhub update --all
clawhub sync --all
```

## 插件系统
```bash
openclaw plugins list [--json]
openclaw plugins install <path|npm-spec>
openclaw plugins enable <name>
openclaw plugins disable <name>
openclaw plugins doctor
```

插件可提供: 工具、Skills、Hooks、渠道、CLI命令

## 浏览器详细配置

### 配置文件模式
- `chrome`: 扩展中继到系统浏览器(默认)
- `openclaw`: 托管隔离浏览器(推荐)

### 完整配置
```json5
browser: {
  enabled: true,
  headless: false,
  noSandbox: false,
  attachOnly: false,                    // 仅附加已运行的浏览器
  defaultProfile: "openclaw",           // chrome|openclaw|自定义
  executablePath: "/path/to/chrome",    // 覆盖自动检测
  color: "#FF4500",
  remoteCdpTimeoutMs: 1500,
  remoteCdpHandshakeTimeoutMs: 3000,
  profiles: {
    openclaw: { cdpPort: 18800, color: "#FF4500" },
    work: { cdpPort: 18801, color: "#0066CC" },
    remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" }
  }
}
```

### 端口派生
- 浏览器控制: gateway.port + 2 (默认18791)
- 中继: gateway.port + 3 (默认18792)
- Canvas: gateway.port + 4 (默认18793)

### 自动检测顺序
系统默认(Chromium系) → Chrome → Brave → Edge → Chromium → Chrome Canary

### CLI
```bash
openclaw browser status|start|stop
openclaw browser --browser-profile openclaw start
openclaw browser tabs|open <url>|focus <id>|close <id>
openclaw browser screenshot [--selector .class]
openclaw browser snapshot [--refs aria]
openclaw browser navigate <url>
openclaw browser profiles|create-profile <name>|delete-profile <name>
openclaw browser reset-profile [--profile openclaw]
```

## Exec 审批详解

### 存储
`~/.openclaw/exec-approvals.json`

### 策略
| 字段 | 选项 | 说明 |
|------|------|------|
| `security` | deny/allowlist/full | 执行策略 |
| `ask` | off/on-miss/always | 提示策略 |
| `askFallback` | deny/allowlist/full | UI不可用时的回退 |
| `autoAllowSkills` | bool | 自动允许Skill引用的CLI |

### 允许列表模式
```json
{ "pattern": "~/Projects/**/bin/rg", "lastUsedAt": 1737150000000 }
```
- 按智能体隔离
- 模式匹配不区分大小写
- 必须是二进制路径(非基本名称)

### 安全二进制 (safeBins)
默认: jq, grep, cut, sort, uniq, head, tail, tr, wc
仅限stdin操作，无需显式白名单。

### 审批流程
1. exec返回 `status: "approval-pending"` + 审批id
2. Control UI/macOS应用显示确认对话框
3. Allow once / Always allow / Deny
4. 系统事件: `Exec finished` / `Exec denied`

### 审批转发到聊天
```json5
approvals: { exec: {
  enabled: true,
  mode: "session",  // session|targets|both
  targets: [{ channel: "telegram", to: "123456789" }]
}}
```
聊天中: `/approve <id> allow-once|allow-always|deny`

### CLI
```bash
openclaw approvals get [--node <id>]
openclaw approvals set --security allowlist --ask on-miss [--node <id>]
openclaw approvals allowlist add [--node <id>] "/usr/bin/rg"
openclaw approvals allowlist remove [--node <id>] <pattern-id>
```

## 插件系统详解

### 官方插件
| 插件 | 安装 |
|------|------|
| Voice Call | `@openclaw/voice-call` |
| MS Teams | `@openclaw/msteams` |
| Matrix | `@openclaw/matrix` |
| Nostr | `@openclaw/nostr` |
| Zalo | `@openclaw/zalo` |
| Zalo Personal | `@openclaw/zalouser` |
| Nextcloud Talk | `@openclaw/nextcloud-talk` |
| LINE | `@openclaw/line` |
| Mattermost | `@openclaw/mattermost` |

### 捆绑插件 (默认禁用)
- `google-antigravity-auth` — Google OAuth
- `google-gemini-cli-auth` — Gemini CLI OAuth
- `qwen-portal-auth` — Qwen OAuth
- `copilot-proxy` — VS Code Copilot桥接
- `memory-lancedb` — LanceDB长期记忆

### 发现优先级
1. `plugins.load.paths` (配置路径)
2. `<workspace>/.openclaw/extensions/` (工作区)
3. `~/.openclaw/extensions/` (全局)
4. 捆绑扩展 (需显式启用)

### 配置
```json5
plugins: {
  enabled: true,
  allow: ["voice-call"],
  deny: ["untrusted"],
  load: { paths: ["~/Projects/my-plugin"] },
  entries: {
    "voice-call": { enabled: true, config: { provider: "twilio" } }
  },
  slots: {
    memory: "memory"  // 或 "memory-lancedb"
  }
}
```

### 插件能力
工具、Skills、Hooks、渠道、CLI命令、RPC方法、HTTP处理程序、后台服务

### CLI
```bash
openclaw plugins list [--json]
openclaw plugins info <id>
openclaw plugins install <path|npm-spec>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

## 提权模式 (Elevated)
```json5
tools: { elevated: { mode: "on" } }  // on|off|ask|full
```
| 模式 | 说明 |
|------|------|
| `off` | 禁用提权 |
| `on` | 允许提权(默认) |
| `ask` | 每次提权需确认 |
| `full` | 完全权限(跳过审批) |

运行时: `/elevated on|off|ask|full`

## 斜杠命令完整列表
| 命令 | 说明 |
|------|------|
| `/status` | 快速诊断 |
| `/model [id]` | 切换模型 |
| `/reasoning on\|off\|stream\|high\|low` | 推理模式 |
| `/verbose on\|off\|full` | 详细模式 |
| `/elevated on\|off\|ask\|full` | 提权模式 |
| `/new [model]` | 重置会话(可选切换模型) |
| `/reset` | 重置会话 |
| `/stop` | 中止当前运行+子智能体 |
| `/compact [focus]` | 手动压缩 |
| `/context list\|detail` | 查看系统提示内容 |
| `/config set\|unset <path> [value]` | 持久化配置 |
| `/debug <key> <value>` | 运行时覆盖 |
| `/exec host=... security=... node=...` | Exec会话覆盖 |
| `/activation mention\|always` | 群组触发模式 |
| `/send on\|off\|inherit` | 发送策略 |
| `/tts off\|always\|inbound\|tagged` | TTS模式 |
| `/subagents list\|kill\|log\|info\|send\|steer\|spawn` | 子智能体管理 |
| `! <cmd>` | 主机shell命令 |
