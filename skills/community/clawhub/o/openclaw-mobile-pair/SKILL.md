---
name: openclaw-mobile-pair
description: 一键生成 OpenClaw 手机控制中心连接码（自动读取本机 gateway token）
user-invocable: true
---

# OpenClaw Mobile Pair

Use this skill to generate a mobile pairing code for OpenClaw control app users.

## Workflow

1. Ask for `BFF` URL only if not provided by the user.
2. Run `scripts/generate-mobile-pairing.ps1` to generate pairing code.
3. Return:
   - Pairing code
   - Output file path
   - Quick next step for mobile user

## Command Template

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-mobile-pairing.ps1 -BffBaseUrl "<https://api.yourdomain.com/>" -CopyToClipboard
```

## Response Style

- Keep it short and actionable.
- If generation fails, state exact reason and how to fix it.

