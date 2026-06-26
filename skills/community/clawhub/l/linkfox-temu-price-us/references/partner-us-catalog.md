# Partner US — Price 接口目录

Partner Platform for US 菜单：**Product**（`menu_code=fb16b05f7a904765aac4af3a24b87d4a`）下与**价格/供货价**相关的子菜单。

本 skill 经本 skill `temu_us_proxy`（`POST /temu/proxy`） 调用，`type` 写在 Body。内联参数见 [apis/README.md](./apis/README.md)。

> **扩展方式**：你每提供一条 Partner 文档（`type` + `sub_menu_code` + URL + 参数表），即在 `references/apis/<type-slug>.md` 新增文档，并添加 `scripts/us_price_<slug>.py` 薄封装，同步更新本表与 `SKILL.md` 脚本表。

## 已接入（4）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| _TBD_ | `temu.local.goods.baseprice.recommend` | `us_price_baseprice_recommend.py` | [apis/temu-local-goods-baseprice-recommend.md](./apis/temu-local-goods-baseprice-recommend.md) |
| _TBD_ | `temu.local.goods.recommendedprice.query` | `us_price_recommendedprice_query.py` | [apis/temu-local-goods-recommendedprice-query.md](./apis/temu-local-goods-recommendedprice-query.md) |
| _TBD_ | `bg.local.goods.priceorder.query` | `us_price_priceorder_query.py` | [apis/bg-local-goods-priceorder-query.md](./apis/bg-local-goods-priceorder-query.md) |
| _TBD_ | `bg.local.goods.priceorder.change.sku.price` | `us_price_priceorder_change_sku_price.py` | [apis/bg-local-goods-priceorder-change-sku-price.md](./apis/bg-local-goods-priceorder-change-sku-price.md) |

Partner 文档入口：

| type | URL |
|------|-----|
| `temu.local.goods.baseprice.recommend` | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a（`sub_menu_code` 待补） |
| `temu.local.goods.recommendedprice.query` | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a（`sub_menu_code` 待补） |
| `bg.local.goods.priceorder.query` | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a（`sub_menu_code` 待补） |
| `bg.local.goods.priceorder.change.sku.price` | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a（`sub_menu_code` 待补） |

## 待补充

以下占位，按你后续提供的官方文档逐条填入：

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| _TBD_ | _TBD_ | `us_price_*.py` | `apis/*.md` |

---

| 全球站（非 US/EU）价格 | `linkfox-temu-price-global` |

## 与 add-product-us 的价格接口区分

| skill | type | 典型入参 | 说明 |
|-------|------|----------|------|
| **本 skill** | `bg.local.goods.priceorder.query` | `request.page` / `size`、筛选条件 | 白名单定价单/报价列表 |
| **本 skill** | `temu.local.goods.recommendedprice.query` | `request.goodsIdList` + `recommendedPriceType` | 推荐供货价 |
| `linkfox-temu-add-product-us` | `temu.goods.price.list.get` | `productSkuIds` | 发品/半托管侧供货价列表 |
