# 合规模板元数据查询 — `bg.compliance.metadata.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_metadata_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=fd12bdf5cb364366bdef85aad9cd8e48 |
| **网关** | `POST /temu/proxy`，`type`=`bg.compliance.metadata.get`，业务载荷放在 Body 的 `params` |

**Description:** Query compliance metadata / template definitions for a product.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── productId (LONG **必填**)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | LONG | **是** | product id |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "productId": 1
  }
}
```

> Partner **Request Example** 为 CURL，业务字段可能在顶层；经 LinkFox 网关请放在 **`params.request`**（或脚本接受的顶层 `request`）。

---

## Response（Partner Response 表 + 全量展开）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── complianceInfoList[] (OBJECT[])
    ├── complianceInfoList[].complianceType (INTEGER)
    ├── complianceInfoList[].desc (STRING)
    ├── complianceInfoList[].name (STRING)
    ├── complianceInfoList[].propertyList[] (OBJECT[])
    ├── complianceInfoList[].propertyList[].controlType (INTEGER)
    ├── complianceInfoList[].propertyList[].desc (STRING)
    ├── complianceInfoList[].propertyList[].excludeVidMap (OBJECT)
    ├── complianceInfoList[].propertyList[].excludeVidMap.$key (STRING)
    ├── complianceInfoList[].propertyList[].excludeVidMap.$value[] (INTEGER[])
    ├── complianceInfoList[].propertyList[].inputNum (INTEGER)
    ├── complianceInfoList[].propertyList[].inputType (INTEGER)
    ├── complianceInfoList[].propertyList[].langDescMap (OBJECT)
    ├── complianceInfoList[].propertyList[].langDescMap.$key (STRING)
    ├── complianceInfoList[].propertyList[].langDescMap.$value (STRING)
    ├── complianceInfoList[].propertyList[].max (INTEGER)
    ├── complianceInfoList[].propertyList[].min (INTEGER)
    ├── complianceInfoList[].propertyList[].needTransLang[] (STRING[])
    ├── complianceInfoList[].propertyList[].parentPid (INTEGER)
    ├── complianceInfoList[].propertyList[].parentVidList[] (INTEGER[])
    ├── complianceInfoList[].propertyList[].propertyId (INTEGER)
    ├── complianceInfoList[].propertyList[].propertyName (STRING)
    ├── complianceInfoList[].propertyList[].propertyValueList[] (OBJECT[])
    ├── complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap (OBJECT)
    ├── complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap.$key (STRING)
    ├── complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap.$value (STRING)
    ├── complianceInfoList[].propertyList[].propertyValueList[].parentVidList[] (INTEGER[])
    ├── complianceInfoList[].propertyList[].propertyValueList[].valueName (STRING)
    ├── complianceInfoList[].propertyList[].propertyValueList[].vid (INTEGER)
    ├── complianceInfoList[].propertyList[].selectNum (INTEGER)
    ├── complianceInfoList[].propertyList[].unit (STRING)
    ├── complianceInfoList[].propertyList[].valuePrecision (INTEGER)
    ├── complianceInfoList[].repDetailList[] (OBJECT[])
    ├── complianceInfoList[].repDetailList[].endTimestamp (INTEGER)
    ├── complianceInfoList[].repDetailList[].personType (INTEGER)
    ├── complianceInfoList[].repDetailList[].repAddressInfo (OBJECT)
    ├── complianceInfoList[].repDetailList[].repAddressInfo.addressLineOne (STRING)
    ├── complianceInfoList[].repDetailList[].repAddressInfo.city (STRING)
    ├── complianceInfoList[].repDetailList[].repAddressInfo.regionName (STRING)
    ├── complianceInfoList[].repDetailList[].repAddressInfo.stateName (STRING)
    ├── complianceInfoList[].repDetailList[].repId (INTEGER)
    ├── complianceInfoList[].repDetailList[].repName (STRING)
    ├── complianceInfoList[].repDetailList[].repStatus (INTEGER)
    ├── complianceInfoList[].repDetailList[].startTimestamp (INTEGER)
    ├── complianceInfoList[].status (INTEGER)
```

> Partner **Response** 表仅含顶层字段；`result` 下全部子字段按 **Response 表层级** 与 **Response Example** 合并展开。

### Partner Response 表（HTML 导出可见行）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | errorCode |
| errorMsg | STRING | errorMsg |
| result | OBJECT | result |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| complianceInfoList[] | OBJECT[] | Partner Response Example |
| complianceInfoList[].complianceType | INTEGER | Partner Response Example |
| complianceInfoList[].desc | STRING | Partner Response Example |
| complianceInfoList[].name | STRING | Partner Response Example |
| complianceInfoList[].propertyList[] | OBJECT[] | Partner Response Example |
| complianceInfoList[].propertyList[].controlType | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].desc | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].excludeVidMap | OBJECT | Partner Response Example |
| complianceInfoList[].propertyList[].excludeVidMap.$key | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].excludeVidMap.$value[] | INTEGER[] | Partner Response Example |
| complianceInfoList[].propertyList[].inputNum | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].inputType | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].langDescMap | OBJECT | Partner Response Example |
| complianceInfoList[].propertyList[].langDescMap.$key | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].langDescMap.$value | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].max | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].min | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].needTransLang[] | STRING[] | Partner Response Example |
| complianceInfoList[].propertyList[].parentPid | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].parentVidList[] | INTEGER[] | Partner Response Example |
| complianceInfoList[].propertyList[].propertyId | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].propertyName | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[] | OBJECT[] | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap | OBJECT | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap.$key | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].langValueNameMap.$value | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].parentVidList[] | INTEGER[] | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].valueName | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].propertyValueList[].vid | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].selectNum | INTEGER | Partner Response Example |
| complianceInfoList[].propertyList[].unit | STRING | Partner Response Example |
| complianceInfoList[].propertyList[].valuePrecision | INTEGER | Partner Response Example |
| complianceInfoList[].repDetailList[] | OBJECT[] | Partner Response Example |
| complianceInfoList[].repDetailList[].endTimestamp | INTEGER | Partner Response Example |
| complianceInfoList[].repDetailList[].personType | INTEGER | Partner Response Example |
| complianceInfoList[].repDetailList[].repAddressInfo | OBJECT | Partner Response Example |
| complianceInfoList[].repDetailList[].repAddressInfo.addressLineOne | STRING | Partner Response Example |
| complianceInfoList[].repDetailList[].repAddressInfo.city | STRING | Partner Response Example |
| complianceInfoList[].repDetailList[].repAddressInfo.regionName | STRING | Partner Response Example |
| complianceInfoList[].repDetailList[].repAddressInfo.stateName | STRING | Partner Response Example |
| complianceInfoList[].repDetailList[].repId | INTEGER | Partner Response Example |
| complianceInfoList[].repDetailList[].repName | STRING | Partner Response Example |
| complianceInfoList[].repDetailList[].repStatus | INTEGER | Partner Response Example |
| complianceInfoList[].repDetailList[].startTimestamp | INTEGER | Partner Response Example |
| complianceInfoList[].status | INTEGER | Partner Response Example |
| errorCode | INTEGER | errorCode |
| errorMsg | STRING | errorMsg |
| result | OBJECT | result |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_metadata_get.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "productId": 1   } }'
```
