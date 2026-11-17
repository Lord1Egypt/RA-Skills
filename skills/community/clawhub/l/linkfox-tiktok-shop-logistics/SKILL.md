---
name: linkfox-tiktok-shop-logistics
description: TikTok Shop ERP 物流/仓库（Logistics）业务技能，经 /tiktokShop/developerProxy（appType=erp）转发 Logistics Open API：获取仓库列表（Get Warehouse List）。依赖 linkfox-tiktok-shop-auth 选店（传 openId；token 后台化，勿手动 refresh）。当用户提到 TikTok 小店仓库、仓库列表、Get Warehouse List、warehouse_id、销售仓/退货仓、多仓、logistics/warehouses、查店铺仓库 时触发。**不含授权**（用 linkfox-tiktok-shop-auth）；**不含订单/履约发货**（用 shop-order / shop-fulfillment）；运费模板/配送选项等可后续扩展本 skill。
---

# TikTok Shop ERP 物流/仓库（Logistics）

本 skill 调用 TikTok Shop **卖家 ERP 物流仓库**开放接口。统一经 LinkFox 网关：

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

> 📌 **前置依赖**：`linkfox-tiktok-shop-auth`（固定 ERP）。
> 📌 **勿手动刷新 token**：业务调用只需 `openId`；网关遇 401/过期会自动续签。
> 📌 **转发说明 + 索引**：`references/api.md`
> 📌 **完整官方参数/响应**：`references/apis/<api>.md`
> 📌 官方入口：[Get Warehouse List](https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309)

## Prerequisites

1. `python scripts/check_auth_dependency.py`；exit **42** → 先安装并完成 **`linkfox-tiktok-shop-auth`**。
2. 本 skill **不实现**授权；也**不必**在调用前手动 `/refreshToken`。

## Core Concepts

| 概念 | 说明 |
|------|------|
| 转发入口 | 仅 `POST /tiktokShop/developerProxy`，**固定 `appType=erp`** |
| path | 相对路径，如 `logistics/202309/warehouses`；白名单 `logistics/`、`authorization/` |
| shop_cipher | 来自 `get_authorized_shops`；单店可自动解析 |
| Get Warehouse List | 仅需 `shop_cipher`（Query）；返回仓库 id/name/type/address 等 |
| warehouse_id | 创建商品库存、改库存、多仓场景常用 |

## Available Scripts

| 脚本 | 作用 |
|------|------|
| `check_auth_dependency.py` | 检测 `linkfox-tiktok-shop-auth` |
| `logistics_api.py` | 具名 API |
| `logistics_proxy.py` | 通用 path/method |
| `get_authorized_shops.py` | 取 `shop_cipher` |
| `get_warehouse_list.py` | 仓库列表（[202309](https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309)） |

共享模块：`_shop_logistics_common.py`、`_logistics_endpoints.py`、`_logistics_api_runner.py`。

## 标准流程

1. **`linkfox-tiktok-shop-auth`** 选 ERP 店 → `openId`
2. `get_authorized_shops` → `shop_cipher`（多店必传）
3. `get_warehouse_list` 拿到 `warehouse_id`（以及 type / effect_status / is_default 等）
4. 下游刊登/改库存使用对应 `warehouse_id`（见 `linkfox-tiktok-shop-product`）

## Usage Examples

```bash
python scripts/get_authorized_shops.py '{"openId":"..."}'

python scripts/get_warehouse_list.py '{"openId":"..."}'

python scripts/logistics_api.py '{"api":"get_warehouse_list","openId":"...","shop_cipher":"GCP_..."}'
```

## Display Rules

1. 勿输出完整 accessToken。
2. 列表优先展示：`id`、`name`、`type`、`sub_type`、`effect_status`、`is_default`、地址摘要。
3. 网关 `errcode=1005` → 需放行 `logistics/`、`authorization/`。

## Important Limitations

- **仅 ERP 物流仓库域**（当前以仓库列表为主；配送选项/运费模板可后续扩展）。
- **不含**订单 list/detail（`linkfox-tiktok-shop-order`）。
- **不含**履约拆单/发货（`linkfox-tiktok-shop-fulfillment`）。
- **不含授权**。

## 积分消耗规则

不消耗积分（以网关实际为准）。

**Feedback**：`skillName` = `linkfox-tiktok-shop-logistics`。

---
*More skills: [LinkFox Skills](https://skill.linkfox.com/)*
