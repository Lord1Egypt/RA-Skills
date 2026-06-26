# OpenClaw OneBot 11 Channel Plugin 🐧

[中文](#中文) | [English](#english)

---

## 中文

OpenClaw 的 **OneBot 11 协议通道插件**，让 QQ 成为 OpenClaw 一等消息通道。

支持 [NapCat](https://github.com/NapNeko/NapCatQQ)、[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 等所有兼容 OneBot 11 协议的 QQ 机器人框架。

说明：
- npm 包名是 `openclaw-onebot`
- ClawHub package payload 包名是 `openclaw-onebot-plugin`
- 插件 `id` 是 `openclaw-onebot`
- 通道 `id` 仍然是 `onebot`
- 因此 `plugins.allow` / `plugins.entries` 使用 `openclaw-onebot`；安装记录由 `openclaw plugins install` 管理
- `channels.onebot` 保持不变
- 当前版本对齐 OpenClaw `2026.4.26` / plugin-sdk `2026.4.26`，并声明 `setupEntry` 与 `channelConfigs` manifest metadata

### 功能

- 🔌 **原生通道插件** — QQ 与 Discord / Telegram / WhatsApp 同级
- 📨 私聊和群聊收发消息
- 😀 **Reaction 支持（群聊）** — 通过 NapCat `set_msg_emoji_like` 给群消息加表情回应；QQ 私聊目前不稳定/通常不生效
- 👍 **群聊自动 reaction** — 对入站群消息自动点表情，可配置开关，默认关闭
- 🌊 **Block streaming** — 支持 OpenClaw 分块回复，QQ 端会连续收到多条流式消息
- 🧭 **OpenClaw 文本命令支持** — 已授权来源可使用 `/status`、`/help`、`/commands`、`/model`、`/new`、`/reset` 等命令
- 🎤 **语音完整链路** — QQ 语音 (SILK/AMR) → MP3 → STT → TTS → 发送 QQ 语音
- 📦 **消息聚合** — 连续多条消息 1.5s 内自动合并（类似 Telegram 风格）
- 🖼️ 图片、语音、文件附件发送
- 🛠️ 通用 `sendMedia` 出站适配，delivery recovery / mirror / message tool 等通路都能发送图片、语音、文件
- 🔄 WebSocket 自动重连（指数退避）
- 🔒 可选 access token 鉴权
- 🎯 `allowFrom` 消息来源过滤（私聊/群聊/用户级别）
- 🛡️ 未配置 `allowFrom` 时 QQ 文本命令不会被授权；需要显式白名单或 `["*"]`
- ✅ 120 个测试用例全部通过
- 📈 覆盖率可通过 `npm run coverage` 复核

### 架构

```
QQ 机器人框架 (NapCat / go-cqhttp)
  ├── WebSocket → 接收消息 (含语音 SILK/AMR 自动转 MP3)
  └── HTTP API  → 发送消息 (文字/图片/语音)
      ↕
OpenClaw OneBot Plugin (ChannelPlugin)
  ├── 消息聚合 (1.5s debounce)
  ├── 语音处理 (SILK → pilk → PCM → ffmpeg → MP3)
  └── allowFrom 过滤
      ↕
OpenClaw Gateway (统一消息管线)
  ├── STT (语音转文字)
  ├── Agent 对话
  ├── Block streaming (多段消息回复)
  ├── Reaction action
  └── TTS (文字转语音) → sendRecord → QQ 语音
```

### 快速开始

#### 1. 安装插件

```bash
# 推荐：直接安装已发布的 ClawHub payload
openclaw plugins install clawhub:openclaw-onebot-plugin

# 自动安装；默认不会修改本机 OpenClaw CLI dist
bash scripts/install.sh

# 或审查源码后手动准备本地发布包
npm install && npm run prepare:clawhub:plugin
openclaw plugins install .clawhub-plugin/openclaw-onebot-plugin
```

`scripts/install.sh` 会先在源码仓库生成 `.clawhub-plugin/openclaw-onebot-plugin` 精简发布包，并优先通过 `openclaw plugins install` 写入新版插件安装索引；旧版 OpenClaw 会回退到手动复制安装。脚本默认不会修改 OpenClaw CLI dist；只有当你的 OpenClaw 构建缺少 `--shared-dir` / `--container-shared-dir` setup 参数时，才需要显式执行 `ONEBOT_SYNC_OPENCLAW_CLI=1 bash scripts/install.sh` 或 `npm run sync:openclaw-cli`。

#### 2. 配置

在 `openclaw.json` 中添加：

```json
{
  "plugins": {
    "allow": ["openclaw-onebot"],
    "entries": {
      "openclaw-onebot": {
        "enabled": true
      }
    }
  },
  "channels": {
    "onebot": {
      "enabled": true,
      "wsUrl": "ws://your-host:3001",
      "httpUrl": "http://your-host:3001",
      "accessToken": "your_token",
      "sharedDir": "/Users/you/napcat/shared",
      "containerSharedDir": "/shared",
      "allowFrom": ["private:12345"],
      "groupAutoReact": false,
      "groupAutoReactEmojiId": 1
    }
  }
}
```

说明：
- 插件配置键使用 `openclaw-onebot`
- 通道配置键使用 `channels.onebot`
- 强烈建议配置 `allowFrom` 为可信 QQ 私聊或群聊；不配置时普通消息仍可进入通道，但 `/status`、`/model` 等 OpenClaw 文本命令不会被授权
- `accessToken` 应使用强随机值，并只把 OneBot HTTP/WebSocket 端点暴露给本机或可信网络
- `sharedDir` 建议使用专用目录，不要与下载、桌面、文档等私人文件目录混用
- 不要手写 `plugins.installs`；新版 OpenClaw 会把插件安装记录保存在托管安装索引中，请使用 `openclaw plugins install <path-or-package>`

也支持环境变量：

```bash
ONEBOT_WS_URL=ws://your-host:3001
ONEBOT_HTTP_URL=http://your-host:3001
ONEBOT_ACCESS_TOKEN=your_token  # 可选
```

OneBot `setup` 也支持：
- `--token wsUrl,httpUrl[,accessToken[,sharedDir[,containerSharedDir]]]`
- 或 `openclaw channels add --channel onebot --shared-dir <hostPath> --container-shared-dir /shared`
- 如果 OpenClaw 升级后覆盖了 CLI dist，且当前 OpenClaw 仍不支持 shared-dir 参数，可在插件目录审查后执行 `npm run sync:openclaw-cli` 重新同步参数接线

#### 3. 重启 Gateway

```bash
openclaw gateway restart
```

### 高级配置

```json
{
  "channels": {
    "onebot": {
      "enabled": true,
      "wsUrl": "ws://your-host:3001",
      "httpUrl": "http://your-host:3001",
      "accessToken": "your_token",
      "sharedDir": "/Users/you/napcat/shared",
      "containerSharedDir": "/shared",
      "allowFrom": ["private:12345", "group:67890"],
      "groupAutoReact": false,
      "groupAutoReactEmojiId": 1
    }
  }
}
```

| 参数 | 说明 |
|------|------|
| `allowFrom` | 消息来源白名单 — `private:<QQ号>`、`group:<群号>`、或 `*`（允许所有） |
| `accessToken` | HTTP API 用 Bearer token，WebSocket 用 query 参数 |
| `sharedDir` | 宿主机共享目录；默认 `~/napcat/shared`，用于把语音/图片 stage 给 NapCat |
| `containerSharedDir` | 容器内共享目录；默认 `/shared`，与 `sharedDir` 对应 |
| `groupAutoReact` | 是否对入站群消息自动添加 reaction，默认 `false` |
| `groupAutoReactEmojiId` | 群聊自动 reaction 使用的 QQ emoji id，默认 `1` |

### Reaction 与流式回复

- **Reaction**
  - 插件实现了 OpenClaw channel action `react`
  - 通过 NapCat `set_msg_emoji_like` 对群消息或指定群消息 `message_id` 添加表情
  - QQ 私聊 reaction 目前不可靠，接口可能返回成功，但不会真正落到消息上
  - 入站群消息还支持自动 reaction，受 `groupAutoReact` / `groupAutoReactEmojiId` 控制，默认关闭
- **流式回复**
  - 这里支持的是 **OpenClaw block streaming**
  - QQ 端表现为连续多条分块消息，不是“编辑同一条消息”的 draft stream
  - 开启方式：

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on"
    }
  }
}
```

- 可选调优：

```json
{
  "channels": {
    "onebot": {
      "streaming": {
        "block": {
          "coalesce": {
            "minChars": 80,
            "idleMs": 600
          }
        }
      }
    }
  }
}
```

旧版 `channels.onebot.blockStreamingCoalesce` 仍兼容；新版 `openclaw doctor --fix` 会把它迁移到 `channels.onebot.streaming.block.coalesce`。

### 验证

- **Reaction**
  - 先让家庭群里出现一条新消息
  - 从 gateway 日志里拿到 `msg=<message_id>`
  - 再执行：

```bash
npm run build
npm run react-test -- --message-id <message_id> --emoji 76
```

  - 当前建议只把这项验证用于群聊消息；私聊 reaction 在 QQ/NapCat 上通常不生效

- **Streaming**
  - 在 OpenClaw 配置里开启 `agents.defaults.blockStreamingDefault = "on"`
  - 然后在 QQ 里发一条明确要求“分段回复”的消息
  - 成功时，QQ 会连续收到多条消息，日志里会出现 `deliver(block)`，最后再有 `deliver(final)`

### 语音支持（可选）

支持 QQ 语音消息的完整自动处理链路：

- **入站**：QQ 语音 (SILK/AMR) → 下载 → 转 MP3 → OpenClaw STT 转文字 → Agent 生成回复
- **出站**：Agent 回复 → TTS 生成音频 → `sendRecord` 发送 QQ 语音

**依赖**：
- `ffmpeg` — 音频格式转换
- `uv` — 运行 `pilk` 解码 SILK 格式（AMR 仅需 ffmpeg）

不需要语音功能时可以跳过这些依赖。

### 消息目标格式

- `private:<QQ号>` — 私聊消息
- `group:<群号>` — 群聊消息
- `<QQ号>` — 自动识别为私聊

### NapCat 部署参考

推荐使用 Docker 部署 [NapCat](https://github.com/NapNeko/NapCatQQ)：

```yaml
# docker-compose.yml
services:
  napcat:
    image: mlikiowa/napcat-docker:latest
    restart: always
    ports:
      - "3001:3001"   # OneBot 11 WS + HTTP
      - "6099:6099"   # WebUI
    volumes:
      - ./napcat-data:/app/.config/QQ
      - ./shared:/shared   # 文件共享目录
