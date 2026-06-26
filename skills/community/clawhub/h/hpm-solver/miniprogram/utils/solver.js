/**
 * HPM 求解器核心算法 v5
 * 优化特性：
 * 1. 约数过滤优化：维护 filter_table，只保留 miniPriceCell 进行穷举
 * 2. 替换还原：穷举成功后，用高价物品替换等值的低价物品组合
 */

class EquivalenceGroup {
  constructor(basePrice, actualPrice, items, category, maxqty = 99) {
    this.basePrice = basePrice;
    this.actualPrice = actualPrice;
    this.items = items;
    this.category = category;
    this.maxqty = maxqty;
  }

  get maxValue() {
    return this.actualPrice * this.maxqty;
  }
}

class FilterRelation {
  constructor(highPriceGroup, lowPriceGroup, ratio) {
    this.highPriceGroup = highPriceGroup;
    this.lowPriceGroup = lowPriceGroup;
    this.ratio = ratio;
  }
}

class Solution {
  constructor(groups, totalCost, residual, isPerfect) {
    this.groups = groups;
    this.totalCost = totalCost;
    this.residual = residual;
    this.isPerfect = isPerfect;
  }

  getQuantities() {
    const result = {};
    for (const [group, qty] of this.groups) {
      if (qty > 0) {
        for (const item of group.items) {
          result[item] = (result[item] || 0) + qty;
        }
      }
    }
    return result;
  }
}

/**
 * 按价格分组，合并等价物品
 */
function groupByPrice(items) {
  console.log('[Solver] groupByPrice 输入:', items.length, '个物品');
  
  const priceGroups = {};
  
  for (const item of items) {
    const key = `${item.price}_${item.category}`;
    if (!priceGroups[key]) {
      priceGroups[key] = [];
    }
    priceGroups[key].push(item);
  }
  
  const groups = [];
  for (const key in priceGroups) {
    const itemList = priceGroups[key];
    const basePrice = Math.min(...itemList.map(i => i.basePrice));
    const price = itemList[0].price;
    const category = itemList[0].category;
    const maxqty = Math.min(...itemList.map(i => i.maxqty || 99));
    
    const group = new EquivalenceGroup(
      basePrice,
      price,
      itemList.map(i => i.name),
      category,
      maxqty
    );
    groups.push(group);
    console.log('[Solver] 创建等价组:', group.items.join('|'), 'price=', group.actualPrice, 'maxqty=', group.maxqty);
  }
  
  const result = groups.sort((a, b) => a.actualPrice - b.actualPrice);
  console.log('[Solver] groupByPrice 输出:', result.length, '个等价组');
  return result;
}

/**
 * 约数过滤：维护 filter_table 记录约数关系
 * 返回：[miniPriceCell, filterTable]
 */
function filterByDivisibility(groups, target) {
  console.log('[Solver] filterByDivisibility 输入:', groups.length, '个等价组, 目标=', target);
  
  const miniPriceCell = [];
  const filterTable = [];
  
  for (const group of groups) {
    let canFilter = false;
    
    for (const lowGroup of miniPriceCell) {
      if (group.actualPrice % lowGroup.actualPrice === 0) {
        const ratio = group.actualPrice / lowGroup.actualPrice;
        
        // 条件1：低价物品能否买够数量来替代高价物品？
        const canBuyEnough = lowGroup.maxqty >= ratio;
        
        // 条件2：低价物品的总价值是否足够达到目标？
        const canReachTarget = lowGroup.maxValue >= target;
        
        if (canBuyEnough && canReachTarget) {
          const relation = new FilterRelation(group, lowGroup, ratio);
          filterTable.push(relation);
          canFilter = true;
          console.log('[Solver] 过滤:', group.actualPrice, '=', lowGroup.actualPrice, 'x', ratio);
          console.log('         低价物品 maxqty=', lowGroup.maxqty, '>= ratio=', ratio, '✓');
          console.log('         低价物品 max_value=', lowGroup.maxValue, '>= target=', target, '✓');
          break;
        } else {
          console.log('[Solver] 检查:', group.actualPrice, '是', lowGroup.actualPrice, '的', ratio, '倍');
          if (!canBuyEnough) {
            console.log('         低价物品 maxqty=', lowGroup.maxqty, '< ratio=', ratio, '✗ 无法买够数量');
          }
          if (!canReachTarget) {
            console.log('         低价物品 max_value=', lowGroup.maxValue, '< target=', target, '✗ 无法达到目标');
          }
        }
      }
    }
    
    if (!canFilter) {
      miniPriceCell.push(group);
      console.log('[Solver] 保留到 miniPriceCell:', group.items[0], 'price=', group.actualPrice);
    }
  }
  
  console.log('[Solver] filterByDivisibility 输出:');
  console.log('  - miniPriceCell:', miniPriceCell.length, '个运算组');
  console.log('  - filterTable:', filterTable.length, '条过滤关系');
  
  return [miniPriceCell, filterTable];
}

