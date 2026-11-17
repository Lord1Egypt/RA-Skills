---
name: omg-api-integration
description: Use when 第三方对接 OMG 游戏 API（docs.omgapi.cc），涉及签名鉴权、单一钱包/转账钱包模式选择、ingame 进入游戏、verify_session 用户验证、change_balance 余额变动、authorize 鉴权 token、transfer 转账、注单查询、RTP 点控、错误码处理等场景
---

# OMG 游戏 API 对接参考

OMG（docs.omgapi.cc）是一个游戏聚合平台，提供 SLOTS、捕鱼、百人场、MiniGame 等游戏。接入分两种钱包模式，**二选一**：

- **单一钱包**：玩家钱包在接入方（商户）侧，OMG 通过回调向接入方查询和扣减余额
- **转账钱包**：玩家钱包在 OMG 侧，接入方主动调用 OMG 完成转入/转出

本文为单文件完整参考，按需跳转目录。

## 目录

1. 接入前必读约定（域名、签名、请求格式、code 含义、金额时区）
2. 单一钱包 vs 转账钱包 — 选择决策
3. 接口速查表
4. 单一钱包模式 — 接口详情
5. 转账钱包模式 — 接口详情
6. 报表与功能接口
7. 错误码完整表
8. 常见陷阱与排查指南
9. 文档地址对照

---

## 一、接入前必读约定

### 1. 三个域名（来自 OMG 商户后台）

| 占位符 | 用途 | 说明 |
|---|---|---|
| `{OMG_API_URL}` | OMG 游戏接口域名 | 接入方调用 OMG 的游戏类接口 |
| `{OMG_BACKEND_URL}` | OMG 后台接口域名 | 调用注单/报表等后台接口 |
| `{AGENT_URL}` | 接入方回调地址 | 接入方在 OMG 后台填写，OMG 调接入方时用 |

### 2. 签名算法（最大陷阱）

公式：

```
sign = md5( url参数字符串 + body的JSON字符串 + 签名密钥key )
```

- **md5 结果转小写**
- **body 必须用「请求中最原始的 JSON 字符」**，不要先 `json.Unmarshal` 再 `json.Marshal` 重新序列化（字段顺序、空格会变，导致签名失败）
- `key` 由 OMG 平台提供（商户后台获取）
- sign 放在 **HTTP header**，不是 body

**签名样例**：

```
URL:  {OMG_API_URL}/api/luck/Balance/GetBalance?trace_id=dhf1aboc1iio
key:  39a6581c31ef3203a22edb2daa2ab6d1
拼接: trace_id=dhf1aboc1iio{"player_logon_token":"...","account_id":"1002402","timestamp":1711971655}39a6581c31ef3203a22edb2daa2ab6d1
sign: e3f8dc79e875e46f6755ef540c2d24f3
```

**Go 实现要点（发送请求，避开重新序列化陷阱）**：

```go
// 发送请求时
bodyBytes := []byte(`{"player_logon_token":"...","account_id":"1002402","timestamp":1711971655}`) // 原始字节
// 或直接拼接 string，确保字段顺序、空格与最终发送的 body 完全一致

urlQuery := "trace_id=" + traceID
toSign := urlQuery + string(bodyBytes) + key
sign := fmt.Sprintf("%x", md5.Sum([]byte(toSign))) // 小写 hex

req, _ := http.NewRequest("POST", url+"?"+urlQuery, bytes.NewReader(bodyBytes))
req.Header.Set("Content-Type", "application/json; charset=utf-8")
req.Header.Set("sign", sign)
```

**Go 实现要点（接收 OMG 回调，验签）**：

```go
bodyBytes, _ := io.ReadAll(c.Request.Body)                  // 必须读取原始字节
c.Request.Body = io.NopCloser(bytes.NewReader(bodyBytes))   // 复位供后续 bind
recvSign := c.GetHeader("sign")
expected := fmt.Sprintf("%x", md5.Sum([]byte(c.Request.URL.RawQuery + string(bodyBytes) + key)))
if recvSign != expected { /* 返回 10002 */ }
```

