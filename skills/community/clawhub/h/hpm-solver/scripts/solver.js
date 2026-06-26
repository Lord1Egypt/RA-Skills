/**
 * HPM 交易求解器 - 核心算法 v5
 * 
 * 功能：哈利波特魔法觉醒游戏交易求解器
 * - 双系数模型 (p/q)
 * - 等价分组
 * - 整除过滤
 * - 穷举求解
 * - 等价替换还原
 * 
 * 作者：龙虾AI-贾维斯
 * 更新：2026-03-25
 */

class EquivalenceGroup {
  /**
   * 等价物品组
   * @param {number} basePrice - 基础价格
   * @param {number} actualPrice - 实际价格（乘以系数后）
   * @param {string[]} items - 物品名称列表
   * @param {string} category - 类别 (foods/plants)
   * @param {Object} maxQuantities - 各物品最大可用数量
   */
  constructor(basePrice, actualPrice, items, category, maxQuantities) {
    this.basePrice = basePrice
    this.actualPrice = actualPrice
    this.items = items
    this.category = category
    this.maxQuantities = maxQuantities || {}
  }
  
  /**
   * 获取组的最大可用数量（取所有物品的最小值）
   */
  getMaxQuantity() {
    var minQty = 99
    for (var i = 0; i < this.items.length; i++) {
      var qty = this.maxQuantities[this.items[i]]
      if (qty !== undefined && qty < minQty) minQty = qty
    }
    return minQty
  }
  
  /**
   * 获取组的最大价值
   */
  get maxValue() { 
    return this.actualPrice * this.getMaxQuantity() 
  }
}

class Solution {
  /**
   * 求解结果
   * @param {Array} groups - 购买组合 [{group: EquivalenceGroup, quantity: number}]
   * @param {number} totalCost - 总花费
   * @param {number} residual - 残值
   */
  constructor(groups, totalCost, residual) {
    this.groups = groups
    this.totalCost = totalCost
    this.residual = residual
    this.isPerfect = residual === 0
  }
  
  /**
   * 获取各物品的购买数量
   * @returns {Object} {物品名称: 数量}
   */
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
  /**
   * HPM 交易求解器
   * @param {Object} basePrices - 价格数据
   * @param {Object} maxQuantities - 最大可用数量
   */
  constructor(basePrices, maxQuantities) {
    this.basePrices = basePrices
    this.maxQuantities = maxQuantities || { 
      foods: { gold: {}, diamond: {} }, 
      plants: { gold: {}, diamond: {} } 
    }
  }

  /**
   * 求解主入口
   * @param {number} targetGold - 目标金币
   * @param {number} targetDiamond - 目标宝石
   * @param {number} multiplierP - 菜品系数
   * @param {number} multiplierQ - 植物系数
   * @returns {Object} 求解结果
   */
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

  /**
   * 构建物品列表
   * @private
   */
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

  /**
   * 等价分组：将相同价格的物品合并
   * @private
   */
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
    
    // 按价格升序排列
    groups.sort(function(a, b) { return a.actualPrice - b.actualPrice })
    return groups
  }

  /**
   * 整除过滤：过滤可被低价物品替代的高价物品
   * @private
   */
  filterByDivisibility(groups, target) {
    var kept = []
    var filterTable = []
    
    for (var i = 0; i < groups.length; i++) {
      var group = groups[i]
      var canFilter = false
      
      for (var j = 0; j < kept.length; j++) {
        var lowGroup = kept[j]
        // 检查整除关系
        if (group.actualPrice % lowGroup.actualPrice === 0) {
          var ratio = group.actualPrice / lowGroup.actualPrice
          // 检查低价物品数量是否足够
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

  /**
   * 求解单一货币
   * @private
   */
  solveCurrency(target, items) {
    var groups = this.groupByPrice(items)
    var filtered = this.filterByDivisibility(groups, target)
    
    if (filtered.kept.length === 0) return null
    
    var maxQuantities = filtered.kept.map(function(g) {
      return Math.min(Math.floor(target / g.actualPrice), g.getMaxQuantity())
    })
    
    return this.exhaustiveSolve(target, filtered.kept, maxQuantities, filtered.filterTable)
  }

  /**
   * 穷举求解
   * @private
   */
  exhaustiveSolve(target, groups, maxQuantities, filterTable) {
    // 按价格降序排列
    var sortedData = groups.map(function(g, i) { 
      return { group: g, maxQty: maxQuantities[i] } 
    }).sort(function(a, b) { return b.group.actualPrice - a.group.actualPrice })
    
    var bestSolution = null
    var minPrice = Math.min.apply(null, groups.map(function(g) { return g.actualPrice }))
    
    // 递归穷举
    function iterate(index, currentCost, currentGroups) {
      if (currentCost > target) return null
      
      if (index === sortedData.length) {
        var residual = target - currentCost
        if (residual >= 0 && residual < minPrice) {
          var solution = new Solution(currentGroups.slice(), currentCost, residual)
          if (solution.isPerfect) return solution  // 完美解立即返回
          if (!bestSolution || residual < bestSolution.residual) bestSolution = solution
        }
        return null
      }
      
      var data = sortedData[index]
      var effectiveMaxQty = Math.min(
        data.maxQty, 
        Math.floor((target - currentCost) / data.group.actualPrice)
      )
      
      // 从大到小尝试
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
    
    // 等价替换还原
    if (solution && filterTable && filterTable.length > 0) {
      solution = this.tryReplaceWithHighPrice(solution, filterTable)
    }
    if (solution) solution.filterTable = filterTable
    
    return solution
  }

  /**
   * 尝试将低价物品替换回高价物品
   * @private
   */
  tryReplaceWithHighPrice(solution, filterTable) {
    var quantities = solution.getQuantities()
    // 按替换比例降序排列
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
    
    // 添加剩余的低价物品
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

// 导出
module.exports = { 
  HPMSolver: HPMSolver, 
  EquivalenceGroup: EquivalenceGroup, 
  Solution: Solution 
}
