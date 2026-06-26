# 合规编辑 — `bg.local.goods.compliance.edit`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_manage_compliance_edit.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.compliance.edit`，业务载荷放在 Body 的 `params` |

**Description:** Edit product qualification information（编辑商品合规/资质信息：资质文件、实拍图、责任人、治理属性等）。

---

## 调用方式说明

经 **LinkFox 网关** 调用时，使用 `accessToken` + `request` 等业务字段即可，**无需**在 `params` 中自行拼装 `app_key`、`sign`、`timestamp` 等（由网关代签转发）。直连 Temu OpenAPI 时需携带下列通用参数。

### Temu OpenAPI 通用参数（直连上游）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | STRING | **是** | API 名称，如 `bg.local.goods.compliance.edit` |
| app_key | STRING | **是** | 应用 Key |
| access_token | STRING | **是** | 访问控制用安全令牌（A secure token for access control） |
| sign | STRING | **是** | 请求签名 |
| timestamp | STRING | **是** | UNIX 时间戳（秒），10 位；须在「当前时间 ±300 秒」范围内 |
| data_type | STRING | 否 | 请求/响应数据格式，可选参数固定为 JSON |
| version | STRING | 否 | API 版本，默认 V1；无特殊要求可不传 |

---

## Request 结构（业务 `params`）

```text
params
└── request (OBJECT, 选填)
    ├── language
    ├── goodsId                    ← 必填
    ├── certificateInfo            ← 资质文件
    │   └── certificateDetailList[]
    │       ├── certType
    │       ├── skip
    │       ├── authCode
    │       ├── authCodes[]
    │       │   └── authCode
    │       ├── certFiles[]        ← 最多 6
    │       │   ├── fileName
    │       │   ├── fileUrl
    │       │   └── language
    │       └── inspectReportFiles[]  ← 最多 6
    │           ├── fileName
    │           ├── fileUrl
    │           └── language
    ├── actualPhoto                ← 实拍图
    │   ├── skip
    │   └── actualPhotoInfoList[]
    │       ├── sameSku
    │       ├── position
    │       └── skuPhotoInfoList[]
    │           ├── specIdList[]
    │           └── imageList[]
    │               └── imageUrl
    ├── repInfo                    ← 责任人
    │   └── repDetailList[]
    │       ├── complianceRepType
    │       └── repIdList[]
    └── extraTemplate              ← 治理属性
        └── extraTemplateDetailList[]
            ├── templateId
            ├── properties         ← MAP: propertyId → value id[]
            ├── inputText          ← MAP: propertyId → 输入对象
            └── compliancePropertyList[]  ← SKU 维度合规
                ├── specIdList[]
                └── inputTextList[]
                    ├── properties
                    └── inputText
```

### `request` 顶层字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | language（语言） |
| goodsId | LONG | **是** | Goods ID（商品 ID） |
| certificateInfo | OBJECT | 否 | Qualification Documents（资质文件） |
| actualPhoto | OBJECT | 否 | Actual Photos（实拍图） |
| repInfo | OBJECT | 否 | Responsible Person Info（责任人信息） |
| extraTemplate | OBJECT | 否 | Governance attributes（治理属性 / 合规模板扩展） |

---

### `certificateInfo` — 资质文件

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| certificateDetailList | OBJECT[] | 否 | List of Qualification Documents（资质文件明细列表） |

#### `certificateDetailList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| certType | INTEGER | **是** | Qualification Type（资质类型） |
| skip | BOOLEAN | 否 | Whether to skip（是否跳过）；未传时**默认不跳过** |
| authCode | STRING | 否 | Qualification Number（资质编号），**最多 120 字符** |
| authCodes | OBJECT[] | 否 | Qualification Number Info（资质编号信息列表） |
| certFiles | OBJECT[] | 否 | List of Qualification Certificate Files（资质证书文件列表），**最多 6 个** |
| inspectReportFiles | OBJECT[] | 否 | List of Inspection Report Files（检测报告文件列表），**最多 6 个** |

##### `authCodes[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| authCode | STRING | 否 | Qualification Number（资质编号），**最多 120 字符** |

##### `certFiles[]` / `inspectReportFiles[]`（结构相同）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fileName | STRING | **是** | File Name（文件名），**最多 200 字符** |
| fileUrl | STRING | **是** | File URL（文件 URL） |
| language | STRING | 否 | file language（文件语言） |

---

### `actualPhoto` — 实拍图

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skip | BOOLEAN | 否 | Whether to skip（是否跳过）；未传时**默认不跳过** |
| actualPhotoInfoList | OBJECT[] | 否 | Actual Photo Module Information（实拍图模块信息列表） |

#### `actualPhotoInfoList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sameSku | BOOLEAN | **是** | Whether the product SKUs are the same（各 SKU 是否相同） |
| position | INTEGER | **是** | Position of the actual photo（实拍图位置） |
| skuPhotoInfoList | OBJECT[] | **是** | SKU Photos（SKU 实拍图列表） |

##### `skuPhotoInfoList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| specIdList | LONG[] | 否 | Spec IDs（规格 ID 列表） |
| imageList | OBJECT[] | **是** | List of Image URLs（图片 URL 列表） |

