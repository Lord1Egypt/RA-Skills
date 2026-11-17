---
name: linkfox-tiktok-shop-product
description: TikTok Shop ERP 商品（Product）业务技能，经 /tiktokShop/developerProxy（appType=erp）转发 TikTok Product Open API：刊登前置检查、授权店铺 cipher、类目/属性/品牌、搜索/创建/编辑商品、刊登校验、上下架、改价改库存、删除恢复。依赖 linkfox-tiktok-shop-auth 选店（传 openId；token 后台化，勿手动 refresh）。当用户提到 TikTok 小店商品、ERP 商品、刊登前置条件、check listing prerequisites、创建商品、编辑商品、搜索商品、上架下架、改价、改库存、类目属性、品牌、product listing、TikTok Shop product API 时触发。**不含授权**（用 linkfox-tiktok-shop-auth）；**不含达人/视频号商品**（用 linkfox-tiktok-video-products）。
---

# TikTok Shop ERP 商品（Product）

本 skill 调用 TikTok Shop **卖家 ERP 商品**开放接口。统一经 LinkFox 网关：

```
linkfox-tiktok-shop-auth  →  openId（选店）
        ↓
POST /tiktokShop/developerProxy
  appType = erp
  openId  = <ERP openId>     # 网关从库取 token；ttsAccessToken 已废弃
  path / method / queryString / body
        ↓
401 或 token 失效 → 网关自动 refresh 并重试一次
        ↓
TikTok Open API → 网关透传 httpStatus + body
```

> 📌 **前置依赖**：`linkfox-tiktok-shop-auth`（固定 ERP）。勿用 `linkfox-tiktok-video-auth`。
> 📌 **勿手动刷新 token**：业务调用只需 `openId`；网关遇 401/过期会自动续签。
> 📌 **转发说明 + 接口索引**：`references/api.md`
> 📌 **每个接口的完整官方参数/响应/错误码**：`references/apis/<api>.md`（已收录 Partner Center 原文 + LinkFox 映射）

## Prerequisites

1. `python scripts/check_auth_dependency.py`；exit **42** → 先安装并完成 **`linkfox-tiktok-shop-auth`** 授权。
2. 本 skill **不实现**授权；也**不必**在调用前手动 `/refreshToken`。

## Core Concepts

| 概念 | 说明 |
|------|------|
| 转发入口 | 仅 `POST /tiktokShop/developerProxy`，**固定 `appType=erp`** |
| path | 相对路径，如 `product/202312/prerequisites`；白名单前缀 `product/`、`authorization/` |
| shop_cipher | 来自 `get_authorized_shops` 的 `data.shops[].cipher`；脚本在仅 1 店时可自动解析 |
| 签名 | 调用方**不要**传 `app_key`/`sign`/`timestamp`（紫鸟注入） |
| 响应 | 先看网关 `developerProxy.httpStatus`，再解析 `body` 内 TikTok `code`/`message` |

## Available Scripts

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测 `linkfox-tiktok-shop-auth` |
| `product_api.py` | 具名 API：`{"api":"...","openId":"..."}` |
| `product_proxy.py` | 通用 path/method 转发 |
| `get_authorized_shops.py` | 取店铺列表与 `cipher` |
| `check_listing_prerequisites.py` | 刊登前置检查 |
| `get_categories.py` / `get_category_rules.py` / `get_attributes.py` / `recommend_category.py` | 类目链路 |
| `get_brands.py` | 品牌 |
| `search_products.py` / `get_product.py` | 查询 |
| `create_product.py` / `edit_product.py` / `partial_edit_product.py` | 创建/编辑 |
| `check_product_listing.py` | 刊登校验 |
| `activate_product.py` / `deactivate_products.py` | 上下架 |
| `update_price.py` / `update_inventory.py` | 改价/库存 |
| `delete_products.py` / `recover_products.py` | 删除/恢复 |

共享模块：`_shop_product_common.py`、`_product_endpoints.py`、`_product_api_runner.py`。

## 标准流程

1. **`linkfox-tiktok-shop-auth`**：`authorized_stores` 选 ERP 店 → 得到 `openId`
2. （推荐）`get_authorized_shops` → 拿到 `shop_cipher`（多店必须显式传）
3. （推荐）`check_listing_prerequisites` → 全部 `is_failed=false` 再刊登
4. 类目/属性/品牌 → `create_product` / `check_product_listing` → `activate_product`
5. 日常：`search_products` / `update_price` / `update_inventory` / 上下架

## Usage Examples

```bash
# 1) 取 cipher
python scripts/get_authorized_shops.py '{"openId":"..."}'

# 2) 刊登前置检查
python scripts/check_listing_prerequisites.py '{"openId":"...","shop_cipher":"GCP_..."}'

# 3) 搜索商品
python scripts/search_products.py '{"openId":"...","page_size":20,"status":"ACTIVATE"}'

# 4) 具名 API
python scripts/product_api.py '{"api":"get_product","openId":"...","product_id":"1..."}'

# 5) 创建（复杂 body 用 requestBody）
python scripts/create_product.py '{"openId":"...","requestBody":{...}}'
```

## Display Rules

1. 勿输出完整 `accessToken` / 完整 `shop_cipher` 以外的敏感信息时可掩码 token。
2. 展示 `check_results` 时逐条说明 `check_item` + `fail_reasons`。
3. 网关 `errcode=1005` → path 未白名单，联系运维放行 `product/`、`authorization/`。

## Important Limitations

- **仅 ERP**：`appType` 固定 erp。
- **不含授权**；达人橱窗选品用 `linkfox-tiktok-video-products`。
- **Image/File Upload（multipart）** 暂未纳入可调用脚本（`developerProxy` body 为字符串）；创建商品需已有图片 URI。
- **Global Product** 跨境全球商品第二期再加。

## 积分消耗规则

不消耗积分（以网关实际计费为准；若返回积分不足按 onboarding 处理）。

**Feedback**：`skillName` = `linkfox-tiktok-shop-product`（见 `references/api.md`）。

---
*More skills: [LinkFox Skills](https://skill.linkfox.com/)*
