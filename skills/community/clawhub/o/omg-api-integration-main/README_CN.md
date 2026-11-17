# OMG 游戏聚合平台 — API 对接指南

![OMG API](https://img.shields.io/badge/OMG-API_Integration-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Docs](https://img.shields.io/badge/官方文档-docs.omgapi.cc-orange.svg)

> **面向 AI 智能体**：本仓库包含 OMG 游戏聚合平台（docs.omgapi.cc）的完整 API 对接参考，涵盖 MD5 签名鉴权、单一钱包/转账钱包模式选择、ingame 进入游戏、verify_session 用户验证、change_balance 余额变动、authorize 鉴权 token、transfer 转账、注单查询、RTP 点控及错误码处理等全部场景。核心文件为 [`OMG_API_接入_SKILL.md`](./OMG_API_接入_SKILL.md)。

---

## OMG 平台简介

**OMG**（docs.omgapi.cc）是一个专业的游戏聚合平台，为第三方商户提供统一 API 接入丰富的游戏内容，包括：

- **SLOTS（老虎机）** — 经典及视频老虎机
- **捕鱼游戏** — 技巧类街机捕鱼
- **百人场** — 多人桌面游戏
- **MiniGame（小游戏）** — 轻量休闲游戏模块

商户一次接入即可获得 OMG 完整游戏库，并享有集中式钱包管理、注单报表和玩家 RTP 调控能力。

---

## 钱包接入模式

OMG 支持两种互斥的钱包架构，根据业务需求**二选一**：

| 维度 | 单一钱包 | 转账钱包 |
|---|---|---|
| 余额持有方 | 商户 | OMG 平台 |
| 进入游戏接口 | `/api/usr/ingame` | `/api/game/v1/entergame` |
| Token 来源 | 商户自有鉴权体系 | OMG `/api/player/v1/authorize` |
| 余额变动方式 | OMG 回调商户 `change_balance` | 商户主动调 OMG `/api/cash/v1/transfer` |
| 需实现的回调 | `verify_session`、`get_balance`、`change_balance` | 无 |
| 适用场景 | 已有完整钱包系统的商户 | 接受 OMG 托管游戏资金的商户 |

---

## 关键技术要点

### 1. MD5 签名（最大陷阱）

所有请求必须按以下公式签名：

```
sign = md5( URL参数字符串 + body原始JSON字符串 + 签名密钥key )
```

- MD5 结果必须为**小写十六进制**。
- `body` 必须使用**原始请求字节**，不要先解析再重新序列化，否则字段顺序/空格变化会导致签名失败。
- `sign` 放在 **HTTP 请求 Header** 中，不在 body 里。

### 2. 响应 code 含义（容易混淆）

`code` 字段含义因接口方向不同而不同：

| 接口类型 | 成功码 |
|---|---|
| 商户 → OMG（游戏类接口） | `code = 0` |
| OMG → 商户回调（单一钱包） | `code = 1` |
| 后台/报表类接口（OMG_BACKEND_URL） | `code = 1` |

### 3. 数据类型与时区

- 所有金额字段（`balance`、`money`、`bet`、`win`）均为**字符串 decimal**，最多 4 位小数，禁止当 float 解析。
- 所有时间戳为 **UTC+0 秒级整数**。
- 玩家 token 有效期 **7 天**。
- `order_id` / `tx_id` 必须全局唯一，作为幂等键使用。

---

## 接口速查表

### 商户 → OMG（成功码 `code=0`）

| 模式 | 接口 | 路径 | 用途 |
|---|---|---|---|
| 通用 | 获取游戏列表 | `{OMG_API_URL}/api/game/loadlist` | 拉取可用游戏 |
| 单一钱包 | 请求进入游戏 | `{OMG_API_URL}/api/usr/ingame` | 获取游戏 URL |
| 转账钱包 | 生成 token | `{OMG_API_URL}/api/player/v1/authorize` | 创建玩家 + 获取 token |
| 转账钱包 | 转账 | `{OMG_API_URL}/api/cash/v1/transfer` | 转入/转出 |
| 转账钱包 | 进入游戏 | `{OMG_API_URL}/api/game/v1/entergame` | 获取游戏 URL |
| 转账钱包 | 查询余额 | `{OMG_API_URL}/api/cash/v1/getPlayerWallet` | 玩家钱包余额 |
| 转账钱包 | 查询转账状态 | `{OMG_API_URL}/api/cash/v1/transfer/status` | 0=失败 1=成功 2=处理中 |
| 报表 | 注单记录 | `{OMG_BACKEND_URL}/api/v1/merchant/outer/record/GetGameRecordList` | 拉取注单明细 |

### OMG → 商户回调（仅单一钱包，成功码 `code=1`）

| 接口 | 路径（商户实现） | 触发时机 |
|---|---|---|
| 用户身份验证 | `{AGENT_URL}/api/luck/user/verify_session` | 玩家进入游戏时 |
| 获取用户余额 | `{AGENT_URL}/api/luck/balance/get_balance` | OMG 需要展示余额时 |
| 改变用户余额 | `{AGENT_URL}/api/luck/balance/change_balance` | 下注/派奖/取消时 |

---

## 常见陷阱

| 现象 | 原因 | 解决方案 |
|---|---|---|
| 始终返回 `10002 sign invalid` | body 被重新序列化 | 用原始请求字节参与签名 |
| 签名正确但仍失败 | URL query 未拼入签名 | 拼接顺序：query + body 原文 + key |
| OMG 反复重试商户回调 | 商户返回了 `code=0` | 回调接口成功必须返回 `code=1` |
| 同一笔下注重复扣款 | 未做 `order_id` 幂等 | 对 `order_id` 加唯一约束 |
| 金额精度丢失 | 当成 float 解析 | 使用 string/Decimal，保留 4 位小数 |
| token 突然失效 | 超过 7 天过期 | 转账钱包重新调 `authorize`，单一钱包重新走 `ingame` |

---

## 仓库内容

| 文件 | 说明 |
|---|---|
| [`README.md`](./README.md) | 英文版概览与快速参考（默认展示） |
| [`README_CN.md`](./README_CN.md) | 本文件 — 中文版指南 |
| [`OMG_API_接入_SKILL.md`](./OMG_API_接入_SKILL.md) | **完整对接 Skill** — 包含所有接口规范、请求/响应示例、错误码及 Go 代码片段 |

---

## 官方文档地址

| 主题 | URL |
|---|---|
| 接入说明 | https://docs.omgapi.cc/kuai-su-kai-shi/quickstart.md |
| 通用错误码 | https://docs.omgapi.cc/kuai-su-kai-shi/tong-yong-cuo-wu-ma.md |
| 流程图 | https://docs.omgapi.cc/kuai-su-kai-shi/liu-cheng-tu.md |
| 游戏列表 | https://docs.omgapi.cc/kuai-su-kai-shi/you-xi-lie-biao.md |
| 货币列表 | https://docs.omgapi.cc/kuai-su-kai-shi/huo-bi-lie-biao.md |
| 在线调试 | https://docs.omgapi.cc/openapi-jie-kou-zai-xian-tiao-shi/ |
| 完整 sitemap | https://docs.omgapi.cc/sitemap.md |

---

## 商务联系

如需商务合作或对接技术支持：

- **Telegram**: [@omgapi666](https://t.me/omgapi666)
- **官方文档**: https://docs.omgapi.cc

---

## License

本仓库作为对接参考指南提供，所有 API 规范归 OMG 平台所有。详见 [LICENSE](./LICENSE)。
