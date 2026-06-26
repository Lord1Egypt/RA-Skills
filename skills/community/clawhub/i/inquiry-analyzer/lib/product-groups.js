/**
 * 产品分组动态获取模块
 * 功能：从阿里巴巴产品管理页面动态获取产品分组列表，并缓存到本地
 *
 * 用法：
 *   const productGroups = await fetchProductGroups(page, context);
 *   const category = mapGroupToCategory(groupName, productGroups);
 */

const fs = require('fs');

// 产品分组缓存文件
const PRODUCT_GROUPS_CACHE_PATH = './product-groups-cache.json';

// 用户自定义映射文件
const MAPPING_FILE = './product-mapping.json';

// 默认分组映射（用于没有匹配到时的回退）
const DEFAULT_GROUP_MAPPING = {
  'stainless steel kitchen cabinet': '厨房橱柜',
  'kitchen cabinet': '厨房橱柜',
  'outdoor kitchen shed': '箱体户外厨房',
  'custom stainless steel outdoor kitchen': '定制户外厨房',
  'kamado grill': 'Kamado Grill',
  'modular stainless steel outdoor kitchen': '标品户外厨房',
  'stainless steel gun cabinet': '枪柜',
  'stainless steel sideboards cabinet': '餐边柜',
  'stainless steel tool cabinet': '工具柜',
  'outdoor kitchen': '户外厨房',
  'tool cabinet': '工具柜',
  'bathroom cabinet': '浴室柜',
  'sideboard': '餐边柜',
  'wardrobe': '衣柜',
  'tv cabinet': '电视柜',
  'wine cabinet': '酒柜',
  'shoe cabinet': '入户柜',
  'bookcase': '书柜',
  'gun cabinet': '枪柜',
};

// ========== 缓存管理 ==========

function loadGroupCache() {
  try {
    if (fs.existsSync(PRODUCT_GROUPS_CACHE_PATH)) {
      const data = fs.readFileSync(PRODUCT_GROUPS_CACHE_PATH, 'utf8');
      const cache = JSON.parse(data);
      // 检查缓存是否过期（7天）
      const cacheDate = new Date(cache.timestamp || 0);
      const now = new Date();
      const daysDiff = (now - cacheDate) / (1000 * 60 * 60 * 24);
      if (daysDiff <= 7) {
        console.log(`  [分组缓存] 使用缓存 (${daysDiff.toFixed(1)}天前)`);
        return cache;
      } else {
        console.log(`  [分组缓存] 缓存已过期 (${daysDiff.toFixed(1)}天)，重新获取`);
      }
    }
  } catch (e) {
    console.log(`  [分组缓存] 加载失败: ${e.message}`);
  }
  return null;
}

function saveGroupCache(groups) {
  try {
    const cache = {
      timestamp: new Date().toISOString(),
      groups: groups,
      version: '1.0'
    };
    fs.writeFileSync(PRODUCT_GROUPS_CACHE_PATH, JSON.stringify(cache, null, 2), 'utf8');
    console.log(`  [分组缓存] 已保存 ${groups.length} 个分组到 ${PRODUCT_GROUPS_CACHE_PATH}`);
  } catch (e) {
    console.log(`  [分组缓存] 保存失败: ${e.message}`);
  }
}

// ========== 动态获取分组 ==========

/**
 * 从产品管理页面动态获取所有产品分组
 * @param {Page} page - Playwright 页面对象
 * @param {Context} context - 浏览器上下文
 * @returns {Promise<Array>} 分组名称数组
 */
