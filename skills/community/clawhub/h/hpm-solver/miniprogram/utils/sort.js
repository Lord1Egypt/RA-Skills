/**
 * 排序工具函数
 * 排序规则：
 * 1. 分类比较物品名，例如"草", "草-紫", "草-蓝"，拆分成3个集合
 * 2. 对第一个集合(不带-字符)按照单价从大到小排序
 * 3. 遍历color_3的集合元素，找到前缀匹配的元素索引i，插入i+1位置
 * 4. 遍历color_2的元素，找到前缀匹配的元素索引i，插入i+1位置
 */

/**
 * 提取物品基础名（去掉-紫、-蓝后缀）
 */
function getBaseName(name) {
  const idx = name.indexOf('-');
  return idx > 0 ? name.substring(0, idx) : name;
}

/**
 * 判断是否是带颜色的物品（-紫、-蓝）
 */
function getColorType(name) {
  if (name.endsWith('-蓝')) return 3;  // color_3
  if (name.endsWith('-紫')) return 2;  // color_2
  return 1;  // color_1
}

/**
 * 对物品列表进行排序
 * @param {Array} items 物品列表，每个元素包含 {name, price}
 * @returns {Array} 排序后的列表
 */
function sortItems(items) {
  console.log('[Sort] sortItems 开始, 物品数=', items.length);
  
  if (!items || items.length === 0) {
    console.log('[Sort] 物品列表为空，返回空数组');
    return [];
  }
  
  // 分类：color_1(不带-), color_2(-紫), color_3(-蓝)
  const color_1 = [];  // 不带颜色后缀
  const color_2 = [];  // -紫
  const color_3 = [];  // -蓝
  
  for (const item of items) {
    const colorType = getColorType(item.name);
    if (colorType === 1) {
      color_1.push(item);
    } else if (colorType === 2) {
      color_2.push(item);
    } else {
      color_3.push(item);
    }
  }
  
  console.log('[Sort] 分类结果: color_1=', color_1.length, 'color_2=', color_2.length, 'color_3=', color_3.length);
  
  // 对 color_1 按单价从大到小排序
  color_1.sort((a, b) => b.price - a.price);
  console.log('[Sort] color_1 排序完成');
  
  // 对 color_2 按单价从大到小排序
  color_2.sort((a, b) => b.price - a.price);
  console.log('[Sort] color_2 排序完成');
  
  // 对 color_3 按单价从大到小排序
  color_3.sort((a, b) => b.price - a.price);
  console.log('[Sort] color_3 排序完成');
  
  // 初始化 showList 为 color_1
  const showList = [...color_1];
  
  // 遍历 color_3，插入到匹配元素后
  for (const item3 of color_3) {
    const baseName = getBaseName(item3.name);
    let inserted = false;
    
    for (let i = 0; i < showList.length; i++) {
      const showItem = showList[i];
      const showBaseName = getBaseName(showItem.name);
      
      if (showBaseName === baseName) {
        // 找到匹配，插入到 i+1 位置
        showList.splice(i + 1, 0, item3);
        inserted = true;
        console.log('[Sort] color_3 插入:', item3.name, '-> 位置', i + 1);
        break;
      }
    }
    
    if (!inserted) {
      // 没有匹配，插入到尾部
      showList.push(item3);
      console.log('[Sort] color_3 插入尾部:', item3.name);
    }
  }
  
  // 遍历 color_2，插入到匹配元素后
  for (const item2 of color_2) {
    const baseName = getBaseName(item2.name);
    let inserted = false;
    
    for (let i = 0; i < showList.length; i++) {
      const showItem = showList[i];
      const showBaseName = getBaseName(showItem.name);
      
      if (showBaseName === baseName) {
        // 找到匹配，插入到 i+1 位置
        showList.splice(i + 1, 0, item2);
        inserted = true;
        console.log('[Sort] color_2 插入:', item2.name, '-> 位置', i + 1);
        break;
      }
    }
    
    if (!inserted) {
      // 没有匹配，插入到尾部
      showList.push(item2);
      console.log('[Sort] color_2 插入尾部:', item2.name);
    }
  }
  
  console.log('[Sort] sortItems 完成, 结果数=', showList.length);
  return showList;
}

/**
 * 对价格数据进行排序
 * @param {Object} priceData 价格数据 {name: price, ...}
 * @returns {Array} 排序后的列表 [{name, price}, ...]
 */
function sortPriceData(priceData) {
  console.log('[Sort] sortPriceData 开始');
  
  const items = [];
  for (const name in priceData) {
    items.push({
      name,
      price: priceData[name]
    });
  }
  
  return sortItems(items);
}

module.exports = {
  sortItems,
  sortPriceData,
  getBaseName,
  getColorType
};
