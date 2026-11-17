# Skills 控制台 SSO（api_key 换票自动登录）

> **状态**：**已实现**

智能体已配置 `HIFLEET_API_KEY`（`sk_…`）时，用 **换票** 打开 Skills 控制台（用量 / 钱包 / 套餐 / API Key），**不要**再让用户走邮箱验证码或密码登录。

**API 基址**：`{base}`（默认 `https://api.hifleet.com`）；见 [api_base.md](api_base.md)。

相关文档：[account_onboarding_api.md](account_onboarding_api.md)、[account_api.md](account_api.md)、[billing_api.md](billing_api.md)。

## 两个域名（勿混用）

| 用途 | 域名 | 说明 |
|------|------|------|
| **换票 API** | `{base}`（默认 `https://api.hifleet.com`） | 仅服务端请求：`POST {base}/openclaw/account/session/from-api-key` |
| **用户浏览器** | `https://skills.hifleet.com` | 介绍页与控制台；打开返回的 `consoleUrl` |

| 页面 | URL |
|------|-----|
| 产品介绍 | `https://skills.hifleet.com/` → `/openclaw/index.html` |
| 控制台 | `https://skills.hifleet.com/openclaw/console.html` |
| 短链 | `https://skills.hifleet.com/console` → 控制台 |

换票在 **api**（`{base}`）上调用；用户打开的是 **skills.hifleet.com** 页面（含一次性 `ticket`）。  
控制台打开后会自行兑票登录；智能体通常**不必**再调 `from-ticket`。

## 推荐流程

```
智能体读取 HIFLEET_API_KEY
        │
        ▼
POST {base}/openclaw/account/session/from-api-key
     Authorization: Bearer sk_xxx
     Body: { "redirect": "/usage", "lang": "en" }   // lang 可选
        │
        ▼
取 data.consoleUrl（已含 ticket，可选带 lang；主机为 skills.hifleet.com）
        │
        ▼
用浏览器打开 consoleUrl（或把链接发给用户）
        │
        ▼
控制台按 URL 中的 lang 切换界面语言 → 自动兑 ticket → 写入 JWT → 擦除 URL 中的 ticket → 进入落地页
```

**安全**：

- URL 里只允许短时 **ticket**（默认约 120 秒、一次性），**禁止**把完整 `api_key` 塞进地址栏或聊天长期展示。
- `accessToken` 可出现在接口 JSON 里；**不要**在回复中完整回显 JWT / `sk_`。
- 优先把 **`consoleUrl`** 给用户点开即可。

## Agent 路由（必守）

| 用户说什么 | 优先动作 |
|------------|----------|
| 打开控制台、看用量、钱包、Skills 控制台、用 api_key 登录 | 本文 **换票** → 打开 `consoleUrl` |
| 介绍 / 什么是 HiFleet Skills | 给 `https://skills.hifleet.com/`（无需换票；可加 `?lang=`） |
| 没有 api_key、注册 | [account_onboarding_api.md](account_onboarding_api.md) / [FIRST_SETUP.md](../FIRST_SETUP.md) |
| 充值、订阅、发票 | [billing_api.md](billing_api.md) |

## 1. 换票 API

`POST {base}/openclaw/account/session/from-api-key`  
（也支持 `GET`，仍须带 key）

### 鉴权（任选其一）

| 方式 | 示例 |
|------|------|
| Header | `Authorization: Bearer sk_...` |
| Header | `x-api-key: sk_...` |
| Body | `{ "apiKey": "sk_..." }` 或 `{ "api_key": "sk_..." }` |
| Query | `api_key=sk_...`（易进访问日志，不推荐） |

### Body / Query（可选）

| 字段 | 说明 |
|------|------|
| `apiKey` / `api_key` | Header 未带 key 时可用 |
| `redirect` | 登录后 hash 落地页，默认 `/usage`；允许：`/usage` `/wallet` `/subscription` `/plans` `/api-keys` `/invoices` |
| `lang` / `locale` / `i18n` | 控制台界面语言（三选一即可，推荐 `lang`）。写入返回的 `consoleUrl`，页面打开后**优先**用该语言并记入本地偏好 |