async function fetchProductGroups(context) {
  const PRODUCT_GROUP_PAGE = 'https://i.alibaba.com/prod/product_manage#/product/online';

  // 先尝试加载缓存
  const cached = loadGroupCache();
  if (cached && cached.groups && cached.groups.length > 0) {
    return cached.groups;
  }

  console.log(`  [分组获取] 正在从产品管理页面获取分组列表...`);

  let groupPage;
  try {
    groupPage = await context.newPage();
    await groupPage.goto(PRODUCT_GROUP_PAGE, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await sleep(3000);

    // 滚动加载确保所有分组可见
    await groupPage.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await sleep(2000);

    // 提取所有分组名称
    const groups = await groupPage.evaluate(() => {
      const results = new Set();

      // 方法1：从分组侧边栏/下拉框提取
      const groupSelectors = [
        '.group-name',
        '.product-group-name',
        '[class*="group-name"]',
        '[data-field="groupName"]',
        '.next-tree-node-title',
      ];

      groupSelectors.forEach((selector) => {
        const els = document.querySelectorAll(selector);
        els.forEach(el => {
          const text = el.textContent?.trim() || el.getAttribute('title')?.trim() || '';
          if (text && text.length > 2 && text.length < 100) {
            results.add(text);
          }
        });
      });

      // 方法2：从 aria-label 属性提取
      const allEls = document.querySelectorAll('[aria-label]');
      allEls.forEach(el => {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('group') || label.includes('分组')) {
          const text = el.textContent?.trim();
          if (text && text.length > 2 && text.length < 100) {
            results.add(text);
          }
        }
      });

      // 方法3：从 data-* 属性提取
      const dataEls = document.querySelectorAll('[data-group-name], [data-group], [data-groupname]');
      dataEls.forEach(el => {
        const group = el.getAttribute('data-group-name') ||
                      el.getAttribute('data-group') ||
                      el.getAttribute('data-groupname');
        if (group && group.length > 2 && group.length < 100) {
          results.add(group);
        }
      });

      // 方法4：从页面文本中提取"分组：xxx"模式
      const text = document.body.innerText;
      const groupPatterns = [
        /分组[:：]\s*([^\n，。,]{2,100})/g,
        /Group[:：]\s*([^\n，。,]{2,100})/gi,
        /Category[:：]\s*([^\n，。,]{2,100})/gi,
      ];
      for (const pattern of groupPatterns) {
        let match;
        while ((match = pattern.exec(text)) !== null) {
          if (match[1]) {
            results.add(match[1].trim());
          }
        }
      }

      return Array.from(results).sort();
    });

    if (groups.length === 0) {
      console.log(`  [分组获取] 未找到分组信息，使用默认映射`);
      return Object.keys(DEFAULT_GROUP_MAPPING);
    }

    console.log(`  [分组获取] 成功获取 ${groups.length} 个分组`);
    groups.forEach(g => console.log(`    - ${g}`));

    // 保存到缓存
    saveGroupCache(groups);

    return groups;

  } catch (e) {
    console.log(`  [分组获取] 获取失败: ${e.message}，使用默认映射`);
    return Object.keys(DEFAULT_GROUP_MAPPING);
  } finally {
    if (groupPage) {
      await groupPage.close().catch(() => {});
    }
  }
}

// ========== 分组映射 ==========

/**
 * 加载用户自定义映射
 */
function loadUserMapping() {
  try {
    if (fs.existsSync(MAPPING_FILE)) {
      const data = fs.readFileSync(MAPPING_FILE, 'utf8');
      const config = JSON.parse(data);
      return config.mapping || config;
    }
  } catch (e) {
    console.log(`  [映射] 加载用户配置失败: ${e.message}`);
  }
  return {};
}

/**
 * 将分组名称映射到产品类型
 * @param {string} groupName - 分组名称
 * @param {Object} userMapping - 用户自定义映射（可选）
 * @returns {string|null} 产品类型，未匹配返回 null
 */
function mapGroupToCategory(groupName, userMapping = null) {
  if (!groupName) return null;

  const lower = groupName.toLowerCase();

  // 1. 用户自定义映射（最高优先级）
  const mapping = userMapping || loadUserMapping();
  if (mapping[groupName]) {
    return mapping[groupName];
  }
  // 尝试大小写不敏感匹配
  for (const [key, value] of Object.entries(mapping)) {
    if (key.toLowerCase() === lower) {
      return value;
    }
  }

  // 2. 默认映射匹配
  for (const [key, value] of Object.entries(DEFAULT_GROUP_MAPPING)) {
    if (lower.includes(key)) {
      return value;
    }
  }

  // 3. 关键词推导
  return deriveCategoryFromGroupName(groupName);
}

/**
 * 从分组名推导产品类型
 * @param {string} groupName - 分组名称
 * @returns {string} 推导的产品类型
 */