```

### 开发

```bash
npm install
npm test          # 120 tests
npm run build     # 编译 TypeScript
npm run coverage  # 覆盖率报告
npm run sync:openclaw-cli  # 审查后重新同步 OpenClaw CLI 的 shared-dir 参数
```

### 发布准备

```bash
npm ci --ignore-scripts
npm run release:check
npm publish --access public
```

说明：
- `npm run release:check` 会串行执行 `build`、全量 `vitest`、`npm pack --dry-run`、`npm publish --dry-run`、ClawHub package/skill 产物准备
- npm 包名保持 `openclaw-onebot`，用于兼容已经安装 `openclaw-onebot@1.2.x` 的用户
- ClawHub package payload 包名是 `openclaw-onebot-plugin`
- OpenClaw runtime manifest id 仍是 `openclaw-onebot`，用于现有 `plugins.allow` / `plugins.entries` 配置兼容
- ClawHub package 产物输出到 `.clawhub-plugin/openclaw-onebot-plugin/`
- ClawHub skill 产物输出到 `.clawhub-skill/openclaw-onebot/`
- npm 发布后，再创建同版本 GitHub tag/release，并用同一个 tag 发布 ClawHub package 和 skill；完整命令见 [docs/release-runbook.md](docs/release-runbook.md)

---

## English

An [OpenClaw](https://github.com/openclaw/openclaw) **native channel plugin** that connects to [NapCat](https://github.com/NapNeko/NapCatQQ), [go-cqhttp](https://github.com/Mrs4s/go-cqhttp), or any OneBot 11 compatible QQ bot framework.

Note:
- npm package name: `openclaw-onebot`
- ClawHub package payload name: `openclaw-onebot-plugin`
- Plugin `id`: `openclaw-onebot`
- Channel `id`: `onebot`
- Use `openclaw-onebot` in `plugins.allow` / `plugins.entries`; install records are managed by `openclaw plugins install`
- Keep `channels.onebot` unchanged
- This release targets OpenClaw `2026.4.26` / plugin-sdk `2026.4.26` and declares `setupEntry` plus `channelConfigs` manifest metadata

### Features

- 🔌 **Native channel plugin** — QQ on par with Discord / Telegram / WhatsApp
- 📨 Private & group chat (inbound + outbound)
- 😀 **Reaction support (groups)** — react to a QQ group message via NapCat `set_msg_emoji_like`; QQ private-chat reactions are currently unreliable
- 👍 **Automatic group reactions** — auto-react to inbound group messages with a configurable switch, disabled by default
- 🌊 **Block streaming** — OpenClaw partial replies arrive as multiple QQ messages
- 🎤 **Full voice pipeline** — QQ voice (SILK/AMR) → MP3 → STT → TTS → send QQ voice
- 📦 **Message batching** — auto-merge rapid messages within 1.5s (Telegram-style)
- 🖼️ Image, audio, and file attachments
- 🛠️ Generic `sendMedia` outbound adapter so delivery recovery, mirror, and message-tool paths can all send images, audio, and files
- 🔄 WebSocket auto-reconnect with exponential backoff
- 🔒 Optional access token authentication
- 🎯 `allowFrom` filtering (private/group/user-level)
- 🧭 OpenClaw text-command support for authorized senders (`/status`, `/help`, `/commands`, `/model`, `/new`, `/reset`, etc.)
- 🛡️ OpenClaw text commands are not authorized until `allowFrom` is explicitly configured
- ✅ 120 tests passing
- 📈 Coverage can be re-generated with `npm run coverage`

### Quick Start

#### 1. Install

```bash
# Recommended: install the published ClawHub payload
openclaw plugins install clawhub:openclaw-onebot-plugin

