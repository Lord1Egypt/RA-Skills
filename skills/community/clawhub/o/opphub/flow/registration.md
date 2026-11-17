# 注册流程 · v3.1 (2026-07-20 修)

> v3.1 走 OPC 原生 `/api/auth/*` 两段式（发码 + 注册），不是 OAuth device flow。
> **plugin 仓的注册 / 登录入口要清理**（v3.1 backlog，见 workboard）。


1. `POST /api/auth/code/send`
   - body: `{ type: "email" | "phone", target: string, purpose: "login" }`
   - resp: `{ ok: true, ttl: 300 }` / `{ code: "TOO_MANY_REQUESTS", error: "rate_limit" | "dedup" }` / `{ code: "CONFLICT", message: "该邮箱/手机号已注册，请直接登录" }`

2. `POST /api/auth/register`
   - body: `{ type: "email" | "phone", target: string, code: string(6 位) }`
   - resp: `{ ok: true, opcId, opphubToken, message }` / `{ error: "invalid_code" }` / `{ error: "already_registered" }`

> ⚠️ 历史：`/api/oauth/register` 是老路径（v0.x），现已迁移到 `/api/auth/register`。本 skill 必须用新路径。


```
用户: @bot 偶合注册
bot: 好的，用邮箱还是手机注册？
     - 回复「邮箱」/「手机」或直接发「邮箱 you@example.com」/「手机 13800138000」

用户: @bot 邮箱 you@example.com
bot 调: POST /api/auth/code/send { type: "email", target: "you@example.com", purpose: "login" }
bot: ✅ 验证码已发到 you@example.com（5 分钟内有效）
     请把收到的 6 位数字告诉我（请不要在群里贴，我私下问你）

用户: (私下给 bot) 123456
bot 调: POST /api/auth/register { type: "email", target: "you@example.com", code: "123456" }
bot: ✅ 注册成功 · opc_id = opc_xxx
     下一步走 "偶合登录" 拿 access_token（device flow）
```

## 注意事项

- **验证码不在公开对话框贴**（runtime 12:04 误贴 567425 教训）
- 5 分钟 1 次冷却（dedup = 还在有效期内不重发；rate_limit = IP 冲击 5 次/分钟）
- 邮箱/手机已注册 → server 返 `CONFLICT`，bot 引导直接走 "偶合登录"（不重复注册）
- bot 调 `/api/auth/register` 拿到的 `opphubToken` 是 30 天 JWT（带 `opphub:profile:rw` scope），
  但 device flow 拿的 access_token 才是走 plugin WS 推送的凭证——**注册 ≠ 登录**，注册完还要再走偶合登录

## 关联

- `偶合登录` → `POST /api/oauth/device/code` + `POST /api/oauth/device/token`（device flow，OAuth）
- `偶合状态` → `/api/oauth/userinfo` 验 token + 本机 Keychain 读 tokenStatus
- **plugin 仓 register / login CLI 子命令清理** → v3.1 backlog（不走 plugin CLI 走 skill，详见 workboard 卡 `plugin-cli-cleanup-2026-07-20`）
