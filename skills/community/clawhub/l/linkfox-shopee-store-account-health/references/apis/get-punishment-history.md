# get_punishment_history — 处罚历史

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_punishment_history.py` |
| Method / path | GET `api/v2/account_health/get_punishment_history` |
| 官方文档 | [v2.account_health.get_punishment_history](https://open.shopee.com/documents/v2/v2.account_health.get_punishment_history?module=103&type=1) |
| 用途 | 查询**当前季度**处罚（punishment）记录 |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `punishment_status` | int | **是** | `1`=Ongoing（进行中），`2`=Ended（已结束） |
| `page_no` | int | 否 | 页码，从 **1** 起；默认 **1** |
| `page_size` | int | 否 | 每页条数，范围 **1–100**；默认 **10** |

- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query

### 常见 `punishment_type`（响应字段，节选）

| 值 | 说明 |
|----|------|
| `103` | Listings not displayed in category browsing |
| `104` | Listings not displayed in search |
| `105` | Unable to create new listings |
| `106` | Unable to edit listings |
| `107` | Unable to join marketing campaigns |
| `109` | Account is suspended |
| `1109–1112` | Listing Limit reduced |
| `2008` | Order Limit applied |

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 进行中的处罚
python scripts/get_punishment_history.py '{"shopId":"67890","punishment_status":1,"page_no":1,"page_size":20}'

# 已结束的处罚
python scripts/get_punishment_history.py '{"shopId":"67890","punishment_status":2,"page_size":50}'

python scripts/account_health_api.py '{"api":"get_punishment_history","shopId":"67890","punishment_status":1}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getPunishmentHistory`**
3. 常见字段：`punishment_list[]`（如 `punishment_type`、`reason`、`start_time`、`end_time`、`listing_limit`、`order_limit`）