# Auto install; does not patch the local OpenClaw CLI dist by default
bash scripts/install.sh

# Or prepare a local payload after reviewing the source
npm install && npm run prepare:clawhub:plugin
openclaw plugins install .clawhub-plugin/openclaw-onebot-plugin
```

`scripts/install.sh` prepares `.clawhub-plugin/openclaw-onebot-plugin` in the source repo first and prefers `openclaw plugins install` so current OpenClaw builds update the managed plugin install index. Older OpenClaw builds fall back to the legacy manual copy path. It no longer patches OpenClaw CLI dist by default; set `ONEBOT_SYNC_OPENCLAW_CLI=1` only after reviewing `scripts/sync-openclaw-cli.mjs` and confirming your OpenClaw build lacks the shared-dir setup flags.

#### 2. Configure

Add to `openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-onebot"],
    "entries": {
      "openclaw-onebot": {
        "enabled": true
      }
    }
  },
  "channels": {
    "onebot": {
      "enabled": true,
      "wsUrl": "ws://your-host:3001",
      "httpUrl": "http://your-host:3001",
      "accessToken": "your_token",
      "sharedDir": "/Users/you/napcat/shared",
      "containerSharedDir": "/shared",
      "allowFrom": ["private:12345"],
      "groupAutoReact": false,
      "groupAutoReactEmojiId": 1
    }
  }
}
```

Notes:
- Use `openclaw-onebot` for plugin config keys
- Keep runtime channel config under `channels.onebot`
- Configure `allowFrom` to trusted QQ private users or groups. Without it, normal messages can still be routed, but OpenClaw text commands such as `/status` and `/model` are not authorized
- Use a strong `accessToken` and keep OneBot HTTP/WebSocket endpoints on localhost or a trusted network
- Use a dedicated `sharedDir`; do not point it at unrelated private files
- Do not edit `plugins.installs` by hand; current OpenClaw stores install records in a managed plugin index, so use `openclaw plugins install <path-or-package>`

Or via environment variables:

```bash
ONEBOT_WS_URL=ws://your-host:3001
ONEBOT_HTTP_URL=http://your-host:3001
ONEBOT_ACCESS_TOKEN=your_token  # optional
```

OneBot setup also supports:
- `--token wsUrl,httpUrl[,accessToken[,sharedDir[,containerSharedDir]]]`
- or `openclaw channels add --channel onebot --shared-dir <hostPath> --container-shared-dir /shared`
- if an OpenClaw upgrade overwrites the installed CLI dist and your current OpenClaw build still lacks shared-dir flags, review then run `npm run sync:openclaw-cli` from the plugin directory

#### 3. Restart Gateway

```bash
openclaw gateway restart
```

### Voice Support (Optional)

End-to-end voice flow:
- **Inbound**: QQ voice (SILK/AMR) → download → MP3 → OpenClaw STT → Agent reply
- **Outbound**: Agent reply → TTS audio → `sendRecord` → QQ voice

**Dependencies**: `ffmpeg` + `uv` (for SILK decoding via `pilk`). Skip if text/image only.

### Reactions and Streaming Replies

- **Reactions**
  - The plugin implements the OpenClaw `react` channel action
  - It maps to NapCat `set_msg_emoji_like`
  - Group-message reactions are supported
  - QQ private-chat reactions are currently unreliable: the API may return success while no visible reaction is persisted
  - Inbound group messages can also be auto-reacted, controlled by `groupAutoReact` / `groupAutoReactEmojiId`, disabled by default
- **Streaming replies**
  - This plugin supports **OpenClaw block streaming**
  - QQ receives multiple incremental messages instead of a single edited draft message
  - Enable it with:

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on"
    }
  }
}
```