> 关键：**先读原始字节，再做反序列化**。框架自带 bind 通常会消费 body，需要先把字节缓存下来用于验签，再写回 Request.Body。

### 3. 请求格式

| 项 | 值 |
|---|---|
| 方法 | `POST`（除非接口另有说明） |
| Content-Type | `application/json; charset=utf-8` |
| Header `sign` | MD5 签名值 |
| URL Query | `?trace_id=xxx`（每次请求唯一随机） |
| Body | JSON 对象 |

### 4. 响应 code 含义（容易混淆，必看）

| 接口类型 | 成功码 |
|---|---|
| **OMG 提供给接入方调用**（接入方 → OMG，游戏类接口） | `code = 0` |
| **接入方实现给 OMG 回调**（OMG → 接入方，单一钱包） | `code = 1` |
| **后台/报表类接口**（OMG_BACKEND_URL） | `code = 1` |

> 写代码前先判断接口方向，code 值不同。错了会被 OMG 当作失败重试。

通用响应结构：

```json
{
  "code": 0,
  "msg": "ok",
  "data": { /* 业务数据 */ }
}
```

### 5. 数据类型 / 时区

- **金额**：所有 `balance`/`money`/`amount`/`bet`/`win` 都是 `string` 类型的 decimal，**最多 4 位小数**，禁止当 float 解析
- **时间**：`timestamp` 为秒级整数；**所有时间统一 UTC+0**
- **token 有效期**：7 天，过期需重新获取
- **`uname`**：接入方提供的用户 ID，全局唯一
- **`order_id` / `tx_id`**：接入方产生，最长 64 位，必须唯一，用作幂等键

---

## 二、单一钱包 vs 转账钱包 — 选择决策

| 维度 | 单一钱包 | 转账钱包 |
|---|---|---|
| 玩家余额持有方 | 接入方维护 | OMG 维护 |
| 进入游戏接口 | OMG `/api/usr/ingame` | OMG `/api/game/v1/entergame` |
| 鉴权 token 获取 | 接入方自有体系 | 先调 OMG `/api/player/v1/authorize` 拿 token |
| 余额变动方式 | OMG 回调接入方 `change_balance` 实时扣加 | 接入方主动调 OMG `/api/cash/v1/transfer` 转入/转出 |
| 接入方需实现的回调 | `verify_session`、`get_balance`、`change_balance` | 无回调，只主动调 OMG |
| 适用场景 | 接入方有完整钱包系统，希望维持唯一资金账本 | 接入方接受 OMG 托管游戏资金，简化集成 |

---

## 三、接口速查表

### OMG 主动提供（接入方 → OMG，成功码 `code=0`）

| 模式 | 接口 | 路径 | 用途 |
|---|---|---|---|
| 通用 | 获取游戏列表 | `{OMG_API_URL}/api/game/loadlist` | 拉取可用游戏 |
| 单一钱包 | 请求进入游戏 | `{OMG_API_URL}/api/usr/ingame` | 拿 game url |
| 转账钱包 | 生成 token | `{OMG_API_URL}/api/player/v1/authorize` | 创建玩家 + 拿 token |
| 转账钱包 | 转账 | `{OMG_API_URL}/api/cash/v1/transfer` | 转入/转出 |
| 转账钱包 | 进入游戏 | `{OMG_API_URL}/api/game/v1/entergame` | 拿 game url |
| 转账钱包 | 查询余额 | `{OMG_API_URL}/api/cash/v1/getPlayerWallet` | 玩家余额 |
| 转账钱包 | 查询转账状态 | `{OMG_API_URL}/api/cash/v1/transfer/status` | 0=失败 1=成功 2=Pending |
| 转账钱包 | 查询离线非零余额 | `{OMG_BACKEND_URL}/api/v1/merchant/outer/queryOfflinePlayerBalance` | 对账用（成功码 `code=1`） |
| 报表 | 注单记录 | `{OMG_BACKEND_URL}/api/v1/merchant/outer/record/GetGameRecordList` | 拉取明细（成功码 `code=1`） |

