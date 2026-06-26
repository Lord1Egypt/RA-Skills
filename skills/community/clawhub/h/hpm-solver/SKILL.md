---
name: hpm-solver
description: "哈利波特魔法觉醒(HPM)交易求解器 - 基于多元一次方程组的购买组合穷举求解。支持双系数模型(p/q)、等价物品合并、智能过滤、等价替换还原。触发词：哈皮马求解、HPM求解、魔法觉醒计算、金币求解、宝石求解、购买组合、残值计算、hpm工具、hpm计算器。"
---

# HPM 交易求解器 v5

哈利波特魔法觉醒(HPM)游戏辅助工具，用于求解最优购买组合。

## 核心特性

1. **双系数模型**：Food系数(p) + Plant系数(q) 独立计算
2. **等价分组**：相同价格物品合并，减少运算规模
3. **整除过滤**：高价物品能被低价物品整除且数量足够时过滤
4. **穷举求解**：从大到小穷举所有组合，优先完美解
5. **等价替换还原**：过滤的高价物品在结果中还原显示

---

## 数学模型

```
目标金额 = (plantA*n1 + plantB*n2 + ...) * q + (foodA*m1 + foodB*m2 + ...) * p
```

- **p**：Food系数（菜品乘算系数）
- **q**：Plant系数（植物乘算系数）

---

## 数据优化流程

```
原始物品 → 等价分组 → 整除过滤 → 运算组 → 穷举求解 → 等价替换还原
  41个      31组        17组       最终参与运算
```

**示例**：
- `香煎怪肉排` 和 `烈焰香煎鹅肝` 都是562金基础价格 → 合并为一个运算单元
- 高价物品能被低价物品整除且低价物品数量足够 → 过滤高价物品，记录替换关系
- 求解后根据替换关系还原高价物品

---

## 核心算法代码 (v5)

### solver.js - 完整实现

