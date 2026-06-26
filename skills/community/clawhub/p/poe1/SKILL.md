---
name: poe-ninja-api
description: Path of Exile 市场价格查询工具。通过 poe.ninja API 获取游戏物品实时价格数据。适用场景：(1) 查询通货汇率（Chaos/Divine/Mirror 等）(2) 查询装备、技能宝石、地图等物品价格 (3) 查询预言卡、圣甲虫、精髓等消耗品价格 (4) 获取价格趋势数据 (5) 跨联盟价格对比。支持所有物品类型的实时行情查询。
---

# Poe Ninja API

查询 Path of Exile 游戏内物品实时市场价格，通过 poe.ninja API 获取数据。

## 快速开始

### 基础 API 端点

所有 API 端点基于 `https://poe.ninja/api/data/`

**两种数据类型：**
- `currencyoverview` - 通货类（Currency、Fragment）
- `itemoverview` - 物品类（其余所有类型）

**必需参数：**
- `league` - 联盟名称（如 `Settlers`、`Standard`、`Hardcore`）
- `type` - 物品类型

## 物品类型列表

### 通货类（currencyoverview）

| 类型 | 说明 |
|------|------|
| `Currency` | 通货（Chaos、Divine、Mirror 等） |
| `Fragment` | 碎片（Sacrifice at Dusk 等） |

### 物品类（itemoverview）

| 类型 | 说明 |
|------|------|
| `Oil` | 油（Golden Oil 等） |
| `Incubator` | 孵化器 |
| `Scarab` | 圣甲虫 |
| `Fossil` | 化石 |
| `Resonator` | 共振器 |
| `Essence` | 精髓 |
| `DivinationCard` | 预言卡 |
| `SkillGem` | 技能宝石 |
| `BaseType` | 基底类型 |
| `HelmetEnchant` | 头盔附魔 |
| `UniqueMap` | 传奇地图 |
| `Map` | 地图 |
| `UniqueJewel` | 传奇珠宝 |
| `UniqueFlask` | 传奇药水 |
| `UniqueWeapon` | 传奇武器 |
| `UniqueArmour` | 传奇护甲 |
| `UniqueAccessory` | 传奇饰品 |
| `Beast` | 野兽 |
| `Vial` | 小瓶 |
| `DeliriumOrb` | 谵妄球 |
| `Omen` | 征兆 |
| `UniqueRelic` | 传奇遗物 |
| `ClusterJewel` | 集群珠宝 |
| `BlightedMap` | 凋零地图 |
| `BlightRavagedMap` | 凋零掠夺地图 |
| `Invitation` | 邀请函 |
| `Memory` | 记忆 |
| `Coffin` | 棺材 |
| `AllflameEmber` | 全燃余烬 |

## API 调用示例

### 查询通货价格

```
GET https://poe.ninja/api/data/currencyoverview?league=Settlers&type=Currency
```

### 查询传奇武器价格

```
GET https://poe.ninja/api/data/itemoverview?league=Settlers&type=UniqueWeapon
```

### 查询预言卡价格

```
GET https://poe.ninja/api/data/itemoverview?league=Settlers&type=DivinationCard
```

## 响应数据结构

### Currency 响应

```json
{
  "lines": [
    {
      "currencyTypeName": "Mirror of Kalandra",
      "chaosEquivalent": 143915.04,
      "pay": { "value": 0.0000070301 },
      "receive": { "value": 146900 },
      "paySparkLine": { "totalChange": 42.25 },
      "receiveSparkLine": { "totalChange": -3.92 },
      "detailsId": "mirror-of-kalandra"
    }
  ],
  "currencyDetails": [
    {
      "id": 22,
      "name": "Mirror of Kalandra",
      "tradeId": "mirror",
      "icon": "https://..."
    }
  ]
}
```

**关键字段：**
- `chaosEquivalent` - Chaos 等值价格
- `pay.value` - 购买时需要的货币数量
- `receive.value` - 出售时获得的货币数量
- `totalChange` - 价格变化百分比

### Item 响应

```json
{
  "lines": [
    {
      "id": 22607,
      "name": "Golden Oil",
      "baseType": "Golden Oil",
      "chaosValue": 59,
      "exaltedValue": 2.42,
      "divineValue": 0.23,
      "sparkline": { "totalChange": -1.67 },
      "detailsId": "golden-oil",
      "listingCount": 1997
    }
  ]
}
```

**关键字段：**
- `chaosValue` - Chaos 价格
- `exaltedValue` - Exalted 价格
- `divineValue` - Divine 价格
- `sparkline.totalChange` - 价格变化趋势
- `listingCount` - 在售数量

## 使用脚本

### 脚本列表

| 脚本 | 说明 |
|------|------|
| `get_currency.py` | 获取通货价格 |
| `get_item.py` | 获取物品价格 |
| `search_item.py` | 搜索特定物品 |

## 常用查询

### 查询 Divine Orb 价格

使用 `get_currency.py` 查询：

```bash
python scripts/get_currency.py --league Settlers --search "divine"
```

### 查询特定传奇装备

使用 `get_item.py` 查询：

```bash
python scripts/get_item.py --league Settlers --type UniqueWeapon --search "Starforge"
```

### 获取价格趋势

响应中的 `sparkline` 字段包含价格趋势数据，`totalChange` 表示变化百分比。

## 注意事项

1. **联盟名称** - 每个新赛季联盟名称不同，需要使用当前联盟名称
2. **价格更新** - poe.ninja 数据每小时更新一次
3. **低置信度数据** - `lowConfidenceSparkline` 表示交易量低，价格可能不准确
4. **图标链接** - 响应中的 `icon` 字段提供物品图标 URL

## 资源文件

### references/
- `api_reference.md` - 完整 API 文档和响应示例

### scripts/
- `get_currency.py` - 查询通货价格
- `get_item.py` - 查询物品价格
- `search_item.py` - 搜索物品