- Optional coalescing hint for OneBot:

```json
{
  "channels": {
    "onebot": {
      "streaming": {
        "block": {
          "coalesce": {
            "minChars": 80,
            "idleMs": 600
          }
        }
      }
    }
  }
}
```

Legacy `channels.onebot.blockStreamingCoalesce` remains accepted; current `openclaw doctor --fix` migrates it to `channels.onebot.streaming.block.coalesce`.

### Verification

- **Reaction**
  - Send a fresh QQ group message first
  - Read the inbound `msg=<message_id>` from the gateway log
  - Then run:

```bash
npm run build
npm run react-test -- --message-id <message_id> --emoji 76
```

  - For now, treat this as a group-chat verification flow; private-chat reactions are not a reliable capability

- **Streaming**
  - Enable `agents.defaults.blockStreamingDefault = "on"` in OpenClaw config
  - Send a QQ prompt that explicitly asks for chunked / stepwise output
  - Success looks like multiple QQ messages plus `deliver(block)` entries in the gateway log, followed by `deliver(final)`

### Configuration

| Option | Description |
|--------|-------------|
| `allowFrom` | Whitelist — `private:<qq>`, `group:<id>`, or `*` (allow all) |
| `accessToken` | Bearer token for HTTP, query param for WebSocket |
| `sharedDir` | Host-side shared directory; defaults to `~/napcat/shared` for staging outbound media |
| `containerSharedDir` | Container-side mount path; defaults to `/shared` and should map to `sharedDir` |
| `groupAutoReact` | Whether to auto-react to inbound group messages; defaults to `false` |
| `groupAutoReactEmojiId` | QQ emoji id used for automatic group reactions; defaults to `1` |

