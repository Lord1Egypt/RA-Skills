# 合规商品列表 — `bg.local.compliance.goods.list.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_compliance_list_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.compliance.goods.list.query`，业务载荷放在 Body 的 `params` |

**Description:** Product management attribute list query（合规待办/属性管理商品列表查询）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNo / pageSize
    ├── searchText
    ├── statusList
    └── optionalConditionList[]
        ├── complianceType
        ├── templateId
        ├── repType
        ├── actualPhotoCheckType
        └── certType
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNo | INTEGER | **是** | Page NO. |
| pageSize | INTEGER | **是** | Page Size，**默认 25** |
| searchText | STRING | 否 | 支持按 **goodsName** / **goodsId** / **skuId** 搜索 |
| statusList | INTEGER[] | 否 | 合规状态筛选，见下表 |
| optionalConditionList | OBJECT[] | 否 | Compliance Information Filters（合规信息筛选） |

#### `statusList` / 各块 `status` 枚举

| 值 | 说明 |
|----|------|
| `1` | not submitted（未提交） |
| `2` | To be reviewed（待审核） |
| `3` | Reviewing（审核中） |
| `4` | Action required（需处理） |
| `5` | Approved（已通过） |
| `6` | Rejected（已拒绝） |
| `7` | To be updated（待更新） |

### `optionalConditionList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| complianceType | INTEGER | 否 | `1` Governance attributes；`2` General Product Safety Regulation（GPSR） |
| templateId | INTEGER | 否 | 合规模板类型筛选（文档与 `complianceType` 同组说明：`1` Governance / `2` GPSR） |
| repType | INTEGER | 否 | `2` EU responsible person；`3` manufacturer。**`complianceType=2` 时必填** |
| actualPhotoCheckType | LONG | 否 | 实拍图 checkType。**`complianceType=3` 时必填** |
| certType | LONG | 否 | 资质 checkType。**`complianceType=4` 时填写** |

> 筛选侧 `complianceType` 除 `1`/`2` 外，通过条件字段可推断 **`3`** 实拍、`**4**` 资质等类型（以 Partner 与实网为准）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 25,
    "statusList": [4, 7],
    "searchText": "keyword"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 25,
    "optionalConditionList": [
      {
        "complianceType": 2,
        "repType": 2
      }
    ]
  }
}
```

> **勿**使用旧字段 `goodsIdList`、`complianceStatus`；官方为 **`statusList`** + **`optionalConditionList`**。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    ├── total
    └── goodsList[]
        ├── goodsId / goodsName / thumbUrl / outGoodsSn / crtTime
        ├── extraTemplateInfoList[]
        ├── gpsrInfoList[]
        ├── repInfoList[]
        ├── actualPhotoList[]
        └── certificateInfoList[]
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Success or not |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result | OBJECT | Result |
| result.total | LONG | Total |
| result.goodsList | OBJECT[] | Goods list |

### `result.goodsList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods Id |
| goodsName | STRING | Goods Name |
| thumbUrl | STRING | Goods Thumb Url |
| outGoodsSn | STRING | External SKU Codes（外部商品编码） |
| crtTime | LONG | Creation time，单位 **秒** |
| extraTemplateInfoList | OBJECT[] | Governance attribute template information list |
| gpsrInfoList | OBJECT[] | GPSR info list |
| repInfoList | OBJECT[] | Responsible Person Info |
| actualPhotoList | OBJECT[] | Actual photo list |
| certificateInfoList | OBJECT[] | certification list |

### `extraTemplateInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| templateId | INTEGER | template ID of governance attributes |
| status | INTEGER | 合规状态，见 `statusList` 枚举 |

### `gpsrInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| repType | INTEGER | `2` EU responsible person；`3` manufacturer |
| status | INTEGER | 合规状态 |

### `repInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| repType | INTEGER | `4` A/S Responsible Person |
| status | INTEGER | 合规状态 |

### `actualPhotoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| actualPhotoCheckType | LONG | checkType of actual photo |
| status | INTEGER | 合规状态 |

### `certificateInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| certType | LONG | certType of this certificate |
| status | INTEGER | 合规状态 |

---

## 示例

```bash
python scripts/global_manage_compliance_list_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 25,
    "statusList": [4, 7]
  }
}'
```

```bash
python scripts/global_manage_compliance_list_query.py '{
  "accessToken": "TOKEN",
  "request": {
    "pageNo": 1,
    "pageSize": 25,
    "searchText": "123456789",
    "optionalConditionList": [
      {
        "complianceType": 2,
        "repType": 3
      }
    ]
  }
}'
```