```javascript
// utils/solver.js - v5
class EquivalenceGroup {
  constructor(basePrice, actualPrice, items, category, maxQuantities) {
    this.basePrice = basePrice
    this.actualPrice = actualPrice
    this.items = items
    this.category = category
    this.maxQuantities = maxQuantities || {}
  }
  
  getMaxQuantity() {
    var minQty = 99
    for (var i = 0; i < this.items.length; i++) {
      var qty = this.maxQuantities[this.items[i]]
      if (qty !== undefined && qty < minQty) minQty = qty
    }
    return minQty
  }
  
  get maxValue() { return this.actualPrice * this.getMaxQuantity() }
}

class Solution {
  constructor(groups, totalCost, residual) {
    this.groups = groups
    this.totalCost = totalCost
    this.residual = residual
    this.isPerfect = residual === 0
  }
  
  getQuantities() {
    var result = {}
    for (var i = 0; i < this.groups.length; i++) {
      var g = this.groups[i]
      if (g.quantity > 0) {
        for (var j = 0; j < g.group.items.length; j++) {
          var item = g.group.items[j]
          result[item] = (result[item] || 0) + g.quantity
        }
      }
    }
    return result
  }
}

class HPMSolver {
  constructor(basePrices, maxQuantities) {
    this.basePrices = basePrices
    this.maxQuantities = maxQuantities || { 
      foods: { gold: {}, diamond: {} }, 
      plants: { gold: {}, diamond: {} } 
    }
  }

  solve(targetGold, targetDiamond, multiplierP, multiplierQ) {
    var allItems = this.buildItems(multiplierP, multiplierQ)
    var goldItems = allItems.filter(function(i) { return i.currency === 'gold' })
    var diamondItems = allItems.filter(function(i) { return i.currency === 'diamond' })
    
    var goldResult = targetGold > 0 && goldItems.length > 0 
      ? this.solveCurrency(targetGold, goldItems) : null
    var diamondResult = targetDiamond > 0 && diamondItems.length > 0 
      ? this.solveCurrency(targetDiamond, diamondItems) : null
    
    var goldGroups = this.groupByPrice(goldItems)
    var goldFiltered = this.filterByDivisibility(goldGroups, targetGold)
    
    return {
      gold: goldResult,
      diamond: diamondResult,
      multiplierP: multiplierP,
      multiplierQ: multiplierQ,
      stats: { 
        goldItemsBefore: goldItems.length, 
        goldGroupsAfter: goldGroups.length, 
        goldGroupsFiltered: goldFiltered.kept.length 
      }
    }
  }

  buildItems(multiplierP, multiplierQ) {
    var items = []
    var maxQty = this.maxQuantities
    
    for (var category in this.basePrices) {
      if (category === 'version' || category === 'updatedAt' || category === 'maxQuantities') continue
      var multiplier = category === 'foods' ? multiplierP : multiplierQ
      
      for (var currency in this.basePrices[category]) {
        var priceData = this.basePrices[category][currency]
        for (var name in priceData) {
          var basePrice = priceData[name]
          var actualPrice = Math.round(basePrice * multiplier)
          var itemMaxQty = 99
          try {
            if (maxQty[category] && maxQty[category][currency] && 
                maxQty[category][currency][name] !== undefined) {
              itemMaxQty = maxQty[category][currency][name]
            }
          } catch (e) {}
          items.push({ 
            name: name, 
            price: actualPrice, 
            basePrice: basePrice, 
            currency: currency, 
            category: category, 
            maxQty: itemMaxQty 
          })
        }
      }
    }
    return items
  }

  groupByPrice(items) {
    var groups = []
    var priceMap = {}
    
    for (var i = 0; i < items.length; i++) {
      var item = items[i]
      var key = item.price + '_' + item.category
      if (!priceMap[key]) priceMap[key] = []
      priceMap[key].push(item)
    }
    
    for (var key in priceMap) {
      var itemList = priceMap[key]
      var maxQuantities = {}
      for (var j = 0; j < itemList.length; j++) {
        maxQuantities[itemList[j].name] = itemList[j].maxQty
      }
      groups.push(new EquivalenceGroup(
        itemList[0].basePrice,
        itemList[0].price,
        itemList.map(function(i) { return i.name }),
        itemList[0].category,
        maxQuantities
      ))
    }
    
    groups.sort(function(a, b) { return a.actualPrice - b.actualPrice })
    return groups
  }

  filterByDivisibility(groups, target) {
    var kept = []
    var filterTable = []
    
    for (var i = 0; i < groups.length; i++) {
      var group = groups[i]
      var canFilter = false
      
      for (var j = 0; j < kept.length; j++) {
        var lowGroup = kept[j]
        if (group.actualPrice % lowGroup.actualPrice === 0) {
          var ratio = group.actualPrice / lowGroup.actualPrice
          if (lowGroup.getMaxQuantity() >= ratio && lowGroup.maxValue >= target) {
            filterTable.push({ 
              highPriceGroup: group, 
              lowPriceGroup: lowGroup, 
              ratio: ratio 
            })
            canFilter = true
            break
          }
        }
      }
      
      if (!canFilter) kept.push(group)
    }
    
    return { kept: kept, filterTable: filterTable }
  }

  solveCurrency(target, items) {
    var groups = this.groupByPrice(items)
    var filtered = this.filterByDivisibility(groups, target)
    
    if (filtered.kept.length === 0) return null
    
    var maxQuantities = filtered.kept.map(function(g) {
      return Math.min(Math.floor(target / g.actualPrice), g.getMaxQuantity())
    })
    
    return this.exhaustiveSolve(target, filtered.kept, maxQuantities, filtered.filterTable)
  }

  exhaustiveSolve(target, groups, maxQuantities, filterTable) {
    var sortedData = groups.map(function(g, i) { 
      return { group: g, maxQty: maxQuantities[i] } 
    }).sort(function(a, b) { return b.group.actualPrice - a.group.actualPrice })
    
    var bestSolution = null
    var minPrice = Math.min.apply(null, groups.map(function(g) { return g.actualPrice }))
    
    function iterate(index, currentCost, currentGroups) {
      if (currentCost > target) return null
      
      if (index === sortedData.length) {
        var residual = target - currentCost
        if (residual >= 0 && residual < minPrice) {
          var solution = new Solution(currentGroups.slice(), currentCost, residual)
          if (solution.isPerfect) return solution
          if (!bestSolution || residual < bestSolution.residual) bestSolution = solution
        }
        return null
      }
      
      var data = sortedData[index]
      var effectiveMaxQty = Math.min(
        data.maxQty, 
        Math.floor((target - currentCost) / data.group.actualPrice)
      )
      
      for (var q = effectiveMaxQty; q >= 0; q--) {
        var cost = currentCost + q * data.group.actualPrice
        if (cost > target) continue
        
        if (q > 0) currentGroups.push({ group: data.group, quantity: q })
        var result = iterate(index + 1, cost, currentGroups)
        if (result && result.isPerfect) return result
        if (q > 0) currentGroups.pop()
      }
      return null
    }
    
    var perfectSolution = iterate(0, 0, [])
    var solution = perfectSolution || bestSolution
    
    if (solution && filterTable && filterTable.length > 0) {
      solution = this.tryReplaceWithHighPrice(solution, filterTable)
    }
    if (solution) solution.filterTable = filterTable
    
    return solution
  }

  tryReplaceWithHighPrice(solution, filterTable) {
    var quantities = solution.getQuantities()
    var sortedFilterTable = filterTable.slice().sort(function(a, b) { 
      return b.ratio - a.ratio 
    })
    var remainingQuantities = {}
    for (var k in quantities) remainingQuantities[k] = quantities[k]
    
    var newGroups = []
    
    for (var i = 0; i < sortedFilterTable.length; i++) {
      var relation = sortedFilterTable[i]
      var lowItemName = relation.lowPriceGroup.items[0]
      
      if (remainingQuantities[lowItemName] !== undefined) {
        var lowQty = remainingQuantities[lowItemName]
        var maxReplace = Math.floor(lowQty / relation.ratio)
        
        if (maxReplace > 0) {
          var actualReplace = Math.min(maxReplace, relation.highPriceGroup.getMaxQuantity())
          if (actualReplace > 0) {
            newGroups.push({ group: relation.highPriceGroup, quantity: actualReplace })
            remainingQuantities[lowItemName] -= actualReplace * relation.ratio
          }
        }
      }
    }
    
    if (newGroups.length === 0) return solution
    
    for (var j = 0; j < solution.groups.length; j++) {
      var g = solution.groups[j]
      if (g.quantity > 0) {
        var remaining = remainingQuantities[g.group.items[0]] || 0
        if (remaining > 0) newGroups.push({ group: g.group, quantity: remaining })
      }
    }
    
    var newSolution = new Solution(newGroups, solution.totalCost, solution.residual)
    newSolution.isPerfect = solution.isPerfect
    return newSolution
  }
}

module.exports = { 
  HPMSolver: HPMSolver, 
  EquivalenceGroup: EquivalenceGroup, 
  Solution: Solution 
}
```

