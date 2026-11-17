# get_listings_with_issues — 问题 Listing

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_listings_with_issues.py` |
| Method / path | GET `api/v2/account_health/get_listings_with_issues` |
| 官方文档 | [v2.account_health.get_listings_with_issues](https://open.shopee.com/documents/v2/v2.account_health.get_listings_with_issues?module=103&type=1) |
| 用途 | 查询存在账户健康问题、需改进的 listing |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `page_no` | int | 否 | 页码，从 **1** 起；默认 **1** |
| `page_size` | int | 否 | 每页条数，范围 **1–100**；默认 **10** |

- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query

### 响应中 `reason` 常用值

| 值 | 说明 |
|----|------|
| `1` | Prohibited |
| `2` | Counterfeit |
| `3` | Spam |
| `4` | Inappropriate Image |
| `5` | Insufficient Info |
| `6` | Mall Listing Improvement |
| `7` | Other Listing Improvement |

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_listings_with_issues.py '{"shopId":"67890","page_no":1,"page_size":50}'

python scripts/account_health_api.py '{"api":"get_listings_with_issues","shopId":"67890","page_size":100}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getListingsWithIssues`**
3. 常见字段：`total_count`、`listing_list[]`（如 `item_id`、`reason`）
