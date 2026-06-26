# Partner Global — 取消订单接口目录

Partner Platform for **Global（全球区，非 US/EU）** 菜单：**Order / 取消订单**（`menu_code=dbd3d395963a408984b8ae7dbc5f64f9`）。

本 skill 经 `temu_global_proxy`（`POST /temu/proxy`）调用 **6** 个 `type`，默认 **`site=global`**、**`tokenPurpose=order-shipping`**。

> 各接口 `sub_menu_code` 请在 [partner-global.temu.com](https://partner-global.temu.com/documentation) 按 `type` 核对。美国站请用 **`linkfox-temu-cancel-order-us`**；欧洲站请用 **`linkfox-temu-cancel-order-eu`**。

## 已接入（6）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| — | `bg.aftersales.cancel.list.get` | `global_cancel_aftersales_cancel_list_get.py` | [apis/bg-aftersales-cancel-list-get.md](./apis/bg-aftersales-cancel-list-get.md) |
| — | `bg.aftersales.cancel.agree` | `global_cancel_aftersales_cancel_agree.py` | [apis/bg-aftersales-cancel-agree.md](./apis/bg-aftersales-cancel-agree.md) |
| — | `temu.order.cancel.appeal.apply` | `global_seller_cancel_order_cancel_appeal_apply.py` | [apis/temu-order-cancel-appeal-apply.md](./apis/temu-order-cancel-appeal-apply.md) |
| — | `temu.order.cancel.appeal.result.get` | `global_seller_cancel_order_cancel_appeal_result_get.py` | [apis/temu-order-cancel-appeal-result-get.md](./apis/temu-order-cancel-appeal-result-get.md) |
| — | `temu.order.cancel.outofstock.apply` | `global_seller_cancel_order_cancel_outofstock_apply.py` | [apis/temu-order-cancel-outofstock-apply.md](./apis/temu-order-cancel-outofstock-apply.md) |
| — | `temu.order.cancel.outofstock.result.get` | `global_seller_cancel_order_cancel_outofstock_result_get.py` | [apis/temu-order-cancel-outofstock-result-get.md](./apis/temu-order-cancel-outofstock-result-get.md) |

## 官方文档 URL

| type | URL |
|------|-----|
| `bg.aftersales.cancel.list.get` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |
| `bg.aftersales.cancel.agree` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |
| `temu.order.cancel.appeal.apply` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |
| `temu.order.cancel.appeal.result.get` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |
| `temu.order.cancel.outofstock.apply` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |
| `temu.order.cancel.outofstock.result.get` | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9 |

## 上游 OpenAPI（Global）

`POST` https://openapi-b-global.temu.com/openapi/router（经 LinkFox 网关 `site=global` 转发）

## 通用脚本

| 脚本 | 说明 |
|------|------|
| `temu_global_proxy.py` | 任意 `type` + `params` |
| `temu_global_file_download.py` | 加签文件下载 |

## 与其他 Temu skill 的关系

| 能力 | skill |
|------|--------|
| **取消订单**（本 skill，买家+卖家，`site=global`） | **`linkfox-temu-cancel-order-global`** |
| 订单查询、发货 | `linkfox-temu-order-global` |
| 美国站取消 | `linkfox-temu-cancel-order-us` |
| 欧洲站取消 | `linkfox-temu-cancel-order-eu` |
| 商品管理 | `linkfox-temu-manage-product-global` |

## Token 说明

详见 [access-token.md](./access-token.md)。
