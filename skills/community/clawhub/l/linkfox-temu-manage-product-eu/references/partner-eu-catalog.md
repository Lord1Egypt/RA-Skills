# Partner EU — Manage Product 接口目录

Partner Platform for EU 菜单：**Product > Manage Products**（`menu_code=2283b8dc7fcc42529633b0b41114aef8`）。

文档根 `menu_code`（与浏览器地址栏一致）：`7289390cfd724be4a196f11ebe45a896`。

本 skill 覆盖 **24** 个 `bg.local.*` / `temu.local.*` 商品管理接口（与 US 版 `type` 对齐）。调用经本 skill `temu_eu_proxy`（`POST /temu/proxy`），默认 **`site=eu`**。

> **内联参数**见 [apis/README.md](./apis/README.md)。`sub_menu_code` 来自 Partner EU 文档导出（2026-05）；`bg.local.goods.publish.status.get` 在 EU 菜单快照中未出现，文档链至 Manage Products 父级。

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `43baaa509c4b4b419853558a613715de` | `bg.local.goods.list.query` | `eu_manage_list_query.py` | [apis/bg-local-goods-list-query.md](./apis/bg-local-goods-list-query.md) |
| `b13c66e2a08740ecbdcc2f95e2573ac9` | `temu.local.goods.list.retrieve` | `eu_manage_goods_list_retrieve.py` | [apis/temu-local-goods-list-retrieve.md](./apis/temu-local-goods-list-retrieve.md) |
| `50a6dd012fcd41149a2d8ef2cdc58b69` | `bg.local.goods.detail.query` | `eu_manage_detail_query.py` | [apis/bg-local-goods-detail-query.md](./apis/bg-local-goods-detail-query.md) |
| `9844039f01204efea2c7355dfdc1eace` | `bg.local.goods.sku.list.query` | `eu_manage_sku_list_query.py` | [apis/bg-local-goods-sku-list-query.md](./apis/bg-local-goods-sku-list-query.md) |
| `4b8fcc68f0f4463ab59225d677301413` | `temu.local.sku.list.retrieve` | `eu_manage_sku_list_retrieve.py` | [apis/temu-local-sku-list-retrieve.md](./apis/temu-local-sku-list-retrieve.md) |
| `—` | `bg.local.goods.publish.status.get` | `eu_manage_publish_status_get.py` | [apis/bg-local-goods-publish-status-get.md](./apis/bg-local-goods-publish-status-get.md) |
| `d2c3a9ad5fe7428b8ac5953b769a2c00` | `temu.local.goods.sku.stock.query` | `eu_manage_sku_stock_query.py` | [apis/temu-local-goods-sku-stock-query.md](./apis/temu-local-goods-sku-stock-query.md) |
| `8b7845c1b6e54c5c81c1eebe4ee829d6` | `bg.local.goods.stock.edit` | `eu_manage_stock_edit.py` | [apis/bg-local-goods-stock-edit.md](./apis/bg-local-goods-stock-edit.md) |
| `f25a3d4a2a884c97ada8944250fd176e` | `bg.local.goods.partial.update` | `eu_manage_partial_update.py` | [apis/bg-local-goods-partial-update.md](./apis/bg-local-goods-partial-update.md) |
| `9ec69ff253ff4403bed421ca114144ef` | `bg.local.goods.update` | `eu_manage_goods_update.py` | [apis/bg-local-goods-update.md](./apis/bg-local-goods-update.md) |
| `d651ab650f3546fea22874a9d758ffe4` | `temu.local.goods.delete` | `eu_manage_goods_delete.py` | [apis/temu-local-goods-delete.md](./apis/temu-local-goods-delete.md) |
| `7e396281b713436c93363864b6b826aa` | `temu.local.goods.spec.info.get` | `eu_manage_spec_info_get.py` | [apis/temu-local-goods-spec-info-get.md](./apis/temu-local-goods-spec-info-get.md) |
| `fbcf3afb3eac4f039e30982ca5641033` | `bg.local.goods.category.check` | `eu_manage_category_check.py` | [apis/bg-local-goods-category-check.md](./apis/bg-local-goods-category-check.md) |
| `42cd0095f6964ed88a2750bf8f005809` | `bg.local.goods.property.get` | `eu_manage_property_get.py` | [apis/bg-local-goods-property-get.md](./apis/bg-local-goods-property-get.md) |
| `d93de48fc77d49d38764292d69dc5abd` | `bg.local.goods.property.relations` | `eu_manage_property_relations.py` | [apis/bg-local-goods-property-relations.md](./apis/bg-local-goods-property-relations.md) |
| `ef845cd5342c4dc7b0c44c2f361abfbb` | `bg.local.goods.property.relations.level.template` | `eu_manage_property_relations_level_template.py` | [apis/bg-local-goods-property-relations-level-template.md](./apis/bg-local-goods-property-relations-level-template.md) |
| `bfd820e01f23408689b2b532816e475d` | `bg.local.goods.property.relations.template` | `eu_manage_property_relations_template.py` | [apis/bg-local-goods-property-relations-template.md](./apis/bg-local-goods-property-relations-template.md) |
| `b203fc2bdde346239dbb51da1dc2e713` | `bg.local.goods.out.sn.set` | `eu_manage_out_sn_set.py` | [apis/bg-local-goods-out-sn-set.md](./apis/bg-local-goods-out-sn-set.md) |
| `e020cff4237247458fdf20fd17675c37` | `bg.local.goods.sku.out.sn.set` | `eu_manage_sku_out_sn_set.py` | [apis/bg-local-goods-sku-out-sn-set.md](./apis/bg-local-goods-sku-out-sn-set.md) |
| `cf3e1c09736d4f1f96c4b0016b2af52d` | `bg.local.compliance.goods.list.query` | `eu_manage_compliance_list_query.py` | [apis/bg-local-compliance-goods-list-query.md](./apis/bg-local-compliance-goods-list-query.md) |
| `4499655e8cb044a0b8a30f9c9994f723` | `bg.local.goods.compliance.edit` | `eu_manage_compliance_edit.py` | [apis/bg-local-goods-compliance-edit.md](./apis/bg-local-goods-compliance-edit.md) |
| `40fd5e090dbb4a3790d1c2b88223ec5e` | `bg.local.goods.sale.status.set` | `eu_manage_sale_status_set.py` | [apis/bg-local-goods-sale-status-set.md](./apis/bg-local-goods-sale-status-set.md) |
| `c3173683180c42e19b12f48c903e2f98` | `temu.local.goods.pre.sale.status.edit` | `eu_manage_pre_sale_status_edit.py` | [apis/temu-local-goods-pre-sale-status-edit.md](./apis/temu-local-goods-pre-sale-status-edit.md) |
| `4759c1207d8940bf8dd09eaad1cc853f` | `bg.local.goods.videocoverimage.get` | `eu_manage_videocoverimage_get.py` | [apis/bg-local-goods-videocoverimage-get.md](./apis/bg-local-goods-videocoverimage-get.md) |

