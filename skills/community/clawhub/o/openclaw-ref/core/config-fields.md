# OpenClaw 配置字段速查表

> 配置文件: `~/.openclaw/openclaw.json` (JSON5格式，支持注释和尾逗号)
> 严格验证: 未知字段会导致网关拒绝启动，用 `openclaw doctor` 诊断

## agents

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `agents.defaults.workspace` | string | `~/.openclaw/workspace` | 全局工作区目录 |
| `agents.defaults.repoRoot` | string | 自动检测 | 系统提示中显示的仓库根 |
| `agents.defaults.skipBootstrap` | bool | false | 禁用自动创建引导文件 |
| `agents.defaults.bootstrapMaxChars` | number | 20000 | 引导文件截断上限 |
| `agents.defaults.userTimezone` | string | 主机时区 | 用户时区(如 Asia/Shanghai) |
| `agents.defaults.timeFormat` | `auto\|12\|24` | auto | 时间格式 |
| `agents.defaults.model.primary` | string | - | 主力模型(provider/model) |
| `agents.defaults.model.fallbacks` | string[] | [] | 全局故障转移链 |
| `agents.defaults.imageModel.primary` | string | - | 绘图模型(仅主模型无图像输入时用) |
| `agents.defaults.imageModel.fallbacks` | string[] | [] | 绘图模型故障转移 |
| `agents.defaults.models` | object | {} | 模型目录(也是/model白名单) |
| `agents.defaults.models.<id>.alias` | string | - | 模型快捷方式 |
| `agents.defaults.models.<id>.params` | object | - | 提供商API参数(temperature/maxTokens) |
| `agents.defaults.thinkingDefault` | string | off | 默认思考级别(off/low/high) |
| `agents.defaults.verboseDefault` | string | off | 默认详细级别 |
| `agents.defaults.elevatedDefault` | string | on | 默认提升权限 |
| `agents.defaults.timeoutSeconds` | number | 600 | 智能体运行超时(秒) |
| `agents.defaults.mediaMaxMb` | number | 5 | 入站媒体上限(MB) |
| `agents.defaults.maxConcurrent` | number | 1 | 最大并行运行数 |
| `agents.defaults.contextTokens` | number | 200000 | 上下文token上限 |
| `agents.defaults.blockStreamingDefault` | `on\|off` | off | 分块流式传输 |
| `agents.defaults.blockStreamingBreak` | string | text_end | 流式断点 |
| `agents.defaults.blockStreamingChunk` | object | {min:800,max:1200} | 流式块大小 |
| `agents.defaults.blockStreamingCoalesce` | object | {idleMs:1000} | 流式合并 |
| `agents.defaults.humanDelay` | object | {mode:"off"} | 块回复间延迟 |
| `agents.defaults.typingMode` | string | instant | 输入指示器模式 |
| `agents.defaults.typingIntervalSeconds` | number | 6 | 输入信号刷新频率 |

### agents.defaults.heartbeat
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `heartbeat.every` | string | 30m | 心跳间隔(ms/s/m/h) |
| `heartbeat.model` | string | - | 心跳运行覆盖模型 |
| `heartbeat.target` | string | last | 投递渠道(last/whatsapp/telegram/none等) |
| `heartbeat.to` | string | - | 收件人覆盖 |
| `heartbeat.prompt` | string | 内置 | 心跳提示内容 |
| `heartbeat.session` | string | main | 心跳运行的会话键 |
| `heartbeat.ackMaxChars` | number | 300 | HEARTBEAT_OK后最大字符数 |
| `heartbeat.includeReasoning` | bool | false | 包含推理消息 |

### agents.defaults.subagents
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `subagents.model` | string | 继承调用者 | 子智能体默认模型 |
| `subagents.maxConcurrent` | number | 1 | 最大并发子智能体数 |
| `subagents.archiveAfterMinutes` | number | 60 | 自动归档时间(0禁用) |

### agents.defaults.exec
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `exec.backgroundMs` | number | 10000 | 自动后台化时间(ms) |
| `exec.timeoutSec` | number | 1800 | 运行超时(秒) |
| `exec.cleanupMs` | number | 1800000 | 完成会话保留时间(ms) |
| `exec.notifyOnExit` | bool | true | 后台退出时通知 |
| `exec.applyPatch.enabled` | bool | false | 启用apply_patch工具 |

### agents.defaults.compaction
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `compaction.mode` | string | default | 压缩策略(default/safeguard) |
| `compaction.reserveTokensFloor` | number | 20000 | 最小预留token |
| `compaction.memoryFlush.enabled` | bool | true | 压缩前记忆刷新 |
| `compaction.memoryFlush.softThresholdTokens` | number | 4000 | 触发阈值 |

