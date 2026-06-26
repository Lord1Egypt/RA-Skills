# 商品编辑 API — 参数参考

经 `POST /temu/proxy` 转发，网关见 [api.md](./api.md)。

---

## 1. 更新商品 — `temu.goods.update`

- **sub_menu_code**：`e93835a33b7a40ce8769fdf75561aff4`
- **脚本**：`scripts/us_goods_update.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | integer | 是 | 货品 ID |
| supplierId | integer | 是 | 供应商 ID |
| productWhExtAttrReq | object | 是 | 仓配扩展 |
| productWhExtAttrReq.productOrigin.region1ShortName | string | 是 | 产地一级区域二字码（如 `CN`、`US`） |
| productWhExtAttrReq.productOrigin.region2Id | integer | 条件 | 省份 ID（`region1ShortName=CN` 时必填） |

### 响应

成功时 `success=true`，`result` 可为空对象。

### 示例

```bash
python scripts/us_goods_update.py '{
  "accessToken": "TOKEN",
  "productId": 604269868588112,
  "supplierId": 123,
  "productWhExtAttrReq": {
    "productOrigin": { "region1ShortName": "CN", "region2Id": 310000 }
  }
}'
```

---

## 2. 编辑商品属性 — `temu.goods.edit.property`

- **sub_menu_code**：`93fecd4d21fd441a8abcfc1497fa085e`
- **脚本**：`scripts/us_goods_edit_property.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | integer | 是 | 货品 ID |
| productProperties | array | 是 | 属性列表 |

#### `productProperties[]`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pid | integer | 是 | 属性 ID |
| templatePid | integer | 是 | 模板属性 ID |
| refPid | integer | 是 | 引用属性 ID |
| vid | integer | 否 | 属性值 ID，无则传 0 |
| propName | string | 是 | 属性名 |
| propValue | string | 是 | 属性值 |
| numberInputValue | string | 是 | 数值录入 |
| valueUnit | string | 否 | 单位，无则空串 |

### 示例

```bash
python scripts/us_goods_edit_property.py '{
  "accessToken": "TOKEN",
  "productId": 604269868588112,
  "productProperties": [{
    "pid": 1, "templatePid": 1, "refPid": 1,
    "vid": 100, "propName": "Material", "propValue": "Cotton",
    "numberInputValue": "", "valueUnit": ""
  }]
}'
```

---

## 3. 编辑敏感品属性 — `temu.goods.edit.sensitive.attr`

- **sub_menu_code**：`fc3de2c8546a496d8a5be8d36953e1bd`
- **脚本**：`scripts/us_goods_edit_sensitive.py`

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | integer | 是 | 货品 ID |
| skuReqList | array | 是 | SKU 敏感属性列表 |

#### `skuReqList[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| productSkuId | integer | 货品 SKU ID |
| productSkuSensitiveAttrReq.isSensitive | integer | 0 非敏感，1 敏感 |
| productSkuSensitiveAttrReq.sensitiveList | array | 敏感类型码（如纯电、内电、液体等） |
| productSkuSensitiveLimitReq | object | 敏感限制（容量、刀长等），无限制可传 `{}` |

### 示例

```bash
python scripts/us_goods_edit_sensitive.py '{
  "accessToken": "TOKEN",
  "productId": 604269868588112,
  "skuReqList": [{
    "productSkuId": 58224724203874,
    "productSkuSensitiveAttrReq": { "isSensitive": 0, "sensitiveList": [] },
    "productSkuSensitiveLimitReq": {}
  }]
}'
```

---

## 4. 半托管货品迁移 — `temu.goods.migrate`

- **sub_menu_code**：`a8f8f3dca5ac4e2c8b9e7bc9d64704c8`
- **脚本**：`scripts/us_goods_migrate.py`
- **用途**：同主体下将全托管店铺货品搬运至半托管。

### 业务参数（`params`）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| migrationList | array | 是 | 搬运列表 |

#### `migrationList[]` 主要字段

| 字段 | 类型 | 说明 |
|------|------|------|
| productSemiManagedReq.bindSiteIds | array | 绑定站点 |
| productSemiManagedReq.semiManagedSiteMode | integer | 半托管售卖模式 |
| productWarehouseRouteReq.targetRouteList | array | 站点-仓路由 `{ siteIdList, warehouseId }` |
| skcDetails | array | SKC/SKU 规格明细 |

### 示例

```bash
python scripts/us_goods_migrate.py '{
  "accessToken": "TOKEN",
  "migrationList": [{ "productSemiManagedReq": { "bindSiteIds": [100] } }]
}'
```
