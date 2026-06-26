# Partner EU — Price 接口目录

Partner Platform for EU 菜单：**Price**（`menu_code=dfff38c23adf498d8a7cd55052bd3648`）。

文档根 `menu_code`（浏览器地址栏常见）：`7289390cfd724be4a196f11ebe45a896`。

本 skill 覆盖与 US 版对齐的 **4** 个价格/供货价 `type`。调用经 `temu_eu_proxy`（`POST /temu/proxy`），默认 **`site=eu`**。

> EU 菜单 HTML 导出中 **Price** 子项未完全展开，下列 4 个接口的 `sub_menu_code` 除已确认者外链至 **Price** 父级；请在 [partner-eu.temu.com](https://partner-eu.temu.com/documentation) 按 `type` 核对。另：`bg.local.goods.sku.list.price.query` 在 **Manage Products** 下可见（`sub_menu_code=c0de4d3f92d94b84a5044c4a3beda9f2`），属 SKU 价格列表，本 skill 未单独封装，可用 `temu_eu_proxy` 调用。

## 已接入（4）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `—` | `temu.local.goods.baseprice.recommend` | `eu_price_baseprice_recommend.py` | [apis/temu-local-goods-baseprice-recommend.md](./apis/temu-local-goods-baseprice-recommend.md) |
| `—` | `temu.local.goods.recommendedprice.query` | `eu_price_recommendedprice_query.py` | [apis/temu-local-goods-recommendedprice-query.md](./apis/temu-local-goods-recommendedprice-query.md) |
| `—` | `bg.local.goods.priceorder.query` | `eu_price_priceorder_query.py` | [apis/bg-local-goods-priceorder-query.md](./apis/bg-local-goods-priceorder-query.md) |
| `—` | `bg.local.goods.priceorder.change.sku.price` | `eu_price_priceorder_change_sku_price.py` | [apis/bg-local-goods-priceorder-change-sku-price.md](./apis/bg-local-goods-priceorder-change-sku-price.md) |

## 官方文档 URL

| type | URL |
|------|-----|
| `temu.local.goods.baseprice.recommend` | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648 |
| `temu.local.goods.recommendedprice.query` | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648 |
| `bg.local.goods.priceorder.query` | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648 |
| `bg.local.goods.priceorder.change.sku.price` | https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648 |

## 上游 OpenAPI（EU）

`POST` https://openapi-b-eu.temu.com/openapi/router（经 LinkFox 网关 `site=eu` 转发）

| 全球站（非 US/EU）价格 | `linkfox-temu-price-global` |

## 与 add-product / manage-product 区分

| skill | type | 说明 |
|-------|------|------|
| **本 skill** | `bg.local.goods.priceorder.*` / `temu.local.goods.*price*` | 定价单、推荐价、批量改价 |
| `linkfox-temu-manage-product-eu` | `bg.local.goods.sku.list.price.query` 等 | 商品管理域 |
| `linkfox-temu-add-product-us` | `temu.goods.price.list.get` | 发品侧（EU 可 `site=eu`） |
