# get_penalty_point_history — 扣分历史

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_penalty_point_history.py` |
| Method / path | GET `api/v2/account_health/get_penalty_point_history` |
| 官方文档 | [v2.account_health.get_penalty_point_history](https://open.shopee.com/documents/v2/v2.account_health.get_penalty_point_history?module=103&type=1) |
| 用途 | 查询**当前季度**产生的扣分（penalty point）记录 |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `page_no` | int | 否 | 页码，从 **1** 起；默认 **1** |
| `page_size` | int | 否 | 每页条数，范围 **1–100**；默认 **10** |
| `violation_type` | int | 否 | 按违规类型筛选（见下表） |

- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query

### `violation_type` 常用值

| 值 | 说明 |
|----|------|
| `5` | High Late Shipment Rate |
| `6` | High Non-fulfilment Rate |
| `7` | High number of non-fulfilled orders |
| `8` | High number of late shipped orders |
| `9` | Prohibited Listings |
| `10` | Counterfeit / IP infringement |
| `11` | Spam |
| `12` | Copy/Steal images |
| `13` | Re-uploading deleted listings with no change |
| `16` | High percentage of pre-order listings |

完整枚举以官方文档为准。

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_penalty_point_history.py '{"shopId":"67890","page_no":1,"page_size":50}'

python scripts/get_penalty_point_history.py '{"shopId":"67890","violation_type":5,"page_size":20}'

python scripts/account_health_api.py '{"api":"get_penalty_point_history","shopId":"67890","page_size":50}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getPenaltyPointHistory`**
3. 常见字段：`total_count`、`penalty_point_list[]`（如 `issue_time`、`original_point_num`、`latest_point_num`、`violation_type`、`reference_id`）
