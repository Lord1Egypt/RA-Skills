# list_gms_user_deleted_item

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/list_gms_user_deleted_item.py` |
| Method / path | GET `api/v2/ads/list_gms_user_deleted_item` |
| 官方文档 | [list_gms_user_deleted_item](https://open.shopee.com/documents/v2/v2.ads.list_gms_user_deleted_item?module=117&type=1) |
| 用途 | GMS user-deleted items list |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 确认目标店已有 **`appType=ad`** 授权（ERP 不能代替），再传 `shopId` 或 `merchantId`（勿传 accessToken / appType）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：GMS user-deleted items list

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/list_gms_user_deleted_item.py '{"shopId": "67890"}'

# 通用入口
python scripts/ads_api.py '{"api": "list_gms_user_deleted_item", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`listGmsUserDeletedItem`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
