---
name: lt99
description: >-
  模拟场玩家用站内 API Key 调 $LT99：Bearer 访问 /sim/state、enter、bet、history；GET /sim/watch 观战。
  在用户已邮箱注册、持有 Key、要让 Agent 代调练习盘接口时使用；只信 HTTP JSON。
version: 1.4.1
homepage: https://github.com/luyao-inc/LT99
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://github.com/luyao-inc/LT99
    requires:
      anyBins:
        - curl
---

# $LT99 模拟场（API Key）

## 前提

用户在 **`roundgame-agent.json` → `agent.game_page`** 对应站点 **邮箱注册**，在账户里领取 **API Key**。Agent 只负责用 Key 调接口，**不描述**站内注册 UI。

## `{base}`

默认 **`agent.services_base`**（见同目录 `roundgame-agent.json`）。可被 **`LT99_SERVICES_BASE_URL` / `SERVICES_BASE_URL`** 覆盖。

## 鉴权

所有需身份的请求加：

```http
Authorization: Bearer <用户提供的 API Key>
```

**`GET /sim/watch`** 可不带头（公开观战）。

若接口仍接受 `wallet` 参数，须与 Key 绑定身份一致；**优先只带 Bearer**，由服务端解析身份。

## 执行顺序

1. `GET {base}/sim/watch`  
2. `GET {base}/sim/state`（Bearer）  
3. 需要时 `POST {base}/sim/enter`，body 常用 `{}`，`Content-Type: application/json`（Bearer）  
4. 开放窗内 `POST {base}/sim/bet`，body：`{"digit":1-100,"amount":"<wei 整数字符串>"}`。`amount` 为 **vUSDT 最小单位（wei）**：18 位小数时 **100 vUSDT** = `100000000000000000000`（见 `roundgame-agent.json` 的 `min_bet_wei` 与 `min_bet_note`）  
5. `GET {base}/sim/history?limit=80`（Bearer）查看结算  

遇 **402** `sim_pass_required`：停止自动下注，说明须按站内规则处理。

## curl 示例

```bash
BASE="https://www.earninghub.ai/lt99-api"
KEY="<用户的 API Key>"

curl -sS "$BASE/sim/watch"
curl -sS -H "Authorization: Bearer $KEY" "$BASE/sim/state"
curl -sS -X POST "$BASE/sim/enter" -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d "{}"
curl -sS -X POST "$BASE/sim/bet" -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"digit":7,"amount":"100000000000000000000"}'
curl -sS -H "Authorization: Bearer $KEY" "$BASE/sim/history?limit=80"
```

## 禁止

遵守 `roundgame-agent.json` 中 **`forbidden_inferences`** 与 **`forbidden_user_facing_claims`**。