---

## 算法详解

### 1. 等价分组 (groupByPrice)

将相同价格的物品归为一组，减少运算规模。

```javascript
// 示例：香煎怪肉排(562金) 和 烈焰香煎鹅肝(562金) 合并
{
  actualPrice: 562,
  items: ['香煎怪肉排', '烈焰香煎鹅肝'],
  category: 'foods'
}
```

### 2. 整除过滤 (filterByDivisibility)

高价物品若能被低价物品整除，且低价物品数量足够，则过滤高价物品。

```javascript
// 示例：鳃囊草(6金) × 4 = 毒牙天竺葵(24金)
// 如果鳃囊草数量足够，则过滤毒牙天竺葵
filterTable.push({
  highPriceGroup: 毒牙天竺葵组,
  lowPriceGroup: 鳃囊草组,
  ratio: 4
})
```

### 3. 穷举求解 (exhaustiveSolve)

从大到小穷举所有可能的购买组合：

1. 按价格降序排列运算组
2. 对每个组，从最大数量开始尝试
3. 找到完美解立即返回，否则记录最小残值解

### 4. 等价替换还原 (tryReplaceWithHighPrice)

根据 filterTable 将低价物品替换回高价物品：

```javascript
// 如果解中有鳃囊草 × 8，且 filterTable 中有 ratio=4 的关系
// 则可以将 鳃囊草 × 4 替换为 毒牙天竺葵 × 1
// 最终：鳃囊草 × 4 + 毒牙天竺葵 × 1
```

