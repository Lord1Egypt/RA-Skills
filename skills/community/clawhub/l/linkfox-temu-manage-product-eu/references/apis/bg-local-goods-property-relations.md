# 商品属性关联数据查询 — `bg.local.goods.property.relations`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_property_relations.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d93de48fc77d49d38764292d69dc5abd |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.property.relations`，业务载荷放在 Body 的 `params` |

**Description:** 查询商品已关联的关系型属性数据（如兼容车型库 / compatible vehicle models）。**不是**按 `catId` 拉车型库层级/选项的接口（见 [level.template](./bg-local-goods-property-relations-level-template.md)、[relations.template](./bg-local-goods-property-relations-template.md)）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId              ← 必填
    ├── relationId           ← 必填
    ├── relationType         ← 必填（车型库填 1）
    └── queryLastVersion     ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | goods id |
| relationId | LONG | **是** | 关系库 ID。不同国家/类目的兼容车型库不同，用该 ID 查询对应 **compatible vehicle models** 数据库 |
| relationType | INTEGER | **是** | 关系类型；查询兼容车型库时传 **`1`** |
| queryLastVersion | BOOLEAN | **是** | 版本选择，见下表 |

#### `queryLastVersion`

| 值 | 行为 |
|----|------|
| `true` | 返回商品**最新版本**上的关联数据 |
| `false` | 优先返回**在售/生效版本**；若无生效版本，则退回最新版本 |

#### `relationType`（已知）

| 值 | 说明 |
|----|------|
| `1` | 查询 **compatible vehicle models**（兼容车型）关系库 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "relationId": 10001,
    "relationType": 1,
    "queryLastVersion": true
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "relationId": 10001,
    "relationType": 1,
    "queryLastVersion": false
  }
}
```

> **勿**使用旧文档中的 `catId`、`pid`、`pageNo`、`keyword` 等字段；本接口为**按商品 + 关系库 ID** 读取已绑定数据。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information（子字段在 Partner 文档中展开） |

官方 Response 表中 **`result` 未在提供的片段中展开**。返回体通常包含该商品在指定 `relationId` 关系库下已选的兼容车型/级联属性值等，具体字段名以 Partner 后台为准。

### 与编辑接口的对应关系（写入侧参考）

发品/编辑时写入车型关联的块为 `request.goodsVehiclePropertyRelation`（见 [partial.update](./bg-local-goods-partial-update.md#requestgoodsvehiclepropertyrelation)）：

| 字段 | 类型 | 说明 |
|------|------|------|
| relationId | LONG | `relationType=1` 时对应兼容车型库 ID |
| relationType | INTEGER | 关系类型 |
| ktype | LONG[] | K-type 映射 |
| leafPropertyValueDependencyIdList | LONG[] | 末级属性值 dependency id |

本接口 **`property.relations` 为读取**；`result` 内字段命名可能与上表一致或嵌套包装，以实网返回为准。

---

## 与同族接口协作（车型库）

```text
1. bg.local.goods.property.relations.level.template
   → 按 **catId + relationType=1** 拉 `result.levelPropertyDependencyList[]`（含 `relationId`、`propertyDependencyId`、`level`、`propertyName`）

2. bg.local.goods.property.relations.template
   → 按 relationId + propertyRelationQueryDTOList 拉各层 propertyValue（见该接口文档）

3. bg.local.goods.property.relations（本接口）
   → 按 goodsId + relationId + relationType=1 + queryLastVersion
     读取商品上已保存的兼容车型关联数据

4. bg.local.goods.partial.update / update
   → goodsVehiclePropertyRelation 写回 ktype / leafPropertyValueDependencyIdList 等
```

---

## 示例

```bash
python scripts/eu_manage_property_relations.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456789,
    "relationId": 10001,
    "relationType": 1,
    "queryLastVersion": true
  }
}'
```