### agents.defaults.contextPruning
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `contextPruning.mode` | `off\|adaptive\|aggressive` | off | 工具结果裁剪模式 |
| `contextPruning.keepLastAssistants` | number | 3 | 保护最近N条助手消息 |
| `contextPruning.softTrimRatio` | number | 0.3 | 软裁剪触发比率 |
| `contextPruning.hardClearRatio` | number | 0.5 | 硬清除触发比率 |
| `contextPruning.minPrunableToolChars` | number | 50000 | 最小可裁剪字符数 |
| `contextPruning.softTrim` | object | {maxChars:4000,head:1500,tail:1500} | 软裁剪参数 |
| `contextPruning.hardClear.enabled` | bool | true | 启用硬清除 |
| `contextPruning.tools.deny` | string[] | - | 跳过裁剪的工具 |

### agents.defaults.sandbox
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sandbox.mode` | `off\|non-main\|all` | off | 沙箱模式 |
| `sandbox.scope` | `session\|agent\|shared` | agent | 沙箱作用域 |
| `sandbox.workspaceAccess` | `none\|ro\|rw` | none | 工作区访问级别 |
| `sandbox.workspaceRoot` | string | ~/.openclaw/sandboxes | 沙箱工作区根 |
| `sandbox.docker.image` | string | openclaw-sandbox:bookworm-slim | Docker镜像 |
| `sandbox.docker.network` | string | none | 网络模式(none/bridge) |
| `sandbox.docker.setupCommand` | string | - | 容器创建后运行的命令 |
| `sandbox.docker.pidsLimit` | number | 256 | PID限制 |
| `sandbox.docker.memory` | string | 1g | 内存限制 |
| `sandbox.docker.cpus` | number | 1 | CPU限制 |
| `sandbox.browser.enabled` | bool | false | 沙箱浏览器 |
| `sandbox.prune.idleHours` | number | 24 | 空闲清理时间 |
| `sandbox.prune.maxAgeDays` | number | 7 | 最大存活天数 |

## models

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `models.mode` | `merge\|replace` | merge | merge=合并内置+自定义, replace=仅用自定义 |
| `models.providers.<name>.baseUrl` | string | - | API 基础 URL |
| `models.providers.<name>.apiKey` | string | - | API Key (支持 `${ENV_VAR}`) |
| `models.providers.<name>.api` | string | - | API 类型: `openai-completions` / `anthropic-messages` |
| `models.providers.<name>.models` | array | [] | 模型列表 |
| `models.providers.<name>.models[].id` | string | - | 模型 ID |
| `models.providers.<name>.models[].name` | string | - | 显示名称 |
| `models.providers.<name>.models[].reasoning` | bool | false | 是否为推理模型 |
| `models.providers.<name>.models[].input` | string[] | ["text"] | 输入类型: text, image |
| `models.providers.<name>.models[].cost` | object | - | 成本(input/output/cacheRead/cacheWrite) |
| `models.providers.<name>.models[].contextWindow` | number | - | 上下文窗口大小 |
| `models.providers.<name>.models[].maxTokens` | number | - | 最大输出 tokens |

### 模型配置示例
```json
{
  "models": {
    "mode": "replace",
    "providers": {
      "my-provider": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "${MY_API_KEY}",
        "api": "openai-completions",
        "models": [{
          "id": "my-model",
          "name": "My Model",
          "reasoning": false,
          "input": ["text", "image"],
          "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
          "contextWindow": 128000,
          "maxTokens": 8192
        }]
      }
    }
  }
}
```

## auth

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `auth.profiles.<profileId>.provider` | string | - | 提供商名称 |
| `auth.profiles.<profileId>.mode` | string | api_key | 认证模式(api_key/oauth) |
| `auth.cooldowns.billingBackoffHours` | number | 1 | 计费错误退避(小时) |
| `auth.cooldowns.billingMaxHours` | number | 24 | 最大退避(小时) |
| `auth.cooldowns.failureWindowHours` | number | 1 | 失败窗口(小时) |

## logging

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `logging.consoleLevel` | string | warn | 控制台级别(debug/info/warn/error) |
| `logging.consoleStyle` | string | pretty | 控制台样式(pretty/json) |
| `logging.redactSensitive` | string | tools | 敏感信息脱敏(off/tools/all) |
| `logging.fileLevel` | string | info | 文件日志级别 |
| `logging.maxFileSizeMb` | number | 50 | 日志文件大小上限(MB) |
| `logging.maxFiles` | number | 5 | 保留日志文件数 |

## browser

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `browser.enabled` | bool | true | 启用浏览器工具 |
| `browser.headless` | bool | true | 无头模式 |
| `browser.executablePath` | string | 自动检测 | 浏览器可执行文件路径 |
| `browser.userDataDir` | string | - | 用户数据目录 |
| `browser.defaultViewport` | object | {width:1280,height:720} | 默认视口 |
| `browser.launchArgs` | string[] | [] | 额外启动参数 |
| `browser.connectOverCDP` | string | - | CDP WebSocket URL |
| `browser.idleTimeoutMs` | number | 300000 | 空闲关闭时间(ms) |

## channels (渠道)

### Telegram
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `channels.telegram.accounts.<name>.token` | string | - | Bot Token |
| `channels.telegram.accounts.<name>.allowedChatIds` | number[] | [] | 允许的聊天ID |
| `channels.telegram.accounts.<name>.adminChatIds` | number[] | [] | 管理员聊天ID |
| `channels.telegram.accounts.<name>.polling` | bool | true | 轮询模式 |
| `channels.telegram.accounts.<name>.webhook` | object | - | Webhook配置 |
| `channels.telegram.accounts.<name>.webhook.url` | string | - | Webhook URL |
| `channels.telegram.accounts.<name>.webhook.secretToken` | string | - | 验证密钥 |
| `channels.telegram.accounts.<name>.reactions` | object | - | 反应配置 |
| `channels.telegram.accounts.<name>.reactions.mode` | `off\|minimal\|full` | off | 反应模式 |
| `channels.telegram.accounts.<name>.reactions.customEmoji` | bool | false | 自定义表情 |

### Discord
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `channels.discord.accounts.<name>.token` | string | - | Bot Token |
| `channels.discord.accounts.<name>.applicationId` | string | - | 应用ID |
| `channels.discord.accounts.<name>.allowedGuildIds` | string[] | [] | 允许的服务器ID |
| `channels.discord.accounts.<name>.allowedChannelIds` | string[] | [] | 允许的频道ID |
| `channels.discord.accounts.<name>.adminUserIds` | string[] | [] | 管理员用户ID |

### WhatsApp
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `channels.whatsapp.accounts.<name>.phoneNumber` | string | - | 电话号码 |
| `channels.whatsapp.accounts.<name>.allowedJids` | string[] | [] | 允许的JID |
| `channels.whatsapp.accounts.<name>.adminJids` | string[] | [] | 管理员JID |

### Signal
| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `channels.signal.accounts.<name>.number` | string | - | 电话号码 |
| `channels.signal.accounts.<name>.allowedNumbers` | string[] | [] | 允许的号码 |
| `channels.signal.accounts.<name>.adminNumbers` | string[] | [] | 管理员号码 |

## gateway

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `gateway.port` | number | 3121 | 监听端口 |
| `gateway.host` | string | 127.0.0.1 | 监听地址 |
| `gateway.token` | string | 自动生成 | API 认证令牌 |
| `gateway.runtime` | `node\|bun` | node | 运行时 |
| `gateway.autoStart` | bool | true | 自动启动 |
| `gateway.tailscale.enabled` | bool | false | Tailscale 集成 |
| `gateway.tailscale.hostname` | string | openclaw | Tailscale 主机名 |
| `gateway.tailscale.funnel` | bool | false | Tailscale Funnel |
| `gateway.bonjour.enabled` | bool | false | Bonjour 发现 |
| `gateway.bonjour.name` | string | - | Bonjour 服务名 |

## tools

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tools.policy` | `full\|allowlist\|deny` | full | 工具策略 |
| `tools.allow` | string[] | - | 允许的工具列表(policy=allowlist时) |
| `tools.deny` | string[] | - | 拒绝的工具列表 |
| `tools.elevated.mode` | `on\|off\|ask` | on | 提升权限模式 |
| `tools.elevated.allow` | string[] | - | 允许提升的工具 |
| `tools.exec.approvals.mode` | `off\|allowlist\|full` | off | 命令审批模式 |
| `tools.exec.approvals.allowlist` | string[] | - | 免审批命令列表 |

