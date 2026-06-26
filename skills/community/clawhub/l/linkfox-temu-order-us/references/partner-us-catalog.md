# Partner US — Order 接口目录

Partner Platform for US 菜单：**Order / 订单管理**（`menu_code` 与各 `sub_menu_code` 以 Partner 后台为准）。

本 skill 经本 skill `temu_us_proxy`（`POST /temu/proxy`） 调用，`type` 写在 Body。内联参数见 [apis/README.md](./apis/README.md)。

> **扩展方式**：你每提供一条 Partner 文档（`type` + `sub_menu_code` + URL + 参数表），即在 `references/apis/<type-slug>.md` 新增文档，并添加 `scripts/us_order_<slug>.py` 薄封装，同步更新本表与 `SKILL.md` 脚本表。

## 已接入（8）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| _TBD_ | `bg.order.list.v2.get` | `us_order_list_v2_get.py` | [apis/bg-order-list-v2-get.md](./apis/bg-order-list-v2-get.md) |
| _TBD_ | `bg.order.detail.v2.get` | `us_order_detail_v2_get.py` | [apis/bg-order-detail-v2-get.md](./apis/bg-order-detail-v2-get.md) |
| _TBD_ | `bg.order.shippinginfo.v2.get` | `us_order_shippinginfo_v2_get.py` | [apis/bg-order-shippinginfo-v2-get.md](./apis/bg-order-shippinginfo-v2-get.md) |
| _TBD_ | `bg.order.decryptshippinginfo.get` | `us_order_decryptshippinginfo_get.py` | [apis/bg-order-decryptshippinginfo-get.md](./apis/bg-order-decryptshippinginfo-get.md) |
| _TBD_ | `bg.order.amount.query` | `us_order_amount_query.py` | [apis/bg-order-amount-query.md](./apis/bg-order-amount-query.md) |
| _TBD_ | `bg.order.combinedshipment.list.get` | `us_order_combinedshipment_list_get.py` | [apis/bg-order-combinedshipment-list-get.md](./apis/bg-order-combinedshipment-list-get.md) |
| _TBD_ | `bg.order.customization.get` | `us_order_customization_get.py` | [apis/bg-order-customization-get.md](./apis/bg-order-customization-get.md) |
| _TBD_ | `temu.local.order.verification.upload` | `us_order_verification_upload.py` | [apis/temu-local-order-verification-upload.md](./apis/temu-local-order-verification-upload.md) |

Partner 文档入口（随接入填写）：

| type | URL |
|------|-----|
| `bg.order.list.v2.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.detail.v2.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.shippinginfo.v2.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.decryptshippinginfo.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.amount.query` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.combinedshipment.list.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `bg.order.customization.get` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |
| `temu.local.order.verification.upload` | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 待补） |

## 通用脚本（已就绪）

| 脚本 | 说明 |
|------|------|
| `temu_us_proxy.py` | 任意 `type` + `params` |
| `temu_us_file_download.py` | 加签文件下载 |

---

| 全球站（非 US/EU）订单 | `linkfox-temu-order-global` |

## 与其他 Temu US skill 的关系

| 能力 | skill |
|------|--------|
| 订单查询、发货、物流 | `linkfox-temu-order-us` |
| 取消订单（买家+卖家） | `linkfox-temu-cancel-order-us` |

| 退货与退款 | `linkfox-temu-returns-refunds-us` |
| 履约/发货（含自发货） | `linkfox-temu-fulfillment-us` |
| 履约/发货（含合作仓） | `linkfox-temu-fulfillment-us` |
| 商品列表/详情/编辑/库存 | `linkfox-temu-manage-product-us` |
| 发品 V2 | `linkfox-temu-add-product-us` |
| 价格/定价单 | `linkfox-temu-price-us` |
| 网关、Token | 本 skill `scripts/`（`temu_us_proxy`、`check_linkfox_token` 等） |

---

## Token 说明

订单类接口建议使用 **`tokenPurpose=order-shipping`**（半托管 US 订单/发货）。详见 `references/access-token.md`。