#### 支持的语言码

| 值 | 语言 |
|----|------|
| `zh` | 简体中文（默认；别名如 `zh-CN` / `cn`） |
| `zh-TW` | 繁體中文（别名如 `zh-HK`） |
| `en` | English |
| `ja` | 日本語 |
| `es` | Español |
| `de` | Deutsch |
| `ru` | Русский |

非法或未知值会被忽略（不写入 `consoleUrl`）；介绍页/控制台再按 localStorage → 浏览器语言回退。

### 成功 `data` 字段

| 字段 | 说明 |
|------|------|
| `consoleUrl` | **优先使用**：已带 ticket（及可选 `lang`）的完整控制台链接 |
| `ticket` | 一次性兑换码（一般不必单独处理） |
| `ticketExpiresInSeconds` | ticket 有效秒数 |
| `accessToken` | 控制台 JWT（勿在聊天中展示） |
| `userId` / `email` | 绑定账户 |
| `tokenPrefix` / `tokenLast4` | 所用 key 摘要，便于核对 |
| `redirect` | 实际落地路径 |
| `lang` | 实际写入 URL 的语言码（仅当请求指定且合法时返回） |

示例（形态示意）：

```text
https://skills.hifleet.com/openclaw/console.html#/usage?ticket=<一次性票据>
https://skills.hifleet.com/openclaw/console.html#/usage?ticket=<一次性票据>&lang=en
```

### curl 示例

```bash
curl -sS -X POST "${HIFLEET_API_BASE:-https://api.hifleet.com}/openclaw/account/session/from-api-key" \
  -H "Authorization: Bearer $HIFLEET_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"redirect":"/usage","lang":"en"}'
```

### 失败常见码

| code | 含义 |
|------|------|
| `token_invalid` | key 无效或非 `sk_` |
| `token_disabled` / `token_expired` | key 停用或过期 |
| `point_user_id_unbound` | key 未绑定用户账户 |
| `redis_unavailable` | 会话临时不可用 |
| `ticket_invalid` | ticket 无效/已用/过期（兑票阶段） |

## 2. 控制台兑票（浏览器自动，智能体通常不用调）

`GET|POST {base}/openclaw/account/session/from-ticket`（skills 同源也可，由页面发起）

| 参数 | 说明 |
|------|------|
| `ticket` | Query 或 body |

兑换成功返回 `accessToken`、`userId`；**ticket 立即作废**。

调试兼容（勿用于生产跳转）：

- `#/usage?accessToken=JWT&userId=...`
- `#/usage?api_key=sk_...`（页面会立刻换票并擦除 URL；可同时带 `lang=`）

## 3. 直接打开页面并指定语言（无需换票）

介绍页与控制台均支持 URL 参数 `lang`（或 `locale` / `i18n`），优先级高于本地已存偏好：

```text
https://skills.hifleet.com/openclaw/?lang=ja
https://skills.hifleet.com/openclaw/console.html#/plans?lang=de
```

换票场景请优先在 **换票 Body** 传 `lang`，让服务端写进 `consoleUrl`，避免人工拼接。

## 4. 智能体动作清单

1. 确认已有 `HIFLEET_API_KEY`（`sk_` 开头）。
2. 对 `{base}` 调用换票接口；若已知用户界面语言偏好，一并传 `lang`（如英文用户用 `"lang":"en"`）。
3. 只把 `data.consoleUrl` 打开或发给用户（可简述「已生成一次性登录链接，约 2 分钟内有效」）。
4. 用户要看介绍而非登录态时，可给：`https://skills.hifleet.com/`（无需换票；需要时可加 `?lang=`）。

脚本：`scripts/open_console.py`

```bash
python scripts/open_console.py --redirect usage
python scripts/open_console.py --redirect wallet --print-only
```

## 触发词

控制台、Skills 控制台、账单、套餐用量、钱包、打开控制台、用 api_key 登录控制台、console SSO、skills.hifleet.com