## 官方文档 URL（按 type）

文档基址：`https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=<code>`

| type | 文档 |
|------|------|
| `bg.local.goods.list.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=43baaa509c4b4b419853558a613715de |
| `temu.local.goods.list.retrieve` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=b13c66e2a08740ecbdcc2f95e2573ac9 |
| `bg.local.goods.detail.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=50a6dd012fcd41149a2d8ef2cdc58b69 |
| `bg.local.goods.sku.list.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=9844039f01204efea2c7355dfdc1eace |
| `temu.local.sku.list.retrieve` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=4b8fcc68f0f4463ab59225d677301413 |
| `bg.local.goods.publish.status.get` | https://partner-eu.temu.com/documentation?menu_code=2283b8dc7fcc42529633b0b41114aef8 |
| `temu.local.goods.sku.stock.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d2c3a9ad5fe7428b8ac5953b769a2c00 |
| `bg.local.goods.stock.edit` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=8b7845c1b6e54c5c81c1eebe4ee829d6 |
| `bg.local.goods.partial.update` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=f25a3d4a2a884c97ada8944250fd176e |
| `bg.local.goods.update` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=9ec69ff253ff4403bed421ca114144ef |
| `temu.local.goods.delete` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d651ab650f3546fea22874a9d758ffe4 |
| `temu.local.goods.spec.info.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=7e396281b713436c93363864b6b826aa |
| `bg.local.goods.category.check` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=fbcf3afb3eac4f039e30982ca5641033 |
| `bg.local.goods.property.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=42cd0095f6964ed88a2750bf8f005809 |
| `bg.local.goods.property.relations` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d93de48fc77d49d38764292d69dc5abd |
| `bg.local.goods.property.relations.level.template` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=ef845cd5342c4dc7b0c44c2f361abfbb |
| `bg.local.goods.property.relations.template` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=bfd820e01f23408689b2b532816e475d |
| `bg.local.goods.out.sn.set` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=b203fc2bdde346239dbb51da1dc2e713 |
| `bg.local.goods.sku.out.sn.set` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=e020cff4237247458fdf20fd17675c37 |
| `bg.local.compliance.goods.list.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=cf3e1c09736d4f1f96c4b0016b2af52d |
| `bg.local.goods.compliance.edit` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=4499655e8cb044a0b8a30f9c9994f723 |
| `bg.local.goods.sale.status.set` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=40fd5e090dbb4a3790d1c2b88223ec5e |
| `temu.local.goods.pre.sale.status.edit` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=c3173683180c42e19b12f48c903e2f98 |
| `bg.local.goods.videocoverimage.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=4759c1207d8940bf8dd09eaad1cc853f |

## 上游 OpenAPI（EU）

`POST` https://openapi-b-eu.temu.com/openapi/router（经 LinkFox 网关 `site=eu` 转发）

## 与 `linkfox-temu-add-product-eu` 的关系

| 能力 | skill |
|------|--------|
| V2 发品、类目映射 | `linkfox-temu-add-product-eu`（若已发布） |
| 全球站（非 US/EU）商品管理 | `linkfox-temu-manage-product-global` |
| 本 skill：`bg.local.*` / `temu.local.*` 商品管理 | `linkfox-temu-manage-product-eu` |
| 网关、Token | 本 skill `scripts/` |