### Target Format

- `private:<qq_number>` — Private message
- `group:<group_id>` — Group message
- `<qq_number>` — Auto-detected as private

### Development

```bash
npm install
npm test          # Run 120 tests
npm run build     # Compile TypeScript
npm run coverage  # Coverage report
npm run sync:openclaw-cli  # Re-apply shared-dir CLI wiring after review
```

### Release Prep

```bash
npm ci --ignore-scripts
npm run release:check
npm publish --access public
```

Notes:
- `npm run release:check` runs `build`, the full `vitest` suite, `npm pack --dry-run`, `npm publish --dry-run`, and ClawHub package/skill staging
- npm package name stays `openclaw-onebot` for users already installed from `openclaw-onebot@1.2.x`
- ClawHub package payload name: `openclaw-onebot-plugin`
- OpenClaw runtime manifest id stays `openclaw-onebot` for existing `plugins.allow` / `plugins.entries` compatibility
- The ClawHub package payload is written to `.clawhub-plugin/openclaw-onebot-plugin/`
- The ClawHub skill payload is written to `.clawhub-skill/openclaw-onebot/`
- After npm is published, create the same-version GitHub tag/release and publish the ClawHub package plus skill from that tag; see [docs/release-runbook.md](docs/release-runbook.md)

## License

MIT
