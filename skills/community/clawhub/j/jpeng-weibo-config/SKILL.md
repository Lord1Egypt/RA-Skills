---
name: weibo-config
description: 连接微博渠道到 OpenClaw。当用户说"连接微博"、"配置微博"、"绑定微博"、"接入微博"时使用。需要 AppId 和 AppSecret 凭证。
---

# Weibo Channel Configuration

Configure Weibo channel credentials via OpenClaw CLI.

## Required Credentials

- **AppId** — Weibo application ID
- **AppSecret** — Weibo application secret

## Configuration Commands

```bash
openclaw config set 'channels.weibo.appId' '<AppId>'
openclaw config set 'channels.weibo.appSecret' '<AppSecret>'
```

## Workflow

1. Ask the user for AppId and AppSecret (if not provided).
2. Run the two `openclaw config set` commands above with the provided values.
3. Verify with `openclaw config get 'channels.weibo'` (if available) or confirm to the user that configuration is complete.

## Example

Given:
- AppId: `AppIdExample`
- AppSecret: `AppSecretExample`

Execute:
```bash
openclaw config set 'channels.weibo.appId' 'AppIdExample'
openclaw config set 'channels.weibo.appSecret' 'AppSecretExample'
```