### 接入方需实现给 OMG 回调（OMG → 接入方，成功码 `code=1`，仅单一钱包）

| 接口 | 路径（接入方实现） | 何时被调 |
|---|---|---|
| 用户身份验证 | `{AGENT_URL}/api/luck/user/verify_session` | 玩家进入游戏后 OMG 验证 token |
| 获取用户余额 | `{AGENT_URL}/api/luck/balance/get_balance` | OMG 显示余额时调 |
| 改变用户余额 | `{AGENT_URL}/api/luck/balance/change_balance` | 下注、派奖、取消时调（核心） |

---

## 四、单一钱包模式 — 接口详情

> 玩家余额在接入方维护。OMG 通过回调向接入方查询和扣减余额。

### 调用链路

```
1. 接入方调 OMG: /api/usr/ingame         → 拿到 gameurl
2. 玩家访问 gameurl 进入游戏
3. OMG 回调接入方: /api/luck/user/verify_session       (验证 token)
4. OMG 回调接入方: /api/luck/balance/get_balance       (查询余额，按需)
5. OMG 回调接入方: /api/luck/balance/change_balance    (下注/派奖/取消)
```

接入方必须实现第 3、4、5 三个回调，并在响应中返回 `code=1` 表示成功。

### 1. 请求进入游戏（接入方 → OMG）

**URL**：`{OMG_API_URL}/api/usr/ingame?trace_id=xxx`　**方法**：POST

**Headers**：

```
Content-Type: application/json; charset=utf-8
sign: <md5 签名>
```

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `gameid` | string | 是 | 游戏 ID（来自游戏列表） |
| `token` | string | 是 | 用户验证 token（接入方自有） |
| `nick` | string | 是 | 用户昵称，最长 40 字节 |
| `lang` | string | 否 | 游戏语言，默认 `en` |
| `cid` | integer | 否 | 货币 ID；多货币商户必传，单货币传 0 |
| `back_url` | string | 否 | 玩家退出回调 URL（仅特定品牌有效） |
| `screen_mode` | string | 是 | 1=竖屏全屏 / 2=半屏 / 3=横屏全屏（仅 Casino、Lottery 有效） |

**响应**：

```json
{
  "code": 0,
  "msg": "success",
  "data": { "gameurl": "https://m.pgf-aspb7a-test.cc/1/index.html?..." }
}
```

> 注意：本接口由接入方调 OMG，成功码为 `code=0`。

### 2. 用户身份验证（接入方实现，OMG 回调）

**URL**（接入方实现）：`{AGENT_URL}/api/luck/user/verify_session?trace_id=xxx`　**方法**：POST

**请求体（OMG 发过来）**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `timestamp` | integer | 是 | 时间戳（秒） |
| `operator_player_session` | string | 是 | 接入方在 ingame 接口传的 `token` |
| `game_id` | integer | 否 | 游戏 ID |
| `ip` | string | 否 | 用户 IP |
| `custom_parameter` | string | 否 | 接入方额外参数 |

**接入方需返回**：

```json
{
  "code": 1,
  "msg": "ok",
  "data": {
    "uname": "10003803",
    "nickname": "bill",
    "balance": "42766.25"
  }
}
```

| 字段 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `uname` | 是 | string | 用户 ID，**必须全局唯一** |
| `nickname` | 是 | string | 用户昵称 |
| `balance` | 是 | string (decimal) | 余额，最多 4 位小数 |

> 成功码：`code=1`。失败示例：`{"code":10002,"msg":"sign invalid"}`

### 3. 获取用户余额（接入方实现，OMG 回调）