/**
 * 尝试用高价物品替换低价物品组合
 */
function tryReplaceWithHighPrice(solution, filterTable, target) {
  if (!filterTable || filterTable.length === 0) {
    console.log('[Solver] 没有过滤关系，跳过替换');
    return solution;
  }
  
  console.log('[Solver] 尝试用高价物品替换低价物品组合...');
  
  const quantities = solution.getQuantities();
  console.log('[Solver] 当前解:', JSON.stringify(quantities));
  
  // 按 ratio 从大到小排序
  const sortedFilterTable = [...filterTable].sort((a, b) => b.ratio - a.ratio);
  
  const remainingQuantities = { ...quantities };
  const newGroups = [];
  
  for (const relation of sortedFilterTable) {
    const lowPrice = relation.lowPriceGroup.actualPrice;
    const highPrice = relation.highPriceGroup.actualPrice;
    const ratio = relation.ratio;
    
    const lowItemName = relation.lowPriceGroup.items[0];
    if (!(lowItemName in remainingQuantities)) {
      continue;
    }
    
    const lowQty = remainingQuantities[lowItemName];
    const maxReplace = Math.floor(lowQty / ratio);
    
    if (maxReplace > 0) {
      const highMaxqty = relation.highPriceGroup.maxqty;
      const actualReplace = Math.min(maxReplace, highMaxqty);
      
      if (actualReplace > 0) {
        newGroups.push([relation.highPriceGroup, actualReplace]);
        remainingQuantities[lowItemName] -= actualReplace * ratio;
        console.log('[Solver] 替换:', actualReplace, '个', relation.highPriceGroup.items[0], 
          '(', highPrice, ') <-> ', actualReplace * ratio, '个', lowItemName, '(', lowPrice, ')');
      }
    }
  }
  
  if (newGroups.length === 0) {
    console.log('[Solver] 没有可替换的组合，返回原解');
    return solution;
  }
  
  // 添加剩余的低价物品
  for (const [group, qty] of solution.groups) {
    if (qty > 0) {
      const itemName = group.items[0];
      const remaining = remainingQuantities[itemName] || 0;
      if (remaining > 0) {
        newGroups.push([group, remaining]);
      }
    }
  }
  
  const newSolution = new Solution(newGroups, solution.totalCost, solution.residual, solution.isPerfect);
  console.log('[Solver] 替换后的解:', JSON.stringify(newSolution.getQuantities()));
  
  return newSolution;
}

/**
 * 穷举求解
 */
