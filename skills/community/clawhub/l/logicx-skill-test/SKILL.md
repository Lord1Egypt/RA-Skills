---
name: logicx-skill
description: Call LogicX frontend proxy APIs for health checks, browser binding, password login, user info, orders, payments, and account actions.
homepage: http://43.139.104.95:8070
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      bins: ["curl", "bash"]
---

# LogicX Skill

Interact with the LogicX platform on behalf of the user. All API calls go through the frontend proxy (`/api/proxy/*`). Use `scripts/logicx_api.sh` for every request — never write ad-hoc `curl` commands.

## Rules

- Only call `/api/proxy/*` (or `/api/health`). Never call backend `/v1/*` directly.
- Default to browser binding. Only ask for email and password if the user explicitly chooses password login.
- Confirm before any mutating call: `payment/create`, `payment/cancel`, `auth/change-password`, `agent/unlink`.
- Never echo `LOGICX_AGENT_SERVICE_KEY` or `LOGICX_USER_TOKEN` in full.
- Never infer binding, membership, order, or payment state — report API responses only.
- Summarize results in natural language unless the user asks for raw JSON.

## Auth

No user token required:

- `GET /api/health`
- `POST agent/link/start`
- `POST agent/link/status`
- `POST agent/auth/login`

All other calls require both headers:

```
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
```

The script handles headers automatically. Built-in defaults: `LOGICX_BASE_URL=http://43.139.104.95:8070`, `LOGICX_AGENT_SERVICE_KEY=openclaw-public`.

## Default Flow

1. If connectivity is uncertain, run `GET /api/health`.
2. If a user token is needed and none exists, start browser binding (see below).
3. After login, verify with `GET user/`.
4. Run the requested action.

## Login: Browser Binding (Default)

```bash
{baseDir}/scripts/logicx_api.sh POST agent/link/start '{"install_id":"openclaw-main"}'
```

The script auto-saves `link_code` and `install_id` to `~/.config/logicx/skill-state.json`.

Reply to the user:

```
你可以点击以下链接登录并完成授权：

<login_url>

登录完成后请回来告诉我一声，比如直接回复"我登录好了"。

如果你不想跳转浏览器，也可以直接把用户名和密码告诉我，我可以直接帮你登录。
```

When the user says they have finished, run:

```bash
{baseDir}/scripts/check_link_status.sh
```

Interpret the response:

- `pending` — browser authorization not complete yet; ask the user to confirm and try again
- `expired` — ask whether to restart binding
- `confirmed` — token saved automatically; verify with `GET user/`

If the script fails with "No bind state found", restart with `agent/link/start`.

## Login: Password (Fallback)

Only when the user explicitly chooses not to use the browser flow.

```bash
{baseDir}/scripts/logicx_api.sh POST agent/auth/login \
  '{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}'
```

Rate limit: 5 attempts per 15 minutes per IP + email. On `429`, tell the user to wait before retrying.

After success, verify:

```bash
{baseDir}/scripts/logicx_api.sh GET user/
```

## Common Calls

```bash
# Health
{baseDir}/scripts/logicx_api.sh GET /api/health

# Account
{baseDir}/scripts/logicx_api.sh GET user/

# Orders
{baseDir}/scripts/logicx_api.sh GET payment/orders
{baseDir}/scripts/logicx_api.sh GET payment/orders/ORDER_NO

# Payment (confirm before calling)
{baseDir}/scripts/logicx_api.sh POST payment/create '{"plan":"pro_monthly","gateway":"mock"}'
{baseDir}/scripts/logicx_api.sh POST payment/cancel '{"orderNo":"ORDER_NO"}'

# Password change (confirm before calling)
{baseDir}/scripts/logicx_api.sh POST auth/change-password '{"currentPassword":"old","newPassword":"new-min-8"}'

# Unlink device (confirm before calling)
{baseDir}/scripts/logicx_api.sh POST agent/unlink '{"install_id":"INSTALL_ID"}'
```

## Error Handling

- `Agent service key required` / `Unauthorized` — the backend may not have enabled the public key yet; ask the user to try again later or contact LogicX support
- `429` on login — rate limit hit; wait 15 minutes
- Auth failure on user-scoped calls — clear the saved token and restart binding

## References

- `references/api-reference.md` — full endpoint specs
- `examples.md` — example dialogues