function deriveCategoryFromGroupName(groupName) {
  if (!groupName) return '其他';

  const lower = groupName.toLowerCase();

  // 厨房橱柜
  if (/kitchen.*cabinet|stainless.*steel.*kitchen/i.test(lower)) {
    return '厨房橱柜';
  }
  if (/kitchen/i.test(lower)) {
    return '厨房橱柜';
  }

  // 户外厨房
  if (/outdoor.*kitchen.*shed|outdoor.*shed/i.test(lower)) {
    return '箱体户外厨房';
  }
  if (/custom.*outdoor.*kitchen/i.test(lower)) {
    return '定制户外厨房';
  }
  if (/modular.*outdoor.*kitchen|standard.*outdoor.*kitchen/i.test(lower)) {
    return '标品户外厨房';
  }
  if (/outdoor.*kitchen/i.test(lower)) {
    return '户外厨房';
  }

  // Kamado Grill
  if (/kamado.*grill|kamado/i.test(lower)) {
    return 'Kamado Grill';
  }

  // 工具柜
  if (/tool.*cabinet|tool.*storage/i.test(lower)) {
    return '工具柜';
  }

  // 枪柜
  if (/gun.*cabinet|gun.*storage/i.test(lower)) {
    return '枪柜';
  }

  // 餐边柜
  if (/sideboard/i.test(lower)) {
    return '餐边柜';
  }

  // 浴室柜
  if (/bathroom.*cabinet|bathroom.*vanity/i.test(lower)) {
    return '浴室柜';
  }

  // 衣柜
  if (/wardrobe|closet/i.test(lower)) {
    return '衣柜';
  }

  // 电视柜
  if (/tv.*cabinet|tv.*stand/i.test(lower)) {
    return '电视柜';
  }

  // 酒柜
  if (/wine.*cabinet|wine.*storage/i.test(lower)) {
    return '酒柜';
  }

  // 鞋柜/入户柜
  if (/shoe.*cabinet|shoe.*rack|entryway/i.test(lower)) {
    return '入户柜';
  }

  // 书柜
  if (/bookcase|bookshelf/i.test(lower)) {
    return '书柜';
  }

  // 兜底返回分组名
  return groupName;
}

// ========== 搜索分组 ==========

/**
 * 在产品管理页面搜索标题对应的分组
 * @param {string} title - 产品标题
 * @param {Context} context - 浏览器上下文
 * @returns {Promise<{group: string, category: string}|null>}
 */
async function searchGroupByTitle(title, context) {
  if (!title) return null;

  const PRODUCT_GROUP_PAGE = 'https://i.alibaba.com/prod/product_manage#/product/online';
  let searchPage;

  try {
    searchPage = await context.newPage();
    await searchPage.goto(PRODUCT_GROUP_PAGE, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await sleep(2000);

    // 输入搜索词
    console.log(`  [分组搜索] 搜索标题: ${title}`);
    const searchInput = searchPage.locator('input[placeholder*="产品名称"], input[placeholder*="Product"]').first();
    await searchInput.waitFor({ timeout: 10000 });
    await searchInput.fill(title);
    await sleep(500);

    // 点击搜索按钮
    const searchBtn = searchPage.locator('button:has-text("搜索"), .search-button button, button.next-btn-secondary').first();
    if (await searchBtn.isVisible()) {
      await searchBtn.click();
      await sleep(4000);
    }

    // 提取分组信息
    const groupInfo = await searchPage.evaluate(() => {
      // 方法1：从搜索结果的分组标签提取
      const groupEls = document.querySelectorAll('.group-name, .product-group-name, [class*="group-name"]');
      for (const el of groupEls) {
        const text = el.textContent?.trim() || el.getAttribute('title')?.trim() || '';
        if (text && text.length > 2 && text.length < 100) {
          return text;
        }
      }

      // 方法2：从产品卡片的数据属性提取
      const cardEls = document.querySelectorAll('[data-group-name], [data-group]');
      for (const el of cardEls) {
        const group = el.getAttribute('data-group-name') || el.getAttribute('data-group');
        if (group && group.length > 2 && group.length < 100) {
          return group;
        }
      }

      return null;
    });

    if (groupInfo) {
      console.log(`  [分组搜索] 找到分组: ${groupInfo}`);
      const category = mapGroupToCategory(groupInfo);
      console.log(`  [分组搜索] 映射产品类型: ${category}`);
      return { group: groupInfo, category: category };
    }

    return null;

  } catch (e) {
    console.log(`  [分组搜索] 搜索失败: ${e.message}`);
    return null;
  } finally {
    if (searchPage) {
      await searchPage.close().catch(() => {});
    }
  }
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ========== 导出 ==========

module.exports = {
  fetchProductGroups,
  mapGroupToCategory,
  deriveCategoryFromGroupName,
  searchGroupByTitle,
  loadUserMapping,
  DEFAULT_GROUP_MAPPING,
  PRODUCT_GROUPS_CACHE_PATH,
  MAPPING_FILE,
};
