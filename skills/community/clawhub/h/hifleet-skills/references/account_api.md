# 账户与用量 API / Account & Usage API

OpenClaw **api_key** 用户自助查询：当前可用积分、调用汇总、单次调用明细、积分入账/出账流水。**均需 `api_key`**；**查询本身不扣积分**（`@OpenClawAuthOnly`）。

**相关文档**（全链路）：

| 文档 | 内容 | 状态 |
|------|------|------|
| [FIRST_SETUP.md](../FIRST_SETUP.md) | 无 Key 时入门：注册 → 配置 → 充值 → 发票 | 流程指南 |
| [account_onboarding_api.md](account_onboarding_api.md) | 注册、登录、api_key 发放 | **已实现** |
| [billing_api.md](billing_api.md) | 积分充值、订阅套餐、收银台支付、混合额度、发票 | **已实现** |
| 本文 | 积分余额、调用记录、流水查询 | **已实现** |

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 **`HIFLEET_API_BASE`**（无末尾 `/`）。见 [api_base.md](api_base.md)。

---

## 鉴权

与船位、档案等 OpenClaw 接口相同：

| 方式 | 示例 |
|------|------|
| Query | `?api_key=sk_live_xxx` 或 `?sk=sk_live_xxx` |
| Header | `x-api-key: sk_live_xxx` |
| Bearer | `Authorization: Bearer sk_live_xxx` |

---

## Agent 路由（必守）

| 用户问什么 | 优先接口 | 说明 |
|------------|----------|------|
| 还剩多少积分、还能不能用 | **`/openclaw/account/summary`** | 向用户说明余额时**只引用 `availablePoints`**，勿自行用 `accountBalance` 与 `pendingDeduction` 加减 |
| 最近调用了哪些接口、用了多少 | **`/openclaw/account/usage/details`** | 单次请求明细；读 `agentSummary` 与 `items[].itemSummary` |
| 按小时汇总、统计趋势 | `/openclaw/account/usage` | 小时级汇总 |
| 什么时候真正扣款/充值 | **`/openclaw/account/transactions`** | 账本流水；`direction=OUT` 为出账 |

**三类数据不要混为一谈**：

1. **调用明细**（`usage/details`）：每次 API 请求的记录，可能有小时级延迟  
2. **调用汇总**（`usage`）：按小时聚合  
3. **积分流水**（`transactions`）：账户真正入账/出账  

用户问「扣了多少钱/积分」时：若明细已有、流水还没有 → 说明**待入账**，小时结算后会出现在 `transactions`。

---

## 1. 账户积分概览 / Summary

### 请求

| 项目 | 值 |
|------|-----|
| URL | `{base}/openclaw/account/summary` |
| 方法 | `GET` 或 `POST` |
| 鉴权 | `api_key`（必填） |

### 响应 `data` 主要字段

| 字段 | 说明 |
|------|------|
| **`availablePoints`** | **当前还可调用接口的积分（主字段）** |
| `accountBalance` | 账户已入账余额 |
| `pendingDeduction` | 待入账消耗；**仅当 > 0 时出现** |
| `totalUsedPoints` | 累计已使用积分（可选） |
| **`agentSummary`** | **可直接转述给用户的自然语言摘要** |
| `fieldGuide` | 字段含义（供 Agent 理解） |
| `balanceHint` | 余额字段关系补充说明 |
| `tokenId` / `tokenPrefix` / `tokenLast4` | 当前 Key 标识（勿向用户泄露完整 Key） |

### Agent 话术

- 优先朗读或改写 **`data.agentSummary`**。  
- 用户只问「还能用多少」→ 答 **`availablePoints` + 单位「积分」**。  
- 若存在 `pendingDeduction`：说明「最近调用中有 X 分尚未入账，结算后会从账户余额扣除；当前以 availablePoints 为准仍可继续调用」。  
- **禁止**向用户解释 `unsettledLimit`、内部结算状态等运维概念（用户接口已不返回）。

---

## 2. 调用汇总（按小时）/ Usage

### 请求

| 项目 | 值 |
|------|-----|
| URL | `{base}/openclaw/account/usage` |
| 方法 | `GET` 或 `POST` |

### Query 参数（均可选）

| 参数 | 说明 |
|------|------|
| `api_key` | 必填 |
| `capabilityCode` | 按能力编码筛选 |
| `requestUri` | 按路径筛选 |
| `settlementStatus` | 结算状态（高级筛选用，一般不对用户强调） |
| `createdDate` | 自然日 `yyyy-MM-dd` |
| `startAt` / `endAt` | 时间范围；**均不传时默认最近 24 小时** |

