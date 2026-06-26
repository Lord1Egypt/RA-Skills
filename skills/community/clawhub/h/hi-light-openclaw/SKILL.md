---
name: hi-light-openclaw
description: 以用户可执行的工作流方式安装、配置和排查 HiLight OpenClaw 插件。用户想把 OpenClaw 连接到 HiLight、安装 `@art_style666/hi-light` 插件、把 `channels["hi-light"]` 写入 OpenClaw 配置、更新 HiLight API Key 或 WebSocket 地址、或排查 HiLight 无法连接时使用。 Install, configure, and troubleshoot the HiLight OpenClaw plugin as a user-facing setup workflow. Use when a user wants to connect OpenClaw to HiLight, install `@art_style666/hi-light`, write `channels["hi-light"]` into OpenClaw config, update the HiLight API key or websocket URL, or diagnose why the HiLight channel does not connect.
---

# HiLight For OpenClaw

## 中文说明

把这个 skill 当成 HiLight 插件的用户入口。第一次使用时，它应该把“收集 API Key、安装插件、写入 `channels["hi-light"]`、重启网关、确认结果”串成一个完整流程。

### 首次使用

如果用户要配置 HiLight，但没有提供 API Key，先向用户索取，再执行命令。

如果用户没有提供 WebSocket 地址，直接使用官方默认地址。除非用户明确要连自定义服务，否则不要强制追问 `wsUrl`。

把 API Key 当成敏感信息处理，不要在回复里回显真实 token。

### 配置流程

1. 需要精确的用户交互和命令样例时，先读 [user-flow.md](references/user-flow.md)。
2. 标准安装执行 `bash scripts/setup_hi_light.sh --api-key '<token>'`。
3. 只有用户给了自定义 WebSocket 地址时，才追加 `--ws-url '<url>'`。
4. 如果用户只是更新凭证或覆盖已有配置，追加 `--skip-install`。
5. 如果用户先想看会改什么，先用 `--dry-run`。
6. 脚本完成后，说明哪些配置已写入，以及 gateway restart 是否成功。

### 操作规则

优先使用默认 WebSocket 地址，只有用户明确覆盖时才改。

优先使用 OpenClaw 自带的 `plugins` 和 `config` 命令，不要直接手改 `~/.openclaw/openclaw.json`。

要明确告诉用户：安装 skill 本身不会自动填入 API Key；真正的插件安装和配置发生在第一次调用 skill 时。

如果用户问“怎么用这个 skill”，给出具体句式，例如：

```text
用 $hi-light-openclaw 帮我安装 HiLight，我的 API Key 是 xxx。
```

```text
用 $hi-light-openclaw 帮我更新 HiLight API Key，继续使用默认 ws 地址。
```

## English

Use this skill as the user-facing wrapper around the HiLight plugin. On first use, it should turn “collect API key, install plugin, write `channels["hi-light"]`, restart the gateway, and confirm the result” into one setup flow.

### First Run

If the user wants to set up HiLight and does not provide an API key, ask for it before running commands.

If the user does not provide a websocket URL, use the official default endpoint. Do not force the user to provide `wsUrl` unless they want a custom server.

Treat the API key as secret input. Never repeat the real token in your response.

### Workflow

1. Read [user-flow.md](references/user-flow.md) if you need exact prompt patterns or command examples.
2. Run `bash scripts/setup_hi_light.sh --api-key '<token>'` for standard setup.
3. Add `--ws-url '<url>'` only when the user provides a custom websocket endpoint.
4. Add `--skip-install` when the user only wants to rotate credentials or refresh the existing configuration.
5. Use `--dry-run` first if the user asks what will change before applying it.
6. After the script finishes, summarize what changed and whether the gateway restart succeeded.

### Rules

Prefer the default websocket URL unless the user explicitly overrides it.

Use OpenClaw's own `plugins` and `config` commands instead of editing `~/.openclaw/openclaw.json` directly.

Mention that installing the skill alone does not automatically populate the API key. The actual plugin installation and configuration happen on first use of the skill.

If the user asks how to use the skill, give concrete examples such as:

```text
Use $hi-light-openclaw to install HiLight with my API key xxx.
```

```text
Use $hi-light-openclaw to update my HiLight API key and keep the default websocket URL.
```

## Resources

中文：使用 `scripts/setup_hi_light.sh` 完成安装和配置，使用 [user-flow.md](references/user-flow.md) 查看首次使用流程、更新流程和安全规则。

English: Use `scripts/setup_hi_light.sh` for installation and configuration, and use [user-flow.md](references/user-flow.md) for first-run prompts, update flow, and safe handling rules.
