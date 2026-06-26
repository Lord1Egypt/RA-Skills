# Partner EU — Tax（电商税务）接口目录

Partner Platform for EU 菜单：**Tax / VAT**（文档根 `menu_code=7289390cfd724be4a196f11ebe45a896`）。

本 skill 经 `temu_eu_proxy`（`POST /temu/proxy`）调用 **7** 个税务 `type`，默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

## 已接入（7）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `6494bb7afd8048d380a13e92f6275d17` | `temu.pay.tax.apply.export.report` | `eu_tax_apply_export_report.py` | [apis/temu-pay-tax-apply-export-report.md](./apis/temu-pay-tax-apply-export-report.md) |
| `d6147c0484a341c49790b6dfed7da275` | `temu.pay.tax.get.galerie.signature` | `eu_tax_get_galerie_signature.py` | [apis/temu-pay-tax-get-galerie-signature.md](./apis/temu-pay-tax-get-galerie-signature.md) |
| `3985fe93bff5437c87863a22112b72db` | `temu.pay.tax.invoice.detail.query` | `eu_tax_invoice_detail_query.py` | [apis/temu-pay-tax-invoice-detail-query.md](./apis/temu-pay-tax-invoice-detail-query.md) |
| `5f5d1168742b4991a86684cbd0c21489` | `temu.pay.tax.invoice.info.query` | `eu_tax_invoice_info_query.py` | [apis/temu-pay-tax-invoice-info-query.md](./apis/temu-pay-tax-invoice-info-query.md) |
| `2b8a5a8a75604779b2e0017ee79b462a` | `temu.pay.tax.invoice.pdf.download` | `eu_tax_invoice_pdf_download.py` | [apis/temu-pay-tax-invoice-pdf-download.md](./apis/temu-pay-tax-invoice-pdf-download.md) |
| `cc87994f2ac24fc88795f2a3a8844683` | `temu.pay.tax.merchant.report.download` | `eu_tax_merchant_report_download.py` | [apis/temu-pay-tax-merchant-report-download.md](./apis/temu-pay-tax-merchant-report-download.md) |
| `98fcf420ee5c4f0d8c8f708adfd89160` | `temu.pay.tax.merchant.upload.invoice` | `eu_tax_merchant_upload_invoice.py` | [apis/temu-pay-tax-merchant-upload-invoice.md](./apis/temu-pay-tax-merchant-upload-invoice.md) |

## 官方文档 URL

| type | URL |
|------|-----|
| `temu.pay.tax.apply.export.report` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=6494bb7afd8048d380a13e92f6275d17 |
| `temu.pay.tax.get.galerie.signature` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d6147c0484a341c49790b6dfed7da275 |
| `temu.pay.tax.invoice.detail.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=3985fe93bff5437c87863a22112b72db |
| `temu.pay.tax.invoice.info.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=5f5d1168742b4991a86684cbd0c21489 |
| `temu.pay.tax.invoice.pdf.download` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=2b8a5a8a75604779b2e0017ee79b462a |
| `temu.pay.tax.merchant.report.download` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=cc87994f2ac24fc88795f2a3a8844683 |
| `temu.pay.tax.merchant.upload.invoice` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=98fcf420ee5c4f0d8c8f708adfd89160 |

## 上游 OpenAPI（EU）

`POST` https://openapi-b-eu.temu.com/openapi/router（经 LinkFox 网关 `site=eu` 转发）

## 通用脚本

| 脚本 | 说明 |
|------|------|
| `temu_eu_proxy.py` | 任意 `type` + `params` |
| `temu_eu_file_download.py` | 加签文件下载 |

## 与其他 Temu EU skill 的关系

| 能力 | skill |
|------|--------|
| 电商税务（本 skill） | **`linkfox-temu-tax-eu`** |
| 商品管理 | `linkfox-temu-manage-product-eu` |
| 订单 / 金额 | `linkfox-temu-order-eu` |
| 价格 | `linkfox-temu-price-eu` |

## Token 说明

详见 [access-token.md](./access-token.md)。