## commands (斜杠命令)

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `commands.config` | bool | false | 启用 /config 命令 |
| `commands.debug` | bool | false | 启用 /debug 命令 |
| `commands.bash` | bool | false | 启用 ! shell 命令 |

## tts

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tts.provider` | string | - | TTS 提供商(elevenlabs/openai/deepgram) |
| `tts.voice` | string | - | 默认语音 |
| `tts.model` | string | - | TTS 模型 |
| `tts.speed` | number | 1.0 | 语速 |
| `tts.mode` | `off\|always\|inbound\|tagged` | off | TTS 模式 |

## web

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `web.enabled` | bool | false | 启用 Web UI |
| `web.port` | number | 3122 | Web UI 端口 |
| `web.auth` | object | - | Web 认证配置 |

## groups (群组策略)

| 路径 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `groups.mode` | `off\|allowlist\|all` | off | 群组模式 |
| `groups.allowlist` | string[] | [] | 允许的群组ID |
| `groups.triggerMode` | `mention\|all\|smart` | mention | 触发模式 |
| `groups.replyMode` | `reply\|send\|thread` | reply | 回复模式 |
| `groups.cooldownSeconds` | number | 0 | 冷却时间(秒) |
| `groups.maxHistoryMessages` | number | 50 | 最大历史消息数 |