---

## 数据结构

### 价格数据格式

```json
{
  "version": 1,
  "updatedAt": "2026-03-25",
  "foods": {
    "gold": { "奶油蟹粉面": 346, "香煎怪肉排": 562 },
    "diamond": { "野心与荣耀之宴": 14 }
  },
  "plants": {
    "gold": { "火焰肉桂": 34, "鳃囊草": 6 },
    "diamond": { "水仙": 2 }
  },
  "maxQuantities": {
    "foods": { "gold": { "奶油蟹粉面": 99 } },
    "plants": { "gold": { "鳃囊草": 99 } }
  }
}
```

### 求解结果格式

```javascript
{
  gold: {
    groups: [
      { group: EquivalenceGroup, quantity: 8 },
      { group: EquivalenceGroup, quantity: 1 }
    ],
    totalCost: 7494,
    residual: 6,
    isPerfect: false,
    filterTable: [...]
  },
  diamond: null,
  multiplierP: 1.5,
  multiplierQ: 1.0,
  stats: {
    goldItemsBefore: 41,
    goldGroupsAfter: 31,
    goldGroupsFiltered: 17
  }
}
```

---

## 微信小程序集成

### 项目结构

```
hpm-miniprogram-v13/
├── pages/
│   ├── index/      # 求解页面
│   ├── result/     # 结果页面（含等价替换说明）
│   ├── prices/     # 价格管理（含配置管理）
│   ├── history/    # 历史记录
│   └── about/      # 关于页面
├── utils/
│   ├── solver.js   # 核心算法 v5
│   ├── storage.js  # 本地存储
│   ├── sort.js     # 排序工具
│   └── data.js     # 默认价格数据
└── app.json
```

### 调用示例

```javascript
const { HPMSolver } = require('../../utils/solver')
const { getPrices } = require('../../utils/storage')

const prices = getPrices()
const solver = new HPMSolver(prices, prices.maxQuantities)
const result = solver.solve(7500, 0, 1.5, 1.0)

console.log(result.gold.isPerfect ? '完美解' : '近似解')
console.log('残值:', result.gold.residual)
```

---

## 测试报告

### 测试1：金币7500，p=1.5，q=1.0

```
数据优化：41物品 → 31等价组 → 17运算组
结果：近似解（残值=6金）
```

### 测试2：金币15000，p=1.5，q=1.0

```
数据优化：41物品 → 31等价组 → 17运算组
结果：完美解（残值=0）
```

### 测试3：金币5000，p=1.0，q=1.0

```
数据优化：41物品 → 31等价组 → 16运算组
结果：完美解（残值=0）
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v5 | 2026-03-25 | 等价替换还原、filterTable机制、微信小程序集成 |
| v4 | 2026-03-20 | 等价分组、约数过滤 |
| v3 | 2026-03-18 | 双系数模型、基础穷举 |

---

## 触发条件

- 哈皮马求解、HPM求解、魔法觉醒计算
- 金币求解、宝石求解、购买组合、残值计算
- HPM价格、HPM历史、HPM计算器

---

## 下载链接

**微信小程序 v13**: https://astron-claw-media-prod.oss-cn-beijing.aliyuncs.com/astron-claw-media-prod/c76c9c06e5a6429885e66501e8730ef8/hpm-miniprogram-v13.tar.gz
