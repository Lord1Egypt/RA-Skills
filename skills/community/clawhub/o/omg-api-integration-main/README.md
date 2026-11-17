# OMG Game Aggregation Platform — API Integration Guide

![OMG API](https://img.shields.io/badge/OMG-API_Integration-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Docs](https://img.shields.io/badge/Official_Docs-docs.omgapi.cc-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> **For AI Agents & LLMs**: This repository contains a complete, structured API integration reference for the **OMG Game Aggregation Platform** (`docs.omgapi.cc`). It covers MD5 signature authentication, Single Wallet mode, Transfer Wallet mode, `ingame` / `entergame` flows, `verify_session`, `change_balance`, `authorize`, `transfer`, bet record queries, RTP control, and full error code handling. The primary skill file is [`OMG_API_接入_SKILL.md`](./OMG_API_接入_SKILL.md).

---

## What is OMG?

**OMG** (docs.omgapi.cc) is a professional game aggregation platform that provides third-party merchants with a unified API to access a wide variety of game content, including:

- **Slots** — classic and video slot machines
- **Fishing Games** — skill-based arcade fishing titles
- **Mass Table Games (百人场)** — multi-player table games
- **Mini Games** — lightweight casual game modules

Merchants integrate once and gain access to the full OMG game library, with centralized wallet management, bet record reporting, and player RTP control.

---

## Wallet Integration Modes

OMG supports two mutually exclusive wallet architectures. Choose **one** based on your business requirements:

| Dimension | Single Wallet (单一钱包) | Transfer Wallet (转账钱包) |
|---|---|---|
| Balance owner | Merchant | OMG platform |
| Enter game API | `/api/usr/ingame` | `/api/game/v1/entergame` |
| Token source | Merchant's own auth system | OMG `/api/player/v1/authorize` |
| Balance change | OMG calls back merchant (`change_balance`) | Merchant calls OMG (`/api/cash/v1/transfer`) |
| Callbacks required | `verify_session`, `get_balance`, `change_balance` | None |
| Best for | Merchants with an existing unified wallet | Merchants who prefer OMG to manage game funds |

---

## Key Technical Points

### 1. MD5 Signature (Critical)

Every request must be signed using the following formula:

```
sign = md5( URL_query_string + raw_body_JSON + secret_key )
```

- The MD5 result must be **lowercase hex**.
- The `body` must be the **original raw JSON bytes** — never re-serialize after parsing, as field order or spacing changes will break the signature.
- The `sign` value is placed in the **HTTP request header**, not the body.

### 2. Response Code Convention

The `code` field meaning differs by interface direction — a common source of bugs:

| Interface Type | Success Code |
|---|---|
| Merchant → OMG (game APIs) | `code = 0` |
| OMG → Merchant callbacks (Single Wallet) | `code = 1` |
| Backend / report APIs (`OMG_BACKEND_URL`) | `code = 1` |

### 3. Data Types & Timezone

- All balance/amount fields (`balance`, `money`, `bet`, `win`) are **string decimals** with up to 4 decimal places. Never parse as `float`.
- All timestamps are **Unix seconds in UTC+0**.
- Player tokens expire after **7 days**.
- `order_id` / `tx_id` must be globally unique and serve as idempotency keys.

---

## API Quick Reference

### Merchant → OMG (success: `code=0`)

| Mode | API | Path | Purpose |
|---|---|---|---|
| Common | Get game list | `{OMG_API_URL}/api/game/loadlist` | Fetch available games |
| Single Wallet | Enter game | `{OMG_API_URL}/api/usr/ingame` | Get game URL |
| Transfer Wallet | Generate token | `{OMG_API_URL}/api/player/v1/authorize` | Create player + get token |
| Transfer Wallet | Transfer funds | `{OMG_API_URL}/api/cash/v1/transfer` | Deposit / withdraw |
| Transfer Wallet | Enter game | `{OMG_API_URL}/api/game/v1/entergame` | Get game URL |
| Transfer Wallet | Query balance | `{OMG_API_URL}/api/cash/v1/getPlayerWallet` | Player wallet balance |
| Transfer Wallet | Transfer status | `{OMG_API_URL}/api/cash/v1/transfer/status` | 0=fail 1=ok 2=pending |
| Report | Bet records | `{OMG_BACKEND_URL}/api/v1/merchant/outer/record/GetGameRecordList` | Pull bet history |

### OMG → Merchant Callbacks (Single Wallet only, success: `code=1`)

| API | Path (merchant implements) | Triggered when |
|---|---|---|
| Verify session | `{AGENT_URL}/api/luck/user/verify_session` | Player enters game |
| Get balance | `{AGENT_URL}/api/luck/balance/get_balance` | OMG needs to display balance |
| Change balance | `{AGENT_URL}/api/luck/balance/change_balance` | Bet / payout / cancel |

---

## Common Pitfalls

| Symptom | Root Cause | Fix |
|---|---|---|
| Always returns `10002 sign invalid` | Body re-serialized before signing | Use the raw request bytes for signing |
| Sign correct but still fails | URL query not included in sign string | Concatenation order: query + raw body + key |
| OMG keeps retrying merchant callback | Merchant returned `code=0` instead of `code=1` | Callbacks must return `code=1` on success |
| Duplicate deductions | No idempotency on `order_id` | Add unique constraint on `order_id` |
| Amount precision loss | Parsed balance as `float` | Use string/Decimal, 4 decimal places |
| Token suddenly invalid | Token expired (> 7 days) | Re-call `authorize` (Transfer) or re-call `ingame` (Single) |

---

## Repository Contents

| File | Description |
|---|---|
| [`README.md`](./README.md) | This file — English overview and quick reference |
| [`README_CN.md`](./README_CN.md) | Chinese version of this guide |
| [`OMG_API_接入_SKILL.md`](./OMG_API_接入_SKILL.md) | **Full integration skill** — complete API specs, request/response examples, error codes, and Go code snippets |

---

## Official Documentation

| Topic | URL |
|---|---|
| Quick Start | https://docs.omgapi.cc/kuai-su-kai-shi/quickstart.md |
| Error Codes | https://docs.omgapi.cc/kuai-su-kai-shi/tong-yong-cuo-wu-ma.md |
| Flow Diagrams | https://docs.omgapi.cc/kuai-su-kai-shi/liu-cheng-tu.md |
| Game List | https://docs.omgapi.cc/kuai-su-kai-shi/you-xi-lie-biao.md |
| Currency List | https://docs.omgapi.cc/kuai-su-kai-shi/huo-bi-lie-biao.md |
| Online Debugger | https://docs.omgapi.cc/openapi-jie-kou-zai-xian-tiao-shi/ |
| Full Sitemap | https://docs.omgapi.cc/sitemap.md |

> English docs are available by replacing the path prefix with `/en/`, e.g. `https://docs.omgapi.cc/en/quick-start/quickstart.md`

---

## Contact

For business inquiries and integration support:

- **Telegram**: [@omgapi666](https://t.me/omgapi666)
- **Official Docs**: https://docs.omgapi.cc

---

## License

This repository is provided as a reference integration guide. All API specifications belong to the OMG platform. See [LICENSE](./LICENSE) for details.