###### `imageList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageUrl | STRING | **是** | Image URL（图片 URL） |

---

### `repInfo` — 责任人信息

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| repDetailList | OBJECT[] | 否 | Responsible Person Detail Info（责任人明细列表） |

#### `repDetailList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| complianceRepType | INTEGER | 否 | 责任人类型，如 **`4`**：A/S REP（售后代表） |
| repIdList | LONG[] | 否 | Responsible Person Id（责任人 ID 列表） |

---

### `extraTemplate` — 治理属性

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| extraTemplateDetailList | OBJECT[] | 否 | attributes List（属性明细列表） |

#### `extraTemplateDetailList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| templateId | INTEGER | 否 | Template ID（模板 ID） |
| properties | MAP | 否 | **propertyId → 属性值 ID 列表**。对应控件：`controlType=1` 下拉选择；`controlType=3` 输入或选择 |
| inputText | MAP | 否 | **propertyId → 输入值对象**。对应控件：`0` 输入；`3` 输入或选择；`17` 多行输入；`18` 双值比例 |
| compliancePropertyList | OBJECT[] | 否 | sku dimension compliance information（SKU 维度合规信息） |

##### `properties`（MAP 键值）

| 键 / 值 | 类型 | 说明 |
|---------|------|------|
| `$key`（propertyId） | STRING | propertyId（属性 ID） |
| `$value` | LONG[] | property value id（属性值 ID 列表） |

##### `inputText`（MAP 键值）

| 键 / 值 | 类型 | 说明 |
|---------|------|------|
| `$key`（propertyId） | STRING | propertyId（属性 ID） |
| `$value` | OBJECT | Input Value（输入值对象），见下表 |

###### `inputText.$value`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | STRING | 否 | Input Value（输入文本） |
| multiLineInputs | OBJECT[] | 否 | Multi-line input（多行输入，`controlType=17`、`18`） |

####### `multiLineInputs[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | STRING | 否 | Input value（`controlType=17`、`18` 时的输入值） |
| vid | LONG | 否 | Attribute value（`controlType=18` 时的属性值 ID） |

##### `compliancePropertyList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| specIdList | LONG[] | 否 | spec ids（规格 ID 列表） |
| inputTextList | OBJECT[] | 否 | Input Value（SKU 维度输入值列表） |

###### `inputTextList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| properties | MAP | 否 | Attribute Value，**key 为 property_id** → `LONG[]` 属性值 ID |
| inputText | MAP | 否 | Input Value，**key 为 property_id** → 输入对象（结构同上文 `inputText.$value`） |

---

### 网关 `params` 写法（示例）

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "language": "en",
    "certificateInfo": {
      "certificateDetailList": [
        {
          "certType": 1,
          "authCode": "CERT-001",
          "certFiles": [
            {
              "fileName": "certificate.pdf",
              "fileUrl": "https://example.com/cert.pdf",
              "language": "en"
            }
          ]
        }
      ]
    },
    "actualPhoto": {
      "actualPhotoInfoList": [
        {
          "sameSku": true,
          "position": 1,
          "skuPhotoInfoList": [
            {
              "specIdList": [10001],
              "imageList": [
                { "imageUrl": "https://example.com/photo1.jpg" }
              ]
            }
          ]
        }
      ]
    },
    "repInfo": {
      "repDetailList": [
        {
          "complianceRepType": 4,
          "repIdList": [90001]
        }
      ]
    },
    "extraTemplate": {
      "extraTemplateDetailList": [
        {
          "templateId": 100,
          "properties": {
            "12345": [67890]
          },
          "inputText": {
            "23456": {
              "name": "custom text"
            }
          }
        }
      ]
    }
  }
}
```

> 官方字段名为 **`certificateInfo`**（非 `certificationInfo`）。各合规块是否必填取决于类目与待办类型，可先通过 `bg.local.compliance.goods.list.query` 查询待补项。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT，可能为空)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | 当前请求是否成功：成功返回 `true`，否则返回 `false` |
| errorCode | INTEGER | 错误码：用于对照错误码表定位解决方案 |
| errorMsg | STRING | 错误信息：与 `errorCode` 对应的反馈内容 |
| result | OBJECT | 业务结果；本接口成功时常见为空对象或仅含简单确认字段，以 Partner 实网返回为准 |

> 解析顺序见 [../api.md](../api.md)：先校验网关 `code`，再解析 `body` 内 `success` / `errorCode` / `errorMsg`。

---

## 相关接口

| 接口 | 用途 |
|------|------|
| `bg.local.compliance.goods.list.query` | 查询待合规/待更新商品及所需合规类型 |
| `bg.local.goods.property.get` | 查询商品属性（含合规模板参考） |
| `linkfox-temu-add-product-us` 发品文档 | `certificationInfo` 与本文 `certificateInfo` 等同族结构参考 |

---

## 示例

```bash
python scripts/us_manage_compliance_edit.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "certificateInfo": {
      "certificateDetailList": [
        {
          "certType": 1,
          "skip": false,
          "authCode": "AUTH-2024-001",
          "certFiles": [
            {
              "fileName": "ce-cert.pdf",
              "fileUrl": "https://cdn.example.com/ce-cert.pdf"
            }
          ]
        }
      ]
    }
  }
}'
```
