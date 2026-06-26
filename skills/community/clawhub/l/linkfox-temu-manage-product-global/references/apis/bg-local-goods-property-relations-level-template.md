# 车型库层级模板 — `bg.local.goods.property.relations.level.template`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_property_relations_level_template.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.property.relations.level.template`，业务载荷放在 Body 的 `params` |

**Description:** Obtaining the hierarchical attribute value and hierarchical id of vehicle type library data（获取车型库的层级属性值与层级 ID）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── catId              ← 必填，叶子类目
    └── relationType       ← 必填，车型库传 1
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | LONG | **是** | 商品类目 ID。须为**叶子类目**，且与 `category_version` 所指定类目树类型下的叶子类目一致 |
| relationType | INTEGER | **是** | 关系类型；查询**兼容车型库**（compatible vehicle models database）时传 **`1`** |

#### `relationType`（已知）

| 值 | 说明 |
|----|------|
| `1` | Query the database of compatible vehicle models |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationType": 1
  }
}
```

> **勿**使用旧文档中的 `pid`、`levelId`；官方入参仅为 **`catId`** + **`relationType`**。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── levelPropertyDependencyList[]
        ├── relationId
        ├── propertyDependencyId
        ├── parentPropertyDependencyId
        ├── propertyName
        └── level
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information |
| result.levelPropertyDependencyList | OBJECT[] | 层级属性依赖列表，见下表 |

### `result.levelPropertyDependencyList[]`

描述在给定 **relationId**（兼容车型库）下共有多少层级、每层属性值分类名（`propertyName`）、层级序号（`level`）以及层级之间的父子关系。**不同 relationId 下，同一 level 可能对应不同的 `propertyDependencyId`**。

| 参数 | 类型 | 说明 |
|------|------|------|
| relationId | LONG | 兼容车型库 ID。不同国家/类目的兼容车型库不同，用该 ID 标识对应数据库 |
| propertyDependencyId | LONG | 属性依赖 ID，对应 `propertyName`；表示该 **relationId** 下的当前层级节点 |
| parentPropertyDependencyId | LONG | 上一级（父级）的 `propertyDependencyId` |
| propertyName | STRING | 兼容车型属性的分类名称，如 brand、manufacturer、model、year、trim、variant、engine 等 |
| level | INTEGER | 层级序号，表示该节点在兼容车型库层级中的位置 |

#### 字段关系示意

```text
relationId（车型库）
  └── level=1  propertyName=Brand      propertyDependencyId=A, parent=0
        └── level=2  propertyName=Model propertyDependencyId=B, parent=A
              └── level=3  ...
```

> 下一步 [relations.template](./bg-local-goods-property-relations-template.md) 使用 **`relationId`** + **`propertyRelationQueryDTOList`** 拉取各层可选 `propertyValue`；不传查询列表时返回 level 1 全部值。后续 [property.relations](./bg-local-goods-property-relations.md) 按 `goodsId` 读取商品已选数据。

---

## 与同族接口协作

```text
1. bg.local.goods.property.relations.level.template（本接口）
   入参：catId + relationType=1
   出参：result.levelPropertyDependencyList[]（relationId、propertyDependencyId、level、propertyName 等）

2. bg.local.goods.property.relations.template
   入参：catId + relationId + relationType=1 + propertyRelationQueryDTOList（可选）
   出参：result.parentPropValDepMapDTOList[] → propValDepDTOList[]（propertyValueId、propertyValue、isLeafProperty 等）

3. bg.local.goods.property.relations
   入参：goodsId + relationId + relationType=1 + queryLastVersion
   出参：商品已保存的兼容车型关联

4. partial.update / update
   → goodsVehiclePropertyRelation 写回
```

---

## 示例

```bash
python scripts/global_manage_property_relations_level_template.py '{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationType": 1
  }
}'
```
