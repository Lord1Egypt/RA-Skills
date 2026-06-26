# 关系属性值查询 — `bg.local.goods.property.relations.template`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_property_relations_template.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=bfd820e01f23408689b2b532816e475d |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.property.relations.template`，业务载荷放在 Body 的 `params` |

**Description:** Query the full quantum attribute by the dependency id of the parent attribute value and the hierarchical id（按父级属性值依赖 ID 查询下级全量可选属性值，用于兼容车型库级联选择）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── catId                         ← 必填
    ├── relationId                    ← 必填
    ├── relationType                  ← 必填，车型库传 1
    └── propertyRelationQueryDTOList[]  ← 选填
        ├── propertyDependencyId
        └── parentPropertyValueDependencyId
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | LONG | **是** | 商品类目 ID。须为**叶子类目**，且与 `category_version` 所指定类目树类型下的叶子类目一致 |
| relationId | LONG | **是** | Relation id（兼容车型库 ID，通常来自 [level.template](./bg-local-goods-property-relations-level-template.md) 的 `levelPropertyDependencyList[].relationId`） |
| relationType | INTEGER | **是** | 关系类型；查询**兼容车型库**时传 **`1`** |
| propertyRelationQueryDTOList | OBJECT[] | 否 | 查询条件；用于指定 `propertyDependencyId` 与 `parentPropertyValueDependencyId`。**留空或不传时，返回全部 level 1 的 `propertyValueId`** |

#### `relationType`（已知）

| 值 | 说明 |
|----|------|
| `1` | Query the database of compatible vehicle models |

### `propertyRelationQueryDTOList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| propertyDependencyId | LONG | 否 | 属性依赖 ID，对应层级分类名（`propertyName`），表示该 `relationId` 下的当前层级 |
| parentPropertyValueDependencyId | LONG | 否 | 上一级（父级）属性**值**的 dependency id |

> 请求侧为 **`parentPropertyValueDependencyId`**（值级父 ID）；与 [level.template](./bg-local-goods-property-relations-level-template.md) 层级定义中的 **`parentPropertyDependencyId`**（层级结构父 ID）名称不同，勿混用。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationId": 10001,
    "relationType": 1
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationId": 10001,
    "relationType": 1,
    "propertyRelationQueryDTOList": [
      {
        "propertyDependencyId": 200,
        "parentPropertyValueDependencyId": 0
      }
    ]
  }
}
```

> **勿**使用旧文档中的 `pid`、`parentVid`、`levelId`。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── parentPropValDepMapDTOList[]
        ├── parentPropertyValueDependencyId
        └── propValDepDTOList[]
            ├── propertyDependencyId
            ├── propertyValueDependencyId
            ├── parentPropertyValueDependencyId
            ├── propertyValueId
            ├── propertyValue
            └── isLeafProperty
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information |
| result.parentPropValDepMapDTOList | OBJECT[] | 父属性值与其子属性值列表 |

### `result.parentPropValDepMapDTOList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentPropertyValueDependencyId | LONG | 父级属性值的 dependency id（上一级） |
| propValDepDTOList | OBJECT[] | 该父值下，下一层级的属性值数据列表 |

### `propValDepDTOList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| propertyDependencyId | LONG | 用于查询层级之间关系的 dependency id |
| propertyValueDependencyId | LONG | 属性值 dependency id，对应当前层级；与 `propertyName` 对应 |
| parentPropertyValueDependencyId | LONG | 父级属性值的 dependency id |
| propertyValueId | LONG | 属性值 ID；与 `propertyValueDependencyId` **一一对应** |
| propertyValue | STRING | 兼容车型枚举展示值，如品牌/年份/发动机等，例：`Toyota`、`1987`、`Base Convertible 2-Door` |
| isLeafProperty | BOOLEAN | `true`：该属性值为**最末级**；`false`：非最末级，可继续级联查询下一层 |

#### 级联查询示意

```text
1. level.template → 得到 relationId、各层 propertyDependencyId / level / propertyName
2. relations.template（本接口）
   - 首次：propertyRelationQueryDTOList 为空 → 返回 level 1 全部 propertyValueId
   - 用户选中某值后：带上 parentPropertyValueDependencyId + propertyDependencyId 再查下一层
   - isLeafProperty=true 的项可作为叶子，写入 goodsVehiclePropertyRelation.leafPropertyValueDependencyIdList
3. property.relations → 按 goodsId 读取商品已保存关联
```

---

## 与同族接口协作

| 步骤 | 接口 | 作用 |
|------|------|------|
| 1 | [level.template](./bg-local-goods-property-relations-level-template.md) | 拉层级定义 `levelPropertyDependencyList[]` |
| 2 | **本接口** | 按 `relationId` + 查询 DTO 拉各层可选 `propertyValue` |
| 3 | [property.relations](./bg-local-goods-property-relations.md) | 读商品已选车型数据 |
| 4 | [partial.update](./bg-local-goods-partial-update.md) | `goodsVehiclePropertyRelation` 写回 |

---

## 示例

```bash
# 拉取 level 1 全部可选值（不传 propertyRelationQueryDTOList）
python scripts/eu_manage_property_relations_template.py '{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationId": 10001,
    "relationType": 1
  }
}'
```

```bash
# 按父级属性值继续查下一层
python scripts/eu_manage_property_relations_template.py '{
  "accessToken": "TOKEN",
  "request": {
    "catId": 12345,
    "relationId": 10001,
    "relationType": 1,
    "propertyRelationQueryDTOList": [
      {
        "propertyDependencyId": 200,
        "parentPropertyValueDependencyId": 987654321
      }
    ]
  }
}'
```