**URL**（接入方实现）：`{AGENT_URL}/api/luck/balance/get_balance?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `uname` | string | 是 | 接入方提供的用户 ID（与 verify_session 返回值一致） |
| `timestamp` | integer | 是 | 时间戳（秒） |
| `game_id` | integer | 否 | 游戏 ID |
| `player_login_token` | string | 否 | 接入方上传的用户 token |

**接入方需返回**：

```json
{ "code": 1, "msg": "ok", "data": { "balance": "4299.12" } }
```

### 4. 改变用户余额（接入方实现，OMG 回调）— 核心

**URL**（接入方实现）：`{AGENT_URL}/api/luck/balance/change_balance?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 说明 |
|---|---|---|
| `app_id` | string | 商户唯一标识 |
| `uname` | string | 用户 ID |
| `money` | string (decimal) | 余额变动量；**正数加、负数扣** |
| `game_id` | integer | 游戏 ID |
| `session_id` | string | 游戏主局号 |
| `round_id` | string | 游戏副局号 |
| `order_id` | string | 订单号；最长 64 位；**全局唯一，幂等键** |
| `timestamp` | integer | 时间戳（秒） |
| `bet` | string (decimal) | 下注金额（始终正数；仅下注时有值） |
| `type` | integer | 交易类型，见下表 |
| `end_round` | bool | 当前局是否结束 |
| `cancel_order_id` | string | 仅 `type=2` 时有值，被取消订单的 ID |
| `award_order_ids` | array | 仅 `type=3` 时有值，每笔下注的派奖明细 |

**type 取值**：

| type | 含义 | money 符号 | 配套字段 |
|---|---|---|---|
| 1 | 游戏下注 | 负 | `bet`（正数下注额）、`end_round` |
| 2 | 取消下注（回滚） | 正 | `cancel_order_id`（被取消的订单 ID） |
| 3 | 游戏返奖 | 正 | `award_order_ids`（每笔下注对应的派奖明细数组） |
| 4 | 验证对局结束 | 0 | `end_round` |
| 5 | LuckWin 宝箱奖励 | 正 | — |
| 7 | WG 品牌活动派奖 | 正 | — |

**请求示例（type=1 下注）**：

```json
{
  "app_id": "10013",
  "bet": "3",
  "game_id": 74,
  "money": "-3",
  "order_id": "20240716195311drxaoz1mxx6g",
  "session_id": "1813180074526625845",
  "round_id": "1813180074526625845",
  "timestamp": 1721130791,
  "uname": "1006417",
  "end_round": false,
  "type": 1
}
```

**请求示例（type=3 派奖，含多笔下注对应）**：

```json
{
  "app_id": "10013",
  "money": "33.66",
  "order_id": "20240715204114drtuiv8r7ny8",
  "type": 3,
  "award_order_ids": [
    {"order_id": "20240715204030drtugi3tau4g", "money": "5.1"},
    {"order_id": "20240715204053drtuhqp0jthc", "money": "10.2"}
  ]
}
```

**`award_order_ids` 语义说明**：

- 这是**本次派奖事件所对应的「已发生下注」明细**，并非历史所有下注
- 每一项的 `order_id` 必须是接入方之前已经成功扣款入账的下注订单 ID（type=1 时存的）
- 每一项的 `money` 是该下注产生的派奖额（**正数**）；外层 `money` 一般等于 `award_order_ids` 中所有 `money` 之和（以 OMG 实际下发为准）
- 接入方做法：在派奖入账时记录派奖明细，便于对账与回滚
- 如果任一 `order_id` 在接入方查无下注记录，应拒绝本次派奖（返回错误码），避免凭空派奖

**接入方需返回**：

```json
{ "code": 1, "msg": "ok", "data": { "balance": "4289.15" } }
```

余额不足应返回 `{"code":10001,"msg":"balance is not enough"}`。

**幂等实现要点**：