### 响应 `data` 结构

| 字段 | 说明 |
|------|------|
| `queryRange` | 本次查询时间范围描述 |
| `totalCount` / `totalCalls` / `totalChargedPoints` | 汇总统计 |
| **`agentSummary`** | 整页自然语言摘要 |
| `items[]` | 小时汇总列表 |
| `items[].summaryHour` | 汇总小时 |
| `items[].requestUri` / `capabilityCode` | 接口标识 |
| `items[].totalCalls` / `successCalls` / `failedCalls` | 次数 |
| `items[].chargedPoints` | 该小时计费积分 |
| `items[].itemSummary` | 单条自然语言摘要 |

---

## 3. 调用明细 / Usage details

### 请求

| 项目 | 值 |
|------|-----|
| URL | `{base}/openclaw/account/usage/details` |
| 方法 | `GET` 或 `POST` |

### Query 参数（均可选）

| 参数 | 说明 |
|------|------|
| `api_key` | 必填 |
| `capabilityCode` / `requestUri` | 筛选 |
| `callStatus` | `SUCCESS` / `FAILED` |
| `createdDate` | 自然日 |
| `startAt` / `endAt` | 时间范围；默认最近 24 小时 |
| `summaryHour` | 指定某汇总小时内的明细 |
| `limit` | 条数上限，默认 500，最大 500 |

### 响应 `data` 结构

| 字段 | 说明 |
|------|------|
| `totalCount` / `successCalls` / `failedCalls` / `totalChargedPoints` | 汇总 |
| **`agentSummary`** | 整页摘要 |
| `items[].requestId` | 请求 ID |
| `items[].requestUri` / `httpMethod` | 接口 |
| `items[].chargedPoints` | 本次计费积分 |
| `items[].callStatus` | 成功/失败 |
| `items[].createdAt` | 调用时间 |
| `items[].itemSummary` | 单条摘要 |

---

## 4. 积分流水 / Transactions

### 请求

| 项目 | 值 |
|------|-----|
| URL | `{base}/openclaw/account/transactions` |
| 方法 | `GET` 或 `POST` |

### Query 参数

| 参数 | 说明 |
|------|------|
| `api_key` | 必填 |
| `limit` | 默认 100，最大 200 |

### 响应 `data` 结构

| 字段 | 说明 |
|------|------|
| `totalInPoints` / `totalOutPoints` | 入账/出账合计 |
| **`agentSummary`** | 整页摘要 |
| `items[].direction` | `IN` 入账 / `OUT` 出账 |
| `items[].points` | 变动积分（绝对值） |
| `items[].balanceAfter` | 变动后账户余额 |
| `items[].remark` | 备注 |
| `items[].createdAt` | 流水时间 |
| `items[].itemSummary` | 单条摘要 |

---

## 调用示例

```bash
# 查余额（Agent 优先读 agentSummary）
curl -s "{base}/openclaw/account/summary" -H "x-api-key: $HIFLEET_API_KEY"

# 查今天调用明细
curl -s -G "{base}/openclaw/account/usage/details" \
  -H "x-api-key: $HIFLEET_API_KEY" \
  --data-urlencode "createdDate=2026-06-29" \
  --data-urlencode "limit=50"

# 查积分流水
curl -s -G "{base}/openclaw/account/transactions" \
  -H "x-api-key: $HIFLEET_API_KEY" \
  --data-urlencode "limit=20"
```

---

## 失败说明

| 场景 | 表现 | Agent 动作 |
|------|------|------------|
| 未传 `api_key` | `status=0`，提示 `api_key is required` | 引导 [FIRST_SETUP.md](../FIRST_SETUP.md) 注册或配置 Key |
| Key 无效/禁用/过期 | HTTP 401/403，`code=4004` | 引导重新登录或轮换 Key |
| 未绑定积分账户 | `summary` 余额可能为 0；`transactions` 为空并带说明性 `agentSummary` | 说明账户未初始化，联系支持或重新注册 |
| **积分不足**（业务接口） | HTTP 402，`code=4021` | 先调本文 `summary` 与 `billing/subscription` → 引导 [billing_api.md](billing_api.md) 充值或续订 |
| `availablePoints <= 0` | `summary` 返回 0 | 同上；若有订阅可能是周期额度用尽 |

---

## 数据范围

- 调用汇总/明细：仅**当前 api_key 对应 Token** 的记录  
- 积分流水：该 Token 绑定的 **pointUserId** 账户  

勿伪造积分、调用次数或流水。
