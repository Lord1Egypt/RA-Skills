# 中文

## 首次配置

如果用户表示要为 OpenClaw 安装或配置 HiLight：

1. 如果请求里没有 API Key，先向用户索取。
2. 只有用户要连接非默认服务时，才追问 `wsUrl`。
3. 如果用户没有提供 `wsUrl`，使用官方默认地址：

```text
wss://open.guangfan.com/open-apis/device-agent/v1/websocket
```

4. 执行：

```bash
bash scripts/setup_hi_light.sh --api-key '<token>'
```

如果用户提供了自定义 WebSocket 地址：

```bash
bash scripts/setup_hi_light.sh --api-key '<token>' --ws-url 'wss://example/path'
```

## 更新已有配置

如果插件已经装好，用户只是想更新 API Key 或切换 WebSocket 地址，执行：

```bash
bash scripts/setup_hi_light.sh --api-key '<token>' --skip-install
```

需要切换地址时，再追加 `--ws-url`。

## 安全规则

- 把 API Key 视为敏感信息。
- 不要在说明性回复里回显真实 token。
- 如果用户想先看变更内容，优先加 `--dry-run`。

## 脚本会改什么

setup 脚本会通过 OpenClaw 官方命令更新这些配置：

- `channels["hi-light"].enabled`
- `channels["hi-light"].wsUrl`
- `channels["hi-light"].authToken`
- `channels["hi-light"].dmPolicy`
- `channels["hi-light"].allowFrom`

除非使用 `--no-restart`，否则脚本还会校验配置并重启 gateway。

# English

## First-time setup

If the user says they want to install or configure HiLight for OpenClaw:

1. Ask for the HiLight API key if it is not already present in the request.
2. Ask for `wsUrl` only if they want a non-default endpoint.
3. Use the official default websocket URL when `wsUrl` is omitted:

```text
wss://open.guangfan.com/open-apis/device-agent/v1/websocket
```

4. Run:

```bash
bash scripts/setup_hi_light.sh --api-key '<token>'
```

If they provide a custom websocket endpoint:

```bash
bash scripts/setup_hi_light.sh --api-key '<token>' --ws-url 'wss://example/path'
```

## Update existing config

If the plugin is already installed and the user only wants to rotate the API key or change the websocket URL, use:

```bash
bash scripts/setup_hi_light.sh --api-key '<token>' --skip-install
```

Add `--ws-url` when the endpoint should change.

## Safe handling

- Treat the API key as secret input.
- Do not echo the real token in your narrative response.
- Prefer `--dry-run` first if the user wants to preview changes.

## What the script changes

The setup script uses OpenClaw's own config commands to update:

- `channels["hi-light"].enabled`
- `channels["hi-light"].wsUrl`
- `channels["hi-light"].authToken`
- `channels["hi-light"].dmPolicy`
- `channels["hi-light"].allowFrom`

It then validates config and restarts the gateway unless `--no-restart` is used.
