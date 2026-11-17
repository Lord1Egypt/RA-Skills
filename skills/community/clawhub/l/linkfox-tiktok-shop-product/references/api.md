# TikTok Shop ERP Product API Reference

本文档是 **`linkfox-tiktok-shop-product`** 的接口总览与转发说明。
**每个接口的完整官方参数/响应/错误码**见 `references/apis/<api>.md`（已从 Partner Center 原文整理并加上 LinkFox 转发映射）。

> ⚠️ 依赖 **`linkfox-tiktok-shop-auth`**（`appType=erp`）。

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

> ⚠️ **ACCESS_TOKEN 已后台化**：勿传 `ttsAccessToken`（即使传入也会被忽略）。业务调用**不要**先调 `/storeTokens` 或 `/refreshToken`；普通取 token 也不会按过期时间提前刷新。

### developerProxy 入参

| 参数 | 必填 | 说明 |
|------|------|------|
| path | 是 | TikTok 相对路径，**不含**主机名 |
| method | 是 | `GET` / `POST` / `PUT` / `DELETE` |
| openId | 是 | 卖家 open_id；网关据此取库中 token |
| appType | 是 | **固定 `erp`** |
| region | 否 | 默认 `global`，美国站 `us` |
| queryString | 视接口 | 不含 `?`；多数需 `shop_cipher` |
| body | 视接口 | JSON 字符串 |
| contentType | 否 | 默认 `application/json` |
| ttsAccessToken | 否 | **已废弃**，忽略 |

### 网关响应

| 字段 | 说明 |
|------|------|
| httpStatus | 上游 HTTP 状态 |
| body | TikTok 业务 JSON 字符串（含 `code`/`message`/`data`） |
| errcode | 网关错误；**1005**=path 未白名单 |

### path 白名单

- `authorization/`
- `product/`

### shop_cipher

1. 调 `get_authorized_shops` → `data.shops[].cipher`
2. 写入后续请求 Query：`shop_cipher=<cipher>`
3. 多店必须显式指定；单店脚本可自动解析

---

## 2. 接口索引（完整定义点进子文档）

| api | Method | path | shop_cipher | 完整参考 | 官方 |
|-----|--------|------|-------------|----------|------|
| `get_authorized_shops` | GET | `authorization/202309/shops` | 否 | [Get Authorized Shops](apis/get_authorized_shops.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309) |
| `check_listing_prerequisites` | GET | `product/202312/prerequisites` | 是 | [Check Listing Prerequisites](apis/check_listing_prerequisites.md) | [doc](https://partner.tiktokshop.com/docv2/page/check-listing-prerequisites-202312) |
| `get_categories` | GET | `product/202309/categories` | 是 | [Get Categories](apis/get_categories.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-categories-202309) |
| `get_category_rules` | GET | `product/202309/categories/{category_id}/rules` | 是 | [Get Category Rules](apis/get_category_rules.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-category-rules-202309) |
| `get_attributes` | GET | `product/202309/categories/{category_id}/attributes` | 是 | [Get Attributes](apis/get_attributes.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-attributes-202309) |
| `recommend_category` | POST | `product/202309/categories/recommend` | 是 | [Recommend Category](apis/recommend_category.md) | [doc](https://partner.tiktokshop.com/docv2/page/recommend-category-202309) |
| `get_brands` | GET | `product/202309/brands` | 是 | [Get Brands](apis/get_brands.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-brands-202309) |
| `search_products` | POST | `product/202502/products/search` | 是 | [Search Products](apis/search_products.md) | [doc](https://partner.tiktokshop.com/docv2/page/search-products-202502) |
| `get_product` | GET | `product/202309/products/{product_id}` | 是 | [Get Product](apis/get_product.md) | [doc](https://partner.tiktokshop.com/docv2/page/get-product-202309) |
| `create_product` | POST | `product/202309/products` | 是 | [Create Product](apis/create_product.md) | [doc](https://partner.tiktokshop.com/docv2/page/create-product-202309) |
| `edit_product` | PUT | `product/202309/products/{product_id}` | 是 | [Edit Product](apis/edit_product.md) | [doc](https://partner.tiktokshop.com/docv2/page/edit-product-202309) |
| `partial_edit_product` | POST | `product/202309/products/{product_id}/partial_edit` | 是 | [Partial Edit Product](apis/partial_edit_product.md) | [doc](https://partner.tiktokshop.com/docv2/page/partial-edit-product-202309) |
| `check_product_listing` | POST | `product/202309/products/listing_check` | 是 | [Check Product Listing](apis/check_product_listing.md) | [doc](https://partner.tiktokshop.com/docv2/page/check-product-listing-202309) |
| `activate_product` | POST | `product/202309/products/activate` | 是 | [Activate Product](apis/activate_product.md) | [doc](https://partner.tiktokshop.com/docv2/page/activate-product-202309) |
| `deactivate_products` | POST | `product/202309/products/deactivate` | 是 | [Deactivate Products](apis/deactivate_products.md) | [doc](https://partner.tiktokshop.com/docv2/page/deactivate-products-202309) |
| `update_price` | POST | `product/202309/products/{product_id}/prices/update` | 是 | [Update Price](apis/update_price.md) | [doc](https://partner.tiktokshop.com/docv2/page/update-price-202309) |
| `update_inventory` | POST | `product/202309/products/{product_id}/inventory/update` | 是 | [Update Inventory](apis/update_inventory.md) | [doc](https://partner.tiktokshop.com/docv2/page/update-inventory-202309) |
| `delete_products` | DELETE | `product/202309/products` | 是 | [Delete Products](apis/delete_products.md) | [doc](https://partner.tiktokshop.com/docv2/page/delete-products-202309) |
| `recover_products` | POST | `product/202309/products/recover` | 是 | [Recover Products](apis/recover_products.md) | [doc](https://partner.tiktokshop.com/docv2/page/recover-products-202309) |
| `upload_product_image` | POST | `product/202309/images/upload` | 是 | [Upload Product Image](apis/upload_product_image.md) | [doc](https://partner.tiktokshop.com/docv2/page/upload-product-image-202309) |
| `upload_product_file` | POST | `product/202309/files/upload` | 是 | [Upload Product File](apis/upload_product_file.md) | [doc](https://partner.tiktokshop.com/docv2/page/upload-product-file-202309) |

### 推荐主链路

```
get_authorized_shops → shop_cipher
  → check_listing_prerequisites
  → get_categories / recommend_category / get_attributes / get_brands
  → check_product_listing → create_product → activate_product
  → search_products / get_product / update_price / update_inventory …
```

### 通用调用

```bash
python scripts/product_api.py '{"api":"check_listing_prerequisites","openId":"...","shop_cipher":"GCP_..."}'
python scripts/product_proxy.py '{"openId":"...","path":"product/202312/prerequisites","method":"GET","shop_cipher":"GCP_..."}'
```

---

## 3. Feedback

- POST `https://skill-api.linkfox.com/api/v1/public/feedback`
- `skillName`: `linkfox-tiktok-shop-product`

## 4. Notes

1. 上传类接口（`upload_product_image` / `upload_product_file`）为 multipart，当前 `developerProxy` 字符串 body **暂不可调用**；文档仍收录供对照。
2. Create/Edit 的嵌套 SKU/图片结构以对应 `apis/*.md` 官方原文为准。
3. 勿输出完整 ERP token。