function exhaustiveSolve(target, miniPriceCell, filterTable) {
  console.log('[Solver] exhaustiveSolve 开始, 目标=', target);
  
  const minPrice = Math.min(...miniPriceCell.map(g => g.actualPrice));
  console.log('[Solver] 最小价格:', minPrice);
  
  const maxQuantities = miniPriceCell.map(g => Math.min(Math.floor(target / g.actualPrice), g.maxqty));
  console.log('[Solver] 各组最大数量:', maxQuantities);
  
  // 计算组合数
  let totalCombos = 1;
  for (const mq of maxQuantities) {
    totalCombos *= (mq + 1);
  }
  console.log('[Solver] 总组合数:', totalCombos);
  
  if (totalCombos > 10000000) {
    console.log('[Solver] 组合数过多，返回null');
    return null;
  }
  
  let bestSolution = null;
  let comboCount = 0;
  
  // 递归穷举
  function recurse(idx, currentCost, currentGroups) {
    if (idx === miniPriceCell.length) {
      comboCount++;
      const y = target - currentCost;
      
      if (y >= 0 && y < minPrice) {
        const solution = new Solution([...currentGroups], currentCost, y, y === 0);
        
        if (solution.isPerfect) {
          console.log('[Solver] 找到完美解! cost=', currentCost, 'residual=', y);
          return solution;
        }
        
        if (!bestSolution || y < bestSolution.residual) {
          bestSolution = solution;
          console.log('[Solver] 更新最佳解: residual=', y);
        }
      }
      return null;
    }
    
    const group = miniPriceCell[idx];
    const maxN = maxQuantities[idx];
    
    for (let n = maxN; n >= 0; n--) {
      const newCost = currentCost + n * group.actualPrice;
      if (newCost > target + minPrice) continue;
      
      if (n > 0) {
        currentGroups.push([group, n]);
      }
      
      const result = recurse(idx + 1, newCost, currentGroups);
      if (result && result.isPerfect) {
        return result;
      }
      
      if (n > 0) {
        currentGroups.pop();
      }
    }
    
    return null;
  }
  
  const perfectSolution = recurse(0, 0, []);
  
  console.log('[Solver] 穷举完成，共检查', comboCount, '个组合');
  
  if (perfectSolution) {
    return tryReplaceWithHighPrice(perfectSolution, filterTable, target);
  }
  
  if (bestSolution) {
    console.log('[Solver] 最佳解: cost=', bestSolution.totalCost, 'residual=', bestSolution.residual);
    return tryReplaceWithHighPrice(bestSolution, filterTable, target);
  }
  
  console.log('[Solver] 未找到任何有效解');
  return null;
}

/**
 * 主求解入口
 */
function solve(target, items) {
  console.log('[Solver] solve 开始, 目标=', target, '物品数=', items.length);
  
  if (!items || items.length === 0) {
    console.log('[Solver] 物品列表为空，返回null');
    return null;
  }
  
  const groups = groupByPrice(items);
  const [miniPriceCell, filterTable] = filterByDivisibility(groups, target);
  
  if (miniPriceCell.length === 0) {
    console.log('[Solver] 过滤后没有可用的运算组');
    return null;
  }
  
  console.log('[Solver] 最终参与穷举的等价组:');
  for (const g of miniPriceCell) {
    console.log('  -', g.items.join('|'), '=', g.actualPrice, 'maxqty=', g.maxqty);
  }
  
  if (filterTable.length > 0) {
    console.log('[Solver] 过滤关系表:');
    for (const r of filterTable) {
      console.log('  -', r.highPriceGroup.actualPrice, '=', r.lowPriceGroup.actualPrice, 'x', r.ratio);
    }
  }
  
  const solution = exhaustiveSolve(target, miniPriceCell, filterTable);
  
  console.log('[Solver] solve 完成, 结果=', solution ? '找到解' : '无解');
  return solution;
}

/**
 * 构建物品列表
 */
function buildItems(basePrices, category, currency, multiplier = 1.0, maxqtyMap = {}) {
  console.log('[Solver] buildItems 开始, category=', category, 'currency=', currency, 'multiplier=', multiplier);
  
  const items = [];
  const priceData = basePrices[category]?.[currency] || {};
  
  for (const name in priceData) {
    const basePrice = priceData[name];
    const actualPrice = Math.round(basePrice * multiplier);
    const maxqty = maxqtyMap[name] || 99;
    
    items.push({
      name,
      price: actualPrice,
      basePrice,
      currency,
      category,
      maxqty
    });
  }
  
  console.log('[Solver] buildItems 完成, 物品数=', items.length);
  return items;
}

module.exports = {
  solve,
  buildItems,
  EquivalenceGroup,
  FilterRelation,
  Solution
};