1. 用 `order_id` 做唯一键（数据库 unique 约束 或 Redis SETNX）
2. 同一 `order_id` 二次到达 → 直接查表返回首次的 `balance`，**不要再扣加**
3. `type=2` 退款需校验 `cancel_order_id` 已扣款且未退过
4. `type=3` 派奖必须匹配 `award_order_ids` 中所有 `order_id` 已存在

---

## 五、转账钱包模式 — 接口详情

> 玩家余额在 OMG 维护。接入方在玩家进出游戏时主动调 OMG 完成转入/转出。**所有接口由接入方调 OMG，成功码均为 `code=0`**（离线余额查询接口除外，见第 6 节）。

### 调用链路

```
1. 接入方调 OMG: /api/player/v1/authorize     → 创建/获取玩家 token
2. 接入方调 OMG: /api/cash/v1/transfer        → 转入金额（amount 为正）
3. 接入方调 OMG: /api/game/v1/entergame       → 拿到 gameurl
4. 玩家访问 gameurl 游戏
5. 玩家退出后:
   - 接入方调 OMG: /api/cash/v1/getPlayerWallet  → 查询当前余额
   - 接入方调 OMG: /api/cash/v1/transfer         → 转出余额（amount 为负）
6. 异步对账: /api/cash/v1/transfer/status     → 确认转账最终状态
              /api/v1/merchant/.../queryOfflinePlayerBalance → 查离线非零用户
```

### 1. 生成用户鉴权 token

**URL**：`{OMG_API_URL}/api/player/v1/authorize?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `uname` | string | 是 | 用户 ID，**必须全局唯一** |
| `nickname` | string | 是 | 用户昵称，最长 40 字节 |
| `timestamp` | integer | 是 | 时间戳（秒） |
| `cid` | integer | 否 | 货币 ID，多货币商户必传 |

**响应**：

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "token": "1003803",
    "balance": "42766.25",
    "app_id": 10013
  }
}
```

> token 有效期 **7 天**，过期需重新调用。

### 2. 余额转入/转出

**URL**：`{OMG_API_URL}/api/cash/v1/transfer?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `token` | string | 是 | 玩家 token（来自 authorize） |
| `amount` | string (decimal) | 是 | **正数=转入（加钱）；负数=转出（扣钱）**；最多 4 位小数 |
| `tx_id` | string | 是 | 转账流水号；**由接入方产生，必须全局唯一**（幂等键） |
| `timestamp` | integer | 是 | 时间戳（秒） |

**响应**：

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "tx_id": "etx0917yn",
    "ptx_id": "1849761935796461568",
    "state": 1
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `tx_id` | string | 回显接入方传入的流水号 |
| `ptx_id` | string | OMG 平台流水号 |
| `state` | integer | 转账状态：**0=失败，1=成功** |

**幂等要点**：

- 接入方对 `tx_id` 做唯一约束
- **若超时未拿到响应，必须用 `tx_id` 调 `/transfer/status` 确认最终状态，不要直接重试**（重试可能用新 `tx_id` 造成重复转账）

### 3. 进入游戏

**URL**：`{OMG_API_URL}/api/game/v1/entergame?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `token` | string | 是 | 玩家 token |
| `gameid` | string | 是 | 游戏 ID |
| `timestamp` | integer | 是 | 时间戳（秒） |
| `screen_mode` | string | 是 | 1=竖屏 / 2=半屏 / 3=横屏 |
| `lang` | string | 否 | 游戏语言，默认 en |
| `back_url` | string | 否 | 玩家退出回调 URL |

**响应**：

```json
{ "code": 0, "msg": "ok", "data": { "gameurl": "https://m.pgf-aspb7a-test.cc/..." } }
```

### 4. 查询用户余额

