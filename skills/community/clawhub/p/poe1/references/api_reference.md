# Poe.ninja API 参考文档

完整的 poe.ninja API 文档和响应示例。

## 基础 URL

```
https://poe.ninja/api/data
```

## 数据端点

### currencyoverview

用于通货类物品（Currency、Fragment）。

**URL 格式：**
```
https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type={TYPE}
```

**支持类型：**
- `Currency` - 主要通货（Chaos Orb、Divine Orb、Mirror of Kalandra 等）
- `Fragment` - 碎片类物品

### itemoverview

用于所有其他物品类型。

**URL 格式：**
```
https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type={TYPE}
```

**支持类型：** 见 SKILL.md 中的完整列表。

---

## 响应结构

### Currency 响应详解

```json
{
  "lines": [
    {
      "currencyTypeName": "Divine Orb",
      "pay": {
        "id": 0,
        "league_id": 161,
        "pay_currency_id": 22,
        "get_currency_id": 1,
        "sample_time_utc": "2023-03-25T20:33:07.1089319Z",
        "count": 59,
        "value": 0.0000070301,
        "data_point_count": 1,
        "includes_secondary": true,
        "listing_count": 252
      },
      "receive": {
        "id": 0,
        "league_id": 161,
        "pay_currency_id": 1,
        "get_currency_id": 22,
        "sample_time_utc": "2023-03-25T20:33:07.1089319Z",
        "count": 33,
        "value": 146900,
        "data_point_count": 1,
        "includes_secondary": true,
        "listing_count": 161
      },
      "paySparkLine": {
        "data": [0, 1.5, 2.1, 2.8, 3.2, 2.9, 3.5],
        "totalChange": 42.25
      },
      "receiveSparkLine": {
        "data": [0, -0.5, -1.2, -1.8, -2.1, -2.5, -3.92],
        "totalChange": -3.92
      },
      "chaosEquivalent": 143915.04,
      "lowConfidencePaySparkLine": {
        "data": [],
        "totalChange": 42.25
      },
      "lowConfidenceReceiveSparkLine": {
        "data": [],
        "totalChange": -3.92
      },
      "detailsId": "divine-orb"
    }
  ],
  "currencyDetails": [
    {
      "id": 22,
      "icon": "https://web.poecdn.com/gen/image/...",
      "name": "Divine Orb",
      "tradeId": "divine"
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `currencyTypeName` | string | 通货名称 |
| `chaosEquivalent` | float | Chaos 等值价格 |
| `pay` | object | 购买数据（用 Chaos 买该通货） |
| `receive` | object | 出售数据（卖该通货换 Chaos） |
| `pay.value` | float | 购买 1 个该通货需要的 Chaos 数量 |
| `receive.value` | float | 出售 1 个该通货获得的 Chaos 数量 |
| `pay.listing_count` | int | 购买挂牌数量 |
| `receive.listing_count` | int | 出售挂牌数量 |
| `paySparkLine` | object | 购买价格趋势 |
| `receiveSparkLine` | object | 出售价格趋势 |
| `totalChange` | float | 价格变化百分比 |
| `detailsId` | string | 唯一标识符，用于 URL slug |
| `currencyDetails` | array | 通货详情列表 |
| `tradeId` | string | 官方交易站 ID |

---

### Item 响应详解

```json
{
  "lines": [
    {
      "id": 22607,
      "name": "Golden Oil",
      "icon": "https://web.poecdn.com/gen/image/...",
      "baseType": "Golden Oil",
      "stackSize": 10,
      "itemClass": 5,
      "sparkline": {
        "data": [0, -0.5, -0.8, -1.2, -1.5, -1.3, -1.67],
        "totalChange": -1.67
      },
      "lowConfidenceSparkline": {
        "data": [],
        "totalChange": -1.67
      },
      "implicitModifiers": [],
      "explicitModifiers": [],
      "flavourText": "",
      "chaosValue": 59,
      "exaltedValue": 2.42,
      "divineValue": 0.23,
      "count": 99,
      "detailsId": "golden-oil",
      "listingCount": 1997
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 物品唯一 ID |
| `name` | string | 物品名称 |
| `baseType` | string | 基底类型 |
| `icon` | string | 图标 URL |
| `stackSize` | int | 堆叠大小（如适用） |
| `itemClass` | int | 物品类别 ID |
| `chaosValue` | float | Chaos 价格 |
| `exaltedValue` | float | Exalted 价格（历史遗留） |
| `divineValue` | float | Divine 价格 |
| `sparkline` | object | 价格趋势数据 |
| `totalChange` | float | 价格变化百分比 |
| `count` | int | 交易样本数 |
| `detailsId` | string | 唯一标识符 |
| `listingCount` | int | 当前在售数量 |
| `implicitModifiers` | array | 隐式词缀 |
| `explicitModifiers` | array | 显式词缀 |
| `flavourText` | string | 风味文字 |
| `corrupted` | bool | 是否已腐化（如适用） |
| `gemLevel` | int | 宝石等级（如适用） |
| `gemQuality` | int | 宝石品质（如适用） |
| `mapTier` | int | 地图阶级（如适用） |
| `levelRequired` | int | 需求等级（如适用） |
| `links` | int | 连结数（如适用） |
| `variant` | string | 变体信息（如 5/20c） |

---

## 特殊物品类型说明

### SkillGem（技能宝石）

包含变体信息，如品质、等级、腐化状态：

```json
{
  "name": "Awakened Enlighten Support",
  "variant": "5/20c",
  "gemLevel": 5,
  "gemQuality": 20,
  "corrupted": true,
  "chaosValue": 104767.39
}
```

**变体格式：** `{level}/{quality}{corrupted}`，如 `5/20c` 表示 5 级 20 品质已腐化。

### BaseType（基底类型）

包含基底类型和影响信息：

```json
{
  "name": "Accumulator Wand",
  "baseType": "Accumulator Wand",
  "variant": "Shaper/Elder",
  "itemType": "Wand",
  "levelRequired": 86,
  "chaosValue": 274791.32
}
```

### UniqueWeapon/UniqueArmour/UniqueAccessory（传奇装备）

包含连结数和基底信息：

```json
{
  "name": "Voidforge",
  "baseType": "Infernal Sword",
  "links": 6,
  "itemType": "Two Handed Sword",
  "levelRequired": 67,
  "chaosValue": 137105.86
}
```

---

## 价格趋势数据

`sparkline` 对象包含 7 天价格趋势：

```json
{
  "sparkline": {
    "data": [0, 1.5, 2.1, 2.8, 3.2, 2.9, 3.5],
    "totalChange": 3.5
  }
}
```

- `data` 数组包含 7 个数据点，第一个始终为 0
- `totalChange` 是整体变化百分比

**低置信度数据：**
- `lowConfidenceSparkline` - 交易量低时的价格趋势
- 当交易量过低时，价格可能不准确

---

## 错误处理

API 返回标准 HTTP 状态码：

- `200` - 成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `429` - 请求过于频繁
- `500` - 服务器错误

---

## 速率限制

- 建议每个请求间隔至少 1 秒
- 避免短时间内大量请求
- 数据每小时更新一次，无需频繁刷新

---

## 联盟名称

当前联盟名称会随赛季变化：

- `Settlers` - 当前赛季（示例）
- `Standard` - 永久标准
- `Hardcore` - 永久专家

查看当前联盟：https://poe.ninja
