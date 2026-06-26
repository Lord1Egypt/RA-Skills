# Partner Global — Compliance 接口目录

Partner Platform for **Global** 菜单：**Product Compliance / 电商合规**（`bg.compliance.*`、`bg.arbok.*`、`bg.flash.*` 等）。

文档根 `menu_code`：`fb16b05f7a904765aac4af3a24b87d4a`。

本 skill 经 `temu_global_proxy`（`POST /temu/proxy`）调用，默认 **`site=global`**、**`tokenPurpose=product-inventory`**。

## 已接入（9）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `a8829c8ede574d9a97cd3cea7c019bc4` | `bg.compliance.edit` | `global_compliance_edit.py` | [apis/bg-compliance-edit.md](./apis/bg-compliance-edit.md) |
| `fd12bdf5cb364366bdef85aad9cd8e48` | `bg.compliance.metadata.get` | `global_compliance_metadata_get.py` | [apis/bg-compliance-metadata-get.md](./apis/bg-compliance-metadata-get.md) |
| `c49495eb93904c93b750e9798c95e7db` | `bg.goods.compliancelabel.get` | `global_compliance_goods_compliancelabel_get.py` | [apis/bg-goods-compliancelabel-get.md](./apis/bg-goods-compliancelabel-get.md) |
| `84d3118d3a604947abf35144606cdea2` | `bg.arbok.open.cert.queryNeedUploadItems` | `global_compliance_arbok_cert_query_need_upload_items.py` | [apis/bg-arbok-open-cert-query-need-upload-items.md](./apis/bg-arbok-open-cert-query-need-upload-items.md) |
| `56de04bcafae45509b21edeab57c9fdb` | `bg.arbok.open.cert.uploadProductCert` | `global_compliance_arbok_cert_upload_product_cert.py` | [apis/bg-arbok-open-cert-upload-product-cert.md](./apis/bg-arbok-open-cert-upload-product-cert.md) |
| `960adb7a9d1f47069cdc0a9abd686dc9` | `bg.flash.open.upload.recognize` | `global_compliance_flash_upload_recognize.py` | [apis/bg-flash-open-upload-recognize.md](./apis/bg-flash-open-upload-recognize.md) |
| `ef77dada37ac49569f6e7c787dd696d9` | `bg.flash.open.upload.real.image` | `global_compliance_flash_upload_real_image.py` | [apis/bg-flash-open-upload-real-image.md](./apis/bg-flash-open-upload-real-image.md) |
| `01b8792d2e4a40f7b3b14f4a1f2711b6` | `bg.arbok.open.upload.uploadFile` | `global_compliance_arbok_upload_upload_file.py` | [apis/bg-arbok-open-upload-upload-file.md](./apis/bg-arbok-open-upload-upload-file.md) |
| `5ec78e3b36c34fcba743a75523349fb5` | `bg.arbok.open.product.cert.query` | `global_compliance_arbok_product_cert_query.py` | [apis/bg-arbok-open-product-cert-query.md](./apis/bg-arbok-open-product-cert-query.md) |

## 官方文档 URL

| type | URL |
|------|-----|
| `bg.compliance.edit` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=a8829c8ede574d9a97cd3cea7c019bc4 |
| `bg.compliance.metadata.get` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=fd12bdf5cb364366bdef85aad9cd8e48 |
| `bg.goods.compliancelabel.get` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=c49495eb93904c93b750e9798c95e7db |
| `bg.arbok.open.cert.queryNeedUploadItems` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=84d3118d3a604947abf35144606cdea2 |
| `bg.arbok.open.cert.uploadProductCert` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=56de04bcafae45509b21edeab57c9fdb |
| `bg.flash.open.upload.recognize` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=960adb7a9d1f47069cdc0a9abd686dc9 |
| `bg.flash.open.upload.real.image` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=ef77dada37ac49569f6e7c787dd696d9 |
| `bg.arbok.open.upload.uploadFile` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=01b8792d2e4a40f7b3b14f4a1f2711b6 |
| `bg.arbok.open.product.cert.query` | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=5ec78e3b36c34fcba743a75523349fb5 |

## 上游 OpenAPI（Global）

`POST` https://openapi-b-global.temu.com/openapi/router（经 LinkFox 网关 `site=global` 转发）

## 通用脚本

| 脚本 | 说明 |
|------|------|
| `temu_global_proxy.py` | 任意 `type` + `params` |
| `temu_global_file_download.py` | 加签文件下载 |

## 相关 skill

| 能力 | skill |
|------|--------|
| **电商合规**（本 skill） | **`linkfox-temu-compliance-global`** |
| 商品管理 | `linkfox-temu-manage-product-global` |

## Token 说明

建议使用 **`tokenPurpose=product-inventory`**。详见 [access-token.md](./access-token.md)。