**URL**：`{OMG_API_URL}/api/cash/v1/getPlayerWallet?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `token` | string | 是 | 玩家 token |
| `timestamp` | integer | 是 | 时间戳（秒） |

**响应**：

```json
{ "code": 0, "msg": "ok", "data": { "balance": "4299.18" } }
```

### 5. 查询转账状态（对账关键）

**URL**：`{OMG_API_URL}/api/cash/v1/transfer/status?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `token` | string | 是 | 玩家 token |
| `tx_id` | string | 是 | 接入方调 transfer 时产生的流水号 |
| `timestamp` | integer | 是 | 时间戳（秒） |

**响应**：

```json
{ "code": 0, "msg": "ok", "data": { "amount": "4299.18", "state": 1 } }
```

| state | 含义 |
|---|---|
| 0 | 失败 |
| 1 | 成功 |
| 2 | Pending（仍在处理） |

> Pending 状态需轮询直到变为 0/1，**不可视为最终态**。

### 6. 查询不在线且余额不为 0 用户（对账）

**URL**：`{OMG_BACKEND_URL}/api/v1/merchant/outer/queryOfflinePlayerBalance`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户唯一标识 |
| `currency_id` | integer | 是 | 单货币商户填 0；多货币商户填货币 ID；0 表示全部货币 |

**响应**：

```json
{
  "code": 1,
  "msg": "success",
  "data": [
    {
      "agent_id": 461559,
      "uid": 395983,
      "account_id": 1080019,
      "account_name": "1242132177",
      "balance": 99949
    }
  ]
}
```

> 该接口在后台域名（OMG_BACKEND_URL），**成功码为 `code=1`**。
> 主要用途：扫描"玩家已下线但 OMG 侧仍有余额"的情况，定期发起转出回流到接入方钱包。

---

## 六、报表与功能接口

> 所有报表接口域名为 `{OMG_BACKEND_URL}`（后台域名）。**本组接口成功码为 `code=1`**（与转账钱包模式相反，注意区分）。

### 1. 注单记录 GetGameRecordList

**URL**：`{OMG_BACKEND_URL}/api/v1/merchant/outer/record/GetGameRecordList?trace_id=xxx`　**方法**：POST

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 商户 appid |
| `page` | integer | 是 | 页码（从 1 开始） |
| `size` | integer | 是 | 每页条数，**最大 1000** |
| `start_time` | integer | 是 | 起始时间戳（秒，**UTC+0**） |
| `end_time` | integer | 是 | 结束时间戳（秒，**UTC+0**） |
| `uname` | string | 否 | 用户 ID |
| `game_id` | string | 否 | 游戏 ID |

**请求示例**：

```json
{
  "app_id": "10013",
  "uname": "1004613",
  "game_id": "10049",
  "start_time": 1742541848,
  "end_time": 1842541848,
  "page": 1,
  "size": 2
}
```

**响应**：

```json
{
  "code": 1,
  "msg": "success",
  "total": 230862,
  "data": [
    {
      "create_time": 1733746183,
      "round_id": 1866092861616992266,
      "round_id_str": "1866092861616992266",
      "account": "1233212142",
      "account_id": "1070800",
      "game_id": "31067",
      "enter_money": 47762.54,
      "bet": 0,
      "win": 0,
      "after_settlement_money": 47762.54,
      "id": 1866092861671518211,
      "id_str": "1866092861671518211",
      "parent_id": 1866092861524717568,
      "parent_id_str": "1866092861524717568",
      "small_game_type": 2,
      "fb": 0,
      "platform": 5
    }
  ]
}
```

**注单字段说明**：

| 字段 | 类型 | 含义 |
|---|---|---|
| `create_time` | integer | 注单创建时间戳（秒） |
| `round_id` / `round_id_str` | integer / string | 牌局唯一标识（数值 + 字符串双格式） |
| `account` | string | 玩家昵称/账号 |
| `account_id` | string | 玩家账户 ID |
| `game_id` | string | 游戏 ID |
| `enter_money` | decimal | 进入游戏时的余额 |
| `bet` | decimal | 本局下注金额 |
| `win` | decimal | 本局派奖金额 |
| `after_settlement_money` | decimal | 结算后玩家余额 |
| `id` / `id_str` | integer / string | 注单记录唯一 ID |
| `parent_id` / `parent_id_str` | integer / string | 上级牌局 ID |
| `small_game_type` | integer | 0=正常、1=连消、2=免费旋转、3=重转、4=高倍 |
| `fb` | integer | 是否购买小游戏 0=否、1=是 |
| `platform` | integer | 游戏平台代码 |

