# TikTok Shop ERP Logistics API Reference

本文档是 **`linkfox-tiktok-shop-logistics`** 的接口总览与转发说明。
**每个接口的完整官方参数/响应/错误码**见 `references/apis/<api>.md`。

> ⚠️ 依赖 **`linkfox-tiktok-shop-auth`**（`appType=erp`）。
> 官方入口：[Get Warehouse List](https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309)。

---

## 1. 转发约定（Agent 必读）

### 调用链

```
linkfox-tiktok-shop-auth  →  openId（选店）
        ↓
POST /tiktokShop/developerProxy
  appType = erp
  openId  = <ERP openId>          # 网关按 openId+appType 从库取 token
  path / method / queryString / body
        ↓
若上游 401 或 token expired/invalid → 网关自动 refresh 并重试一次，回写库
        ↓
紫鸟注入 app_key / timestamp / sign → TikTok Open API
```

> ⚠️ **ACCESS_TOKEN 已后台化**：勿传 `ttsAccessToken`（即使传入也会被忽略）。业务调用**不要**先调 `/storeTokens` 或 `/refreshToken`。

### developerProxy 入参

| 参数 | 必填 | 说明 |
|------|------|------|
| path | 是 | 相对路径，不含主机名 |
| method | 是 | `GET` / `POST` |
| openId | 是 | 卖家 open_id；网关据此取库中 token |
| appType | 是 | **固定 `erp`** |
| region | 否 | 默认 `global`，美国站 `us` |
| queryString | 视接口 | 不含 `?`；物流 API 须含 `shop_cipher` |
| body | 视接口 | JSON 字符串 |
| ttsAccessToken | 否 | **已废弃**，忽略 |

### path 白名单

- `authorization/`
- `logistics/`

> 订单请用 **`linkfox-tiktok-shop-order`**；履约拆单请用 **`linkfox-tiktok-shop-fulfillment`**。

### shop_cipher

1. `get_authorized_shops` → `data.shops[].cipher`
2. Query：`shop_cipher=<cipher>`
3. 多店须显式传；单店脚本可自动解析

---

## 2. 接口索引

| api | Method | path | shop_cipher | 完整参考 | 官方 |
|-----|--------|------|-------------|----------|------|
| `get_authorized_shops` | GET | `authorization/202309/shops` | 否 | [Get Authorized Shops](apis/get_authorized_shops.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309) |
| `get_warehouse_list` | GET | `logistics/202309/warehouses` | 是 | [Get Warehouse List](apis/get_warehouse_list.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309) |

### 推荐链路

```
get_authorized_shops → shop_cipher
  → get_warehouse_list
  → （可选）linkfox-tiktok-shop-product 创建/改库存时传 warehouse_id
```

### 通用调用

```bash
python scripts/get_warehouse_list.py '{"openId":"..."}'
python scripts/logistics_api.py '{"api":"get_warehouse_list","openId":"..."}'
```

---

## 3. Feedback

- POST `https://skill-api.linkfox.com/api/v1/public/feedback`
- `skillName`: `linkfox-tiktok-shop-logistics`

## 4. Notes

1. Get Warehouse List **无业务 body**，仅 Query `shop_cipher`。
2. 上游 path 属于 **`logistics/`**。
3. 多仓刊登前应先取仓库列表，再把 `warehouse_id` 写入库存相关字段。
4. 勿输出完整 ERP token。