**输赢计算**：

```
玩家输赢 = win - bet
```

**拉单纪律**：

- 大数据量场景需循环到 `data` 为空为止
- **每次拉单间隔 ≥ 500ms**（频控）
- 响应**不返回总页数**，需用 `total` 自行计算或用「空数组」作为结束信号

### 2. 玩家点控（RTP 调控）

按玩家+游戏维度调整 RTP（Return To Player）目标。
文档：`https://docs.omgapi.cc/bao-biao-ji-gong-neng-jie-kou/wan-jia-dian-kong-rtp-tiao-kong.md`

可能返回的特殊错误码：`20005` 未查询到游戏此 RTP 配置信息 / `20006` 商户未配置此游戏 / `20007` 此游戏未配置 RTP

### 3. 新玩家自动养客

控制新玩家进入后的初始返水节奏。
文档：`https://docs.omgapi.cc/bao-biao-ji-gong-neng-jie-kou/xin-wan-jia-zi-dong-yang-ke.md`

### 4. 设置/取消 玩家养客、杀客

针对特定玩家的人工策略干预。
- 设置：`https://docs.omgapi.cc/bao-biao-ji-gong-neng-jie-kou/she-zhi-wan-jia-yang-ke-sha-ke.md`
- 取消：`https://docs.omgapi.cc/bao-biao-ji-gong-neng-jie-kou/qu-xiao-wan-jia-yang-ke-sha-ke.md`

---

## 七、错误码完整表

### code 成功值速记

| 接口类别 | 成功值 |
|---|---|
| OMG 主动提供（接入方 → OMG，游戏类接口） | `code = 0` |
| 接入方实现的回调（OMG → 接入方，单一钱包） | `code = 1` |
| 后台/报表类接口（OMG_BACKEND_URL） | `code = 1` |

### 通用错误码（10xxx，游戏 API + 单一钱包回调）

| code | 含义 |
|---|---|
| 1 | 成功（回调接口） |
| 10001 | 余额不足，下分失败 |
| 10002 | 签名验证未通过 |
| 10003 | 订单正在处理中 |
| 10004 | 订单不存在 |
| 10005 | 订单重复 |
| 10006 | 请求过于频繁 |
| 10007 | 游戏中不能上下分 |
| 10008 | 游戏已关闭 |
| 10009 | 非法参数 |
| 10010 | 失败 |
| 10011 | 玩家登录 token 验证失败 |
| 10012 | 非法的 app_id |
| 10013 | 玩家不存在 |
| 10014 | 玩家被禁止登录 |
| 10015 | 服务器内部错误 |
| 10016 | 游戏不存在 |
| 10017 | 游戏未开通 |
| 10018 | 商户已被禁用 |
| 10019 | 不支持的货币 |
| 10020 | 转账交易不存在 |
| 10021 | 商户钱包类型不正确 |
| 10022 | 传入的 appid 对应的商户不存在 |
| 10023 | 参数类型不匹配 |

### 特殊错误码（20xxx，报表/风控类接口）

| code | 含义 |
|---|---|
| 1 | 成功 |
| 20001 | 商户不存在 |
| 20003 | 查询条数超过限制 |
| 20004 | 商户用户信息不一致，请核对用户信息 |
| 20005 | 未查询到游戏此 RTP 配置信息 |
| 20006 | 商户未配置此游戏 |
| 20007 | 此游戏未配置 RTP |
| 20008 | 签名错误 |
| 20009 | 读取 body 失败 |
| 20010 | 签名不合法 |
| 20011 | 商户已关闭 |
| 20012 | 流水号错误 |
| 20013 | 参数错误 |

### 排查指引

| 错误码 | 优先排查项 |
|---|---|
| 10002 / 20008 / 20010 | 1) body 是否用原始字符串签名；2) URL query 是否拼入；3) 密钥是否正确；4) trace_id 是否传入 |
| 10003 | 同一 `order_id` / `tx_id` 正在处理中，**等待并查询状态**，不要重复提交 |
| 10004 / 10020 | 订单/流水不存在，可能时间太久或 ID 错；先用 `transfer/status` 确认 |
| 10005 | `order_id` 重复，业务侧需保证 ID 唯一；幂等情况应返回首次结果 |
| 10006 | 调用频率超限，加退避重试 |
| 10011 | token 失效（过期/被刷新），重新调 authorize（转账钱包）或重新走 ingame（单一钱包） |
| 10015 | OMG 服务端异常，可重试，必要时联系 OMG |
| 10019 | `cid` 货币 ID 不在商户开通列表中，确认开通货币 |
| 10021 | 接入方调错钱包模式接口（单一/转账），确认商户配置 |
| 10022 | `app_id` 与实际商户不匹配 |
| 20003 | `size` 超 1000 或时间范围过大，缩小查询窗口 |

---

## 八、常见陷阱与排查指南

| 现象 | 可能原因 | 排查 |
|---|---|---|
| 始终返回 `10002 sign invalid` | body 被重新序列化导致字符串变化 | 用「请求字面字符串」参与签名，而非重新 Marshal |
| sign 计算正确但仍失败 | url 参数没拼上，或 `trace_id` 没传 | 拼接顺序：URL query + body 原文 + key |
| 接入方实现的接口被 OMG 反复重试 | 返回了 `code=0`，OMG 期望 `code=1` | 接入方回调接口成功返回 `code=1` |
| 同一笔下注重复扣款 | 未做 `order_id` 幂等 | 用 `order_id` 做唯一约束/去重 |
| 派奖金额与下注 ID 对应不上 | `award_order_ids` 未解析 | type=3 时遍历 `award_order_ids` 数组 |
| 跨日数据偏差 | 用了本地时区 | 所有时间按 UTC+0 计算 |
| 金额精度丢失 | 当成 float 解析 | 使用 decimal/string，4 位小数 |
| token 突然失效 | 超过 7 天 | 转账钱包需重新调 authorize |
| 多货币商户 `cid` 传错 | 默认传 0 | 多货币商户必传 cid，单货币传 0 |
| 转账超时后重复转账 | 超时直接重试用了新 `tx_id` | 超时改调 `/transfer/status` 用原 `tx_id` 确认 |

---

## 九、文档地址对照

| 主题 | 中文文档 URL |
|---|---|
| 接入说明 | https://docs.omgapi.cc/kuai-su-kai-shi/quickstart.md |
| 通用错误码 | https://docs.omgapi.cc/kuai-su-kai-shi/tong-yong-cuo-wu-ma.md |
| 流程图 | https://docs.omgapi.cc/kuai-su-kai-shi/liu-cheng-tu.md |
| 游戏列表（编号） | https://docs.omgapi.cc/kuai-su-kai-shi/you-xi-lie-biao.md |
| 货币列表 | https://docs.omgapi.cc/kuai-su-kai-shi/huo-bi-lie-biao.md |
| 多语言编码表 | https://docs.omgapi.cc/kuai-su-kai-shi/duo-yu-yan-bian-ma-biao.md |
| 在线调试 | https://docs.omgapi.cc/openapi-jie-kou-zai-xian-tiao-shi/ |
| 完整 sitemap | https://docs.omgapi.cc/sitemap.md |

> 英文版替换路径前缀为 `/en/`，例如 `https://docs.omgapi.cc/en/quick-start/quickstart.md`。
