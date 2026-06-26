/**
 * 通用询盘分析脚本
 * 用法：node inquiry-analyzer.js <目标询盘号> [开始时间] [结束时间]
 * 示例：node inquiry-analyzer.js 13789026663
 *       node inquiry-analyzer.js 13789026663 "2026-03-16T15:00:00" "2026-03-18T15:00:00"
 *
 * 时间窗口：默认 3/16 15:00 ~ 3/18 15:00，可通过命令行参数自定义
 * 完成后输出 Markdown 表格报告
 *
 * OpenClaw 浏览器自动启动：
 * - 脚本会自动检测 OpenClaw 浏览器是否运行
 * - 如果未运行，会自动启动浏览器
 * - 启动路径：E:\Nvm\nodejs\node_global\node_modules\openclaw\openclaw.mjs
 */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

// 动态产品分组模块
const {
  fetchProductGroups,
  mapGroupToCategory,
  searchGroupByTitle,
  loadUserMapping,
  MAPPING_FILE,
} = require('./product-groups');

// 产品分组配置向导
const {
  autoConfigureProductMapping,
} = require('./product-mapping');

// ============ 标题分类缓存 ============
const TITLE_CACHE_PATH = './title-cache.json';
function loadTitleCache() {
  try { return JSON.parse(fs.readFileSync(TITLE_CACHE_PATH, 'utf8')); } catch { return { direct: {}, forced: {} }; }
}
function saveTitleCache(cache) {
  fs.writeFileSync(TITLE_CACHE_PATH, JSON.stringify(cache, null, 2), 'utf8');
}
function clearTitleCache() {
  fs.writeFileSync(TITLE_CACHE_PATH, JSON.stringify({ direct: {}, forced: {} }, null, 2), 'utf8');
  console.log('✅ 标题缓存已清除');
}
// 每次运行清除缓存
clearTitleCache();
const titleCache = loadTitleCache();
let titleCacheDirty = false;

// ============ 聊天产品缓存 ============
// 存储从聊天内容发现的产品描述 → 类型映射，用户可手动编辑补充
const CHAT_PRODUCTS_PATH = './chat-products.json';
function loadChatProducts() {
  try { return JSON.parse(fs.readFileSync(CHAT_PRODUCTS_PATH, 'utf8')); } catch { return {}; }
}
function saveChatProducts(map) {
  fs.writeFileSync(CHAT_PRODUCTS_PATH, JSON.stringify(map, null, 2), 'utf8');
}
const chatProductsMap = loadChatProducts();
let chatProductsDirty = false;

// ============ 配置区 ============
const RELAY_TOKEN = '856baea1afbe169e5eec0f6ecb5b90c77ddeb06b2abe1154';
const DEFAULT_TIME_WINDOW_START = '2026-03-16T15:00:00';
const DEFAULT_TIME_WINDOW_END = '2026-03-18T15:00:00';

// 支持命令行自定义时间窗口：node inquiry-analyzer.js <询盘号> [开始时间] [结束时间]
const TIME_WINDOW_START = process.argv[3] || DEFAULT_TIME_WINDOW_START;
const TIME_WINDOW_END = process.argv[4] || DEFAULT_TIME_WINDOW_END;
const OPENCLAW_PATH = 'E:\\Nvm\\nodejs\\node_global\\node_modules\\openclaw\\openclaw.mjs';
const OPENCLAW_CDP_URL = 'http://127.0.0.1:18800';

// ============ 通用链接规则 ============
// 这些链接需要登录才能使用
const ALIBABA_LINKS = {
  // 询盘单号页面 - 显示所有反馈/询盘
  inquiryPage: 'https://message.alibaba.com/message/default.htm#feedback/all?order={"order":"desc","orderBy":"gmt_create"}&pageSize=100',

  // 产品分组页面 - 查找链接分组
  productGroupPage: 'https://i.alibaba.com/prod/product_manage#/product/online',
};

// ============ 国家管理系统 ============

// 基础国家列表
const BASE_COUNTRIES = ['美国','英国','德国','法国','意大利','西班牙','澳大利亚','加拿大','日本','韩国','巴西','墨西哥','荷兰','比利时','瑞典','挪威','丹麦','芬兰','波兰','捷克','匈牙利','罗马尼亚','保加利亚','克罗地亚','塞尔维亚','希腊','葡萄牙','瑞士','奥地利','以色列','土耳其','沙特阿拉伯','阿联酋','南非','埃及','尼日利亚','肯尼亚','坦桑尼亚','刚果','印度','巴基斯坦','孟加拉国','泰国','越南','印度尼西亚','马来西亚','菲律宾','新加坡','新西兰','阿根廷','智利','哥伦比亚','秘鲁','委内瑞拉','厄瓜多尔','哥斯达黎加'];

// 动态国家列表文件
const COUNTRIES_FILE = 'countries-list.json';

// 加载国家列表
function loadCountries() {
  let allCountries = [...BASE_COUNTRIES];
  try {
    if (fs.existsSync(COUNTRIES_FILE)) {
      const data = fs.readFileSync(COUNTRIES_FILE, 'utf-8');
      const customCountries = JSON.parse(data);
      if (Array.isArray(customCountries)) {
        allCountries = [...new Set([...BASE_COUNTRIES, ...customCountries])];
      }
    }
  } catch (e) {
    console.log(`  [提示] 无法加载国家列表: ${e.message}`);
  }
  return allCountries;
}

// 保存新国家
function saveNewCountry(country) {
  if (!country || country.length === 0) return;

  try {
    let customCountries = [];
    if (fs.existsSync(COUNTRIES_FILE)) {
      const data = fs.readFileSync(COUNTRIES_FILE, 'utf-8');
      customCountries = JSON.parse(data);
    }

    // 检查是否已存在（包括基础列表）
    const allCountries = [...BASE_COUNTRIES, ...customCountries];
    if (!allCountries.includes(country)) {
      customCountries.push(country);
      fs.writeFileSync(COUNTRIES_FILE, JSON.stringify(customCountries, null, 2));
      console.log(`  [新国家] 已添加: ${country}`);
    }
  } catch (e) {
    console.log(`  [警告] 无法���存国家: ${e.message}`);
  }
}

// ============ 产品分类规则（关键词匹配） ============
// 注意：更具体的规则应该放在前面，避免被通用规则覆盖
// 动态分组功能已移至 product-groups.js 模块
const PRODUCT_KEYWORDS = [
  // 户外厨房系列（箱体/shed/pod优先，因为更具体；定制次之）
  { type: '箱体户外厨房', keywords: ['outdoor kitchen shed','outdoor kitchen shed set','outdoor kitchen with shed','outdoor kitchen with closable shed','outdoor kitchen with electric door shed','outdoor kitchen with shelter','outdoor kitchen pod','outdoor bbq kitchen pod','outdoor kitchen bbq pod','Outdoor-Küchen-BBQ-Pod','Outdoor-Küchen-Terrassen-Schuppen','Outdoor-Küchen-Pod','outdoor kitchen schuppen'] },
  { type: '凉亭', keywords: ['Outdoor Kitchen with Aluminum Pergolas','Outdoor Kitchen Cabinet with Aluminum Pergolas','Outdoor Kitchen with Electric Louvered Pavilion','Outdoor Kitchen with Aluminium Gazebo','Aluminum Pergola Outdoor Kitchen','Louvered Roof Outdoor Kitchen'] },
  // 厨房系列
  { type: '电烤箱', keywords: ['Built-in Oven','Electric Oven','Combi Steam Oven'] },

  // 其他柜类
  { type: '工具柜', keywords: ['Tool Cabinet','Rolling Tool Cabinet','heavy duty Tools Cabinet','Rolling Tool Storage Cabinet','Tool chest','Workbench Cabinet','Tool Trolley','Tool Cart','Stainless Steel Tool Cabinet','Armario de herramientas','Armario de ferramentas','Szafka narzedziowa'] },
  { type: '浴室柜', keywords: ['bathroom cabinet','bathroom vanity cabinet','bathroom sink cabinet','bathroom mirror cabinet','bathroom cabinet with sink','vanity bathroom cabinet','bathroom cabinets and vanities','bathroom storage cabinet','shower cabinet bathroom','modern bathroom cabinet','aluminium bathroom cabinets','vanity cabinet bathroom'] },
  { type: '酒柜', keywords: ['Wine Cabinet','wine bar cabinet','wine display cabinet','wine rack cabinet','wine storage cabinet','glass wine cabinet','wine glass cabinet','luxury wine cabinet','Built-in stainless steel wine cabinet'] },
  { type: '衣柜', keywords: ['wardrobe','wardrobe closet','wardrobe cabinet','bedroom wardrobe','Armoire','Garderobe','closet wardrobe','bedroom closet','walk in closet','closet cabinets','Bedroom Cabinet','clothes closet'] },
  { type: '电视柜', keywords: ['TV cabinet','TV Stand','tv stand modern','fireplace tv stand','tv stand with fireplace','modern tv stand','tv stand furniture','tv stand cabinet','motorized tv stand','mobile tv stand','floating tv stand wall mounted'] },
  { type: '阳台柜', keywords: ['Balcony Storage Bench','Balcony Storage Unit','Balcony Storage Cabinet','Balcony Appliance Cabinet','Modular Balcony Storage','Terrace Storage Unit'] },
  { type: '入户柜', keywords: ['Shoe Rack','Shoe Cabinet','shoe rack cabinet','shoe storage cabinet','shoe organizer cabinet','entryway cabinet','Entryway Storage Cabinet','entryway shoe cabinet'] },
  // 餐边柜改为强制搜索分类
  // { type: '餐边柜', keywords: ['Sideboard','sideboard cabinet','stainless steel sideboard','dining sideboard','sideboard furniture','buffet sideboard','sideboard storage'] },
  { type: '书柜', keywords: ['Bookshelf','Bookcase','Book Rack','Book Cabinet','bookshelf cabinet','bookcase with glass door','library bookshelf','File Cabinet','Librero','Libreria','Scaffale per libri'] },
  { type: '抽屉柜', keywords: ['Chest Of Drawer','Dressers','Drawers Chest','drawer Storage Cabinet','Furniture Chest of drawers','Storage Chest','Dressing Table'] },
  // 注意：厨房橱柜、餐边柜 改为强制搜索分类，不使用关键词匹配

  // 其他
  { type: 'Kamado Grill', keywords: ['Kamado Grill','Kamado grill','kamado grill'] },
];

// 注意：GROUP_MAP 已移除，改用 product-groups.js 模块的动态分组功能

// L+图片src → 等级映射
const LEVEL_MAP = {
  'O1CN01NQDNGN1GXxg1QhmCW_!!6000000000633-2-tps-136-80.png': 'L2',
  'O1CN01QPXkVq1xUmP6u0guh_!!6000000006447-2-tps-136-80.png': 'L1',
  'O1CN016s9YtC1jJsEn1Insi_!!6000000004528-2-tps-144-82.png': 'L3',
  'O1CN01Y2kXyK27mJc8CmtgL_!!6000000007839-2-tps-144-82.png': 'L4',
  'O1CN01irT4ui1PgVUnXIuXT_!!6000000001870-2-tps-172-80.png': 'L1+',
};

// ============ 工具函数 ============
async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// 清理旧文件，只保留最近 N 个
function cleanOldFiles(dir, keepCount) {
  if (!fs.existsSync(dir)) return;

  const files = fs.readdirSync(dir)
    .filter(f => {
      const filePath = path.join(dir, f);
      return fs.statSync(filePath).isFile();
    })
    .map(f => ({
      name: f,
      path: path.join(dir, f),
      mtime: fs.statSync(path.join(dir, f)).mtime.getTime()
    }))
    .sort((a, b) => b.mtime - a.mtime); // 按修改时间降序

  if (files.length <= keepCount) return;

  const toDelete = files.slice(keepCount);
  toDelete.forEach(f => {
    try {
      fs.unlinkSync(f.path);
      console.log(`  [清理] 删除旧文件: ${f.name}`);
    } catch (e) {
      console.log(`  [清理失败] ${f.name}: ${e.message}`);
    }
  });
}

async function connectBrowser() {
  // 重试连接，最多等待 30 秒
  for (let i = 0; i < 6; i++) {
    try {
      return await chromium.connectOverCDP(OPENCLAW_CDP_URL, {
        headers: { 'x-openclaw-relay-token': RELAY_TOKEN }, timeout: 5000,
      });
    } catch (e) {
      if (i < 5) {
        console.log(`  连接失败，5秒后重试 (${i+1}/6)...`);
        await sleep(5000);
      }
    }
  }
  throw new Error('无法连接 OpenClaw 浏览器，请确认已启动');
}

function classifyProduct(title) {
  if (!title) return '其他';
  // 命中缓存直接返回
  if (titleCache.direct[title]) return titleCache.direct[title];
  const lower = title.toLowerCase();
  // 第一轮：前缀优先匹配（标题以关键词开头）
  for (const { type, keywords } of PRODUCT_KEYWORDS) {
    for (const kw of keywords) {
      if (lower.startsWith(kw.toLowerCase())) {
        titleCache.direct[title] = type;
        titleCacheDirty = true;
        return type;
      }
    }
  }
  // 第二轮：普通包含匹配
  for (const { type, keywords } of PRODUCT_KEYWORDS) {
    for (const kw of keywords) {
      if (lower.includes(kw.toLowerCase())) {
        titleCache.direct[title] = type;
        titleCacheDirty = true;
        return type;
      }
    }
  }
  return '其他';
}

// 注意：classifyProductByGroup 已移除，改用 product-groups.js 模块的 mapGroupToCategory 函数

/**
 * 强制分类函数 - 当常规分类失败时使用
 * 1. 先尝试常规分类
 * 2. 如果失败，使用用户自定义映射
 * 3. 如果失败，使用动态分组模块搜索
 * 4. 如果找不到，返回标题或"未知"
 */
async function classifyProductForced(title, context, productGroups, userMapping) {
  if (!title) return '未知';

  // 命中强制缓存直接返回
  if (titleCache.forced[title]) {
    console.log(`  [强制分类] 命中缓存: ${title} → ${titleCache.forced[title].type}`);
    return titleCache.forced[title].type;
  }

  // 第一步：尝试常规分类
  const regularClassify = classifyProduct(title);
  if (regularClassify !== '其他') {
    return regularClassify;
  }

  // 第二步：使用用户自定义映射
  console.log(`  [强制分类] 常规分类失败，检查用户映射...`);
  if (userMapping) {
    const mapped = mapGroupToCategory(title, userMapping);
    if (mapped && mapped !== '其他') {
      console.log(`  [强制分类] 用户映射命中: ${title} → ${mapped}`);
      titleCache.forced[title] = { group: title, type: mapped };
      titleCacheDirty = true;
      return mapped;
    }
  }

  // 第三步：使用动态分组搜索
  console.log(`  [强制分类] 使用动态分组搜索: ${title}`);

  // 3.1 先检查是否匹配已知分组列表
  if (productGroups && productGroups.length > 0) {
    for (const group of productGroups) {
      const lowerTitle = title.toLowerCase();
      const lowerGroup = group.toLowerCase();
      if (lowerTitle.includes(lowerGroup) || lowerGroup.includes(lowerTitle.split(' ')[0])) {
        const category = mapGroupToCategory(group, userMapping);
        console.log(`  [强制分类] 匹配分组: ${group} → ${category}`);
        titleCache.forced[title] = { group: group, type: category };
        titleCacheDirty = true;
        return category;
      }
    }
  }

  // 3.2 去产品分组页面搜索
  const searchResult = await searchGroupByTitle(title, context);
  if (searchResult && searchResult.category && searchResult.category !== '其他') {
    console.log(`  [强制分类] 搜索成功: ${searchResult.group} → ${searchResult.category}`);
    titleCache.forced[title] = { group: searchResult.group, type: searchResult.category };
    titleCacheDirty = true;
    return searchResult.category;
  }

  // 第四步：如果找不到分组信息，返回标题
  console.log(`  [强制分类] 未找到分组信息，返回标题`);
  return title;
}

function isInTimeWindow(chatText) {
  const times = chatText.match(/\d{4}-\d{2}-\d{2} \d{2}:\d{2}/g);
  if (!times || times.length === 0) return { pass: true, earliest: null };
  const earliestStr = times[times.length - 1];
  const inquiryTime = new Date(earliestStr.replace(' ', 'T'));
  const windowStart = new Date(TIME_WINDOW_START);
  const todayEnd = new Date(TIME_WINDOW_END);
  return { pass: inquiryTime >= windowStart && inquiryTime <= todayEnd, earliest: earliestStr, windowStart, todayEnd };
}

function parseLevelFromSrc(src) {
  if (!src) return 'L0';
  const file = src.split('/').pop().split('?')[0];
  return LEVEL_MAP[file] || ('src:' + file.substring(0, 20));
}

// ============ 数据采集函数 ============
async function collectInquiries(page, targetNo) {
  const maxPages = 5; // 最多查找5页
  let allItems = []; // 存储所有页面的询盘数据

  for (let pageNum = 1; pageNum <= maxPages; pageNum++) {
    console.log(`  [分页查找] 正在第 ${pageNum} 页查找询盘 ${targetNo}...`);

    // 动态滚动：检测内容变化，不再固定等待
    // 如果加载数量不足50条，刷新页面重试（最多3次）
    let lastCount = 0;
    let stableRounds = 0;
    let finalCount = 0;

    for (let retry = 0; retry < 3; retry++) {
      lastCount = 0;
      stableRounds = 0;

      for (let i = 0; i < 30; i++) {
        await page.evaluate(() => window.scrollBy(0, 800));
        await sleep(500);
        const count = await page.evaluate(() => document.querySelectorAll('a[href*="maDetail"]').length);
        if (count === lastCount) {
          stableRounds++;
          if (stableRounds >= 3) break;
        } else {
          stableRounds = 0;
          lastCount = count;
        }
      }

      finalCount = await page.evaluate(() => document.querySelectorAll('a[href*="maDetail"]').length);
      console.log(`  [加载检测] 第 ${retry + 1} 次加载，获取到 ${finalCount} 条询盘`);

      // 如果数量足够或已是最后一次重试，跳出
      if (finalCount >= 50 || retry === 2) break;

      // 数量不足，刷新页面重试
      console.log(`  [加载检测] 数量不足50条，刷新页面重试...`);
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 });
      await sleep(3000);
    }

    // 收集当前页的所有询盘数据
    const pageItems = await page.evaluate(({ targetNo, timeWindowStart, timeWindowEnd }) => {
      const cards = Array.from(document.querySelectorAll('a[href*="maDetail"]'));
      const result = [];
      let foundTarget = false;
      const windowStart = new Date(timeWindowStart);
      const windowEnd = new Date(timeWindowEnd);

      cards.forEach((a, idx) => {
        const m = a.href.match(/imInquiryId=(\d+)/);
        if (!m) return;
        const no = m[1];
        let levelSrc = '';
        let handler = '';
        let customerName = '';
        let inquiryTime = null;

        let card = a.closest('[class*="item"]') || a.closest('li') || a.parentElement;
        for (let i = 0; i < 5 && card; i++) {
          if (card.querySelectorAll('a[href*="maDetail"]').length === 1) break;
          card = card.parentElement;
        }
        if (card) {
          const imgs = card.querySelectorAll('img[src*="O1CN01"]');
          if (imgs.length > 0) levelSrc = imgs[0].src;

          // 优先从 .aui-grid-owner-name 提取负责人
          const ownerNameEl = card.querySelector('.aui-grid-owner-name, [class*="owner-name"]');
          if (ownerNameEl) {
            const ownerName = ownerNameEl.getAttribute('title') || ownerNameEl.textContent.trim();
            if (ownerName && ownerName.length > 0) {
              handler = ownerName;
            }
          }

          // 如果没有找到，使用正则表达式提取
          if (!handler) {
            const text = card.innerText || '';
            const hm = text.match(/(?:TM 商机|询盘商机)\s*\t\s*([^\t\n]+?)\s*\t\s*(?:洽谈中|新询盘|待处理|已关闭)/);
            if (hm) handler = hm[1].trim();
          }

          // 提取时间信息
          const text = card.innerText || '';
          const timeMatch = text.match(/(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})/);
          if (timeMatch) {
            inquiryTime = new Date(timeMatch[1]);
          }

          const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

          // 【修复】不再从文本行中提取客户名，因为容易误匹配聊天内容
          // 改为从特定 DOM 元素提取
          const nameEl = card.querySelector('.name, .customer-name, [class*="customerName"], [class*="customer-name"], [class*="buyerName"], [class*="buyer-name"]');
          if (nameEl) {
            const name = nameEl.textContent.trim();
            if (name && name.length >= 2 && name.length <= 50 && /^[A-Za-z]/.test(name)) {
              customerName = name;
            }
          }
        }

        // 先检查是否是目标询盘
        if (no === targetNo) foundTarget = true;

        // 检查时间是否在窗口范围内
        if (inquiryTime && (inquiryTime < windowStart || inquiryTime > windowEnd)) {
          return; // 跳过不在时间窗口内的询盘
        }

        result.push({ no, href: a.href, levelSrc, handler, customerName, idx, inquiryTime: inquiryTime ? inquiryTime.toISOString() : null });
      });

      return { items: result, foundTarget };
    }, { targetNo, timeWindowStart: TIME_WINDOW_START, timeWindowEnd: TIME_WINDOW_END });

    // 将当前页的数据添加到总数据中
    allItems = allItems.concat(pageItems.items);

    // 如果找到目标询盘，返回所有数据
    if (pageItems.foundTarget) {
      console.log(`  [分页查找] 在第 ${pageNum} 页找到目标询盘`);
      console.log(`  [分页查找] 共收集 ${allItems.length} 个询盘（包含前 ${pageNum} 页）`);

      // 找到目标询盘的位置，返回从第一条到目标询盘的所有数据
      const targetIdx = allItems.findIndex(item => item.no === targetNo);
      if (targetIdx !== -1) {
        return allItems.slice(0, targetIdx + 1);
      }
    }

    // 如果没找到且不是最后一页，点击下一页按钮
    if (pageNum < maxPages) {
      console.log(`  [分页查找] 跳转到第 ${pageNum + 1} 页...`);
      const nextClicked = await page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button, a, [class*="next"], [class*="pagination"]'));
        for (const btn of btns) {
          const text = btn.innerText?.trim();
          if (text === '>' || text === '下一页' || btn.getAttribute('aria-label') === '下一页') {
            btn.click();
            return true;
          }
        }
        // 尝试找 next 箭头图标按钮
        const nextBtn = document.querySelector('[class*="next-btn"]:not([disabled]), [class*="pagination-next"]:not([disabled])');
        if (nextBtn) { nextBtn.click(); return true; }
        return false;
      });
      if (!nextClicked) {
        console.log(`  [分页查找] 无法找到下一页按钮，停止翻页`);
        break;
      }
      await sleep(5000);
    }
  }

  throw new Error('未找到目标询盘 ' + targetNo + '（已查找 ' + maxPages + ' 页）');
}

async function readChatHistory(page) {
  await page.evaluate(() => {
    const els = document.querySelectorAll('*');
    for (let i = 0; i < els.length; i++) {
      if (els[i].textContent.trim() === '查看更多历史消息' && els[i].children.length <= 1) {
        els[i].click(); return;
      }
    }
  });
  await sleep(3000);

  const chatText = await page.evaluate(() => {
    const c = document.querySelector('.common-load-more');
    return c ? c.innerText : document.body.innerText.substring(0, 15000);
  });
  const sidebarText = await page.evaluate(() => {
    const s = document.querySelector('[class*="im-alicrm-box"]');
    return s ? s.innerText.substring(0, 1000) : '';
  });
  return { chatText, sidebarText };
}


async function readCountryFromDetail(page) {
  // 加载当前的国家列表（包括新发现的国家）
  const allCountries = loadCountries();

  return page.evaluate((countries) => {
    // 优先：直接查找国旗标签旁的国家文字
    const countryLabel = document.querySelector('span.country-flag-label');
    if (countryLabel && countryLabel.innerText.trim()) return countryLabel.innerText.trim();

    const flagImgs = document.querySelectorAll('img[src*="flag"], img[class*="flag"], [class*="country"] img');
    for (const img of flagImgs) {
      const parent = img.parentElement;
      if (parent) {
        const text = parent.innerText.trim();
        if (text) return text;
        const next = img.nextSibling;
        if (next && next.textContent) return next.textContent.trim();
      }
    }
    const sidebar = document.querySelector('[class*="im-alicrm-box"]');
    if (sidebar) {
      const text = sidebar.innerText;
      const m = text.match(/国家[：:]\s*([^\n]+)/);
      if (m) return m[1].trim();

      // 首先尝试匹配已知国家（包括新发现的）
      for (const c of countries) {
        if (text.includes(c)) return c;
      }

      // 如果没有匹配到已知国家，尝试提取未知国家
      const unknownCountryPatterns = [
        /国家[：:]\s*([^\n，。]+)/,
        /Country[：:]\s*([^\n,\.]+)/i,
        /地区[：:]\s*([^\n，。]+)/,
        /Region[：:]\s*([^\n,\.]+)/i,
        /来自[：:]\s*([^\n，。]+)/,
        /From[：:]\s*([^\n,\.]+)/i,
      ];

      for (const pattern of unknownCountryPatterns) {
        const match = text.match(pattern);
        if (match && match[1]) {
          const country = match[1].trim();
          // 过滤掉太短或包含特殊字符的结果
          if (country.length > 1 && country.length < 50 && !/^[\d\s\-_]+$/.test(country)) {
            return country;
          }
        }
      }
    }
    return '';
  }, allCountries);
}

async function readCustomerName(page) {
  // 【修复】先等待页面元素加载完成
  await sleep(1000);

  return page.evaluate(() => {
    // 【策略1】从聊天卡片中提取客户名称（最精确）
    // 结构：<span class="name">客户名称</span>
    const nameSpan = document.querySelector('.item-content .item-base-info .name');
    if (nameSpan) {
      const name = nameSpan.textContent.trim();
      if (name && name.length >= 2 && name.length <= 50) {
        return name;
      }
    }

    // 【策略2】从询盘详情页的 .name-text 提取客户名称
    const nameText = document.querySelector('.name-text, span.name-text');
    if (nameText) {
      const name = nameText.textContent.trim();
      if (name && name.length >= 2 && !/^(manager assigned|未分配|待分配)$/i.test(name)) {
        return name;
      }
    }

    // 【策略3】从客户信息区域提取（更精准的选择器）
    const customerInfoSelectors = [
      '.customer-info .name',
      '.customer-name',
      '[class*="customerName"]',
      '[class*="customer-name"]',
      '[class*="contact-name"]',
      '[class*="contactName"]',
      '[class*="buyer-name"]',
      '[class*="buyerName"]',
      '[class*="member-name"]',
      '[class*="memberName"]',
    ];
    for (const sel of customerInfoSelectors) {
      const el = document.querySelector(sel);
      if (el) {
        const t = el.textContent.trim();
        if (t && t.length >= 2 && t.length <= 50 && /^[A-Za-z]/.test(t)) {
          // 排除常见非名字字段
          const lower = t.toLowerCase();
          if (!['inquiry', 'tm', 'customer', 'buyer', 'manager', 'assigned', '未分配', '待分配'].some(w => lower.includes(w))) {
            return t;
          }
        }
      }
    }

    // 【策略4】从 title 属性读取客户名称
    const titleElements = document.querySelectorAll('[title]');
    for (const el of titleElements) {
      const title = el.getAttribute('title');
      if (title && title.trim()) {
        const name = title.trim();
        // 过滤无效值
        if (!/^(manager assigned|未分配|待分配|负责人|客户|buyer|customer)$/i.test(name)
            && name.length >= 2
            && name.length <= 50
            && /^[A-Za-z]/.test(name)) {
          return name;
        }
      }
    }

    // 【策略5】从侧边栏提取客户名称（放宽匹配条件）
    const sidebar = document.querySelector('[class*="im-alicrm-box"], [class*="customer-info"], [class*="buyer-info"]');
    if (sidebar) {
      const lines = sidebar.innerText.split('\n').map(l => l.trim()).filter(Boolean);
      for (const line of lines) {
        // 放宽条件：英文开头、长度2-50
        if (!/^[A-Za-z][A-Za-z\s\-\.']+$/.test(line)) continue;
        if (line.length < 2 || line.length > 50) continue;
        // 排除常见非名字字段
        const lower = line.toLowerCase();
        const excludeWords = ['inquiry', 'tm', 'customer', 'buyer', 'country', 'region', 'email', 'phone', 'company', 'date', 'time', 'manager', 'assigned'];
        if (excludeWords.some(w => lower.includes(w))) continue;
        // 排除句子特征
        if (line.split(/\s+/).length > 6) continue;
        if (/[.;,!?]/.test(line)) continue;
        return line;
      }
    }

    // 【已移除】不再从聊天区域提取客户名称，因为聊天内容格式为"客户名 时间 消息内容"，容易误匹配

    return '';
  });
}

async function getProductTitle(page, context) {
  // 用于存储场景信息，供后续分类使用
  const titleContext = { sceneInfo: {} };

  try {
    // 先滚动到页面顶部，确保产品卡片可见
    await page.evaluate(() => window.scrollTo(0, 0));
    await sleep(500);

    // ============================================================
    // 场景识别：区分"询盘卡片"和"TM转询盘"两种场景
    // ============================================================
    let sceneInfo = await page.evaluate(() => {
      // 检测询盘卡片（有产品卡片结构）
      const productCard = document.querySelector('[data-dx-event-datasource*="product_click"]');
      const hasProductCard = !!productCard;

      // 检测 TM 转询盘特征
      const inquiryBox = document.querySelector('.inquiry-product-box');
      const tipSpan = inquiryBox?.querySelector('.inquiry-tip');
      const isTMInquiry = tipSpan?.textContent.includes('Inquiry from TM') ||
                          tipSpan?.textContent.includes('Inquiry from Product Details Page');

      // 检测是否有"询盘"和"采购数量"的卡片（标准询盘卡片）
      const allText = document.body.innerText || '';
      const hasInquiryCard = allText.includes('采购数量') && allText.includes('查看详情');

      // 从主题栏提取（TM转询盘场景）
      const subjectText = document.querySelector('.subject-text');
      const subjectTitle = subjectText?.textContent.trim() || '';

      return { hasProductCard, isTMInquiry, hasInquiryCard, subjectTitle };
    });

    // 保存 sceneInfo 到上下文
    titleContext.sceneInfo = sceneInfo;

    console.log(`  [场景] 产品卡片:${sceneInfo.hasProductCard} TM转询盘:${sceneInfo.isTMInquiry} 询盘卡片:${sceneInfo.hasInquiryCard}`);

    // ============================================================
    // 策略1：从询盘卡片提取（优先级最高）
    // ============================================================
    if (sceneInfo.hasProductCard || sceneInfo.hasInquiryCard) {
      // 1.1 从 data-dx-event-datasource*="product_click" 提取
      const titleFromProductCard = await page.evaluate(() => {
        const productCards = document.querySelectorAll('[data-dx-event-datasource*="product_click"]');
        const candidates = []; // 收集所有候选标题
        for (const card of productCards) {
          const spans = card.querySelectorAll('span[style*="-webkit-line-clamp"]');
          for (const span of spans) {
            const text = span.textContent.trim();
            if (text && text.length >= 10 && text.length <= 300) {
              // 优先英文标题，但也接受其他语言
              if (/^[A-Z]/.test(text)) {
                return text; // 英文标题直接返回
              }
              candidates.push(text);
            }
          }
          const allSpans = card.querySelectorAll('span');
          for (const span of allSpans) {
            const style = span.getAttribute('style') || '';
            if (style.includes('-webkit-line-clamp') || style.includes('-webkit-box')) {
              const text = span.textContent.trim();
              if (text && text.length >= 10 && text.length <= 300) {
                if (/^[A-Z]/.test(text)) {
                  return text;
                }
                candidates.push(text);
              }
            }
          }
        }
        // 如果没有英文标题，返回第一个候选
        return candidates.length > 0 ? candidates[0] : null;
      });
      if (titleFromProductCard) {
        console.log('  [标题] 从产品卡片提取成功');
        return { title: titleFromProductCard, sceneInfo: titleContext.sceneInfo };
      }

      // 1.2 从包含"询盘"和"采购数量"的卡片区域提取
      const titleFromInquiryCard = await page.evaluate(() => {
        const allElements = document.querySelectorAll('*');
        const candidates = [];
        for (const el of allElements) {
          const text = el.innerText || '';
          if (text.includes('询盘') && text.includes('采购数量')) {
            const lines = text.split('\n').map(l => l.trim()).filter(l => l.length >= 10);
            for (const line of lines) {
              if (line.length <= 300 &&
                  !line.match(/\.(pdf|jpg|png|doc|xlsx?)$/i) &&
                  !line.toLowerCase().match(/^(because|our|this|with|you|can|the|we|sorry|please)/) &&
                  (line.includes('Stainless') || line.includes('Steel') ||
                   line.includes('Cabinet') || line.includes('Kitchen') ||
                   line.includes('Outdoor') || line.includes('Grill') ||
                   line.includes('Tool') || line.includes('Wardrobe') ||
                   line.includes('Bathroom') || line.includes('Shoe') ||
                   line.includes('Sideboard') || line.includes('Wine') ||
                   line.includes('TV') || line.includes('Book') ||
                   line.includes('Gun') || line.includes('BBQ') ||
                   line.includes('柜') || line.includes('厨') || line.includes('浴'))) {
                if (/^[A-Z]/.test(line)) return line; // 英文优先
                candidates.push(line);
              }
            }
          }
        }
        return candidates.length > 0 ? candidates[0] : null;
      });
      if (titleFromInquiryCard) {
        console.log('  [标题] 从询盘卡片提取成功');
        return { title: titleFromInquiryCard, sceneInfo: titleContext.sceneInfo };
      }
    }

    // ============================================================
    // 策略2：TM 转询盘场景提取
    // ============================================================
    if (sceneInfo.isTMInquiry) {
      console.log('  [标题] 检测到 TM 转询盘场景');

      // 2.1 从主题栏提取
      if (sceneInfo.subjectTitle && sceneInfo.subjectTitle !== 'Inquiry from TM') {
        console.log('  [标题] 从主题栏提取成功');
        return { title: sceneInfo.subjectTitle, sceneInfo: titleContext.sceneInfo };
      }

      // 2.2 从右侧面板产品卡片提取
      const titleFromPanel = await page.evaluate(() => {
        const selectors = [
          '.product-card-title', '.goods-title', '[class*="product-title"]',
          '[class*="goodsTitle"]', '[class*="item-title"]',
          '[view-name="FrameLayoutNG"] [class*="title"]',
          'h1.product-name', 'h2.product-name', '.product-name'
        ];
        const candidates = [];
        for (const sel of selectors) {
          const el = document.querySelector(sel);
          if (el) {
            const text = el.textContent.trim();
            if (text && text.length >= 10 && !text.includes('\n')) {
              if (/^[A-Z]/.test(text)) return text; // 英文优先
              candidates.push(text);
            }
          }
        }
        return candidates.length > 0 ? candidates[0] : null;
      });
      if (titleFromPanel) {
        console.log('  [标题] 从右侧面板提取成功');
        return { title: titleFromPanel, sceneInfo: titleContext.sceneInfo };
      }

      // 2.3 从产品消息卡片提取（TM转询盘产品卡片）
      // 这是 TM 转询盘中产品卡片的标准结构
      const titleFromMessageCard = await page.evaluate(() => {
        const candidates = [];

        // 方法1：从 data-exp="2020MC_MessageCard_Show" 卡片提取
        const messageCards = document.querySelectorAll('[data-exp="2020MC_MessageCard_Show"]');
        for (const card of messageCards) {
          // 检查是否是产品卡片
          const expinfo = card.getAttribute('data-expinfo') || '';
          if (expinfo.includes('"extBizType":"product"') || expinfo.includes('"messageType":54') || expinfo.includes('"messageType":100010')) {
            // 在卡片内查找 TextView 组件
            const textViews = card.querySelectorAll('div[view-name="TextView"] span, span[style*="-webkit-line-clamp"]');
            for (const tv of textViews) {
              const text = tv.textContent.trim();
              if (text && text.length >= 10 && text.length <= 300) {
                if (/^[A-Z]/.test(text)) return text;
                candidates.push(text);
              }
            }
          }
        }

        // 方法2：从 .message-item-wrapper[data-exp="2020MC_Message_Show"] 提取
        const messageItems = document.querySelectorAll('.message-item-wrapper[data-exp="2020MC_Message_Show"]');
        for (const item of messageItems) {
          const expinfo = item.getAttribute('data-expinfo') || '';
          if (expinfo.includes('"extBizType":"product"')) {
            // 查找卡片内容区域
            const cardContent = item.querySelector('.session-rich-content.card, .card-content');
            if (cardContent) {
              const textViews = cardContent.querySelectorAll('div[view-name="TextView"] span, span[style*="-webkit-line-clamp"]');
              for (const tv of textViews) {
                const text = tv.textContent.trim();
                if (text && text.length >= 10 && text.length <= 300) {
                  if (/^[A-Z]/.test(text)) return text;
                  candidates.push(text);
                }
              }
            }
          }
        }

        // 方法3：从滑动区域的产品卡片提取（TM转询盘右侧产品卡片）
        // 特征：div[view-name="TextView"] 内的 span 带有 -webkit-line-clamp 样式
        const allTextViews = document.querySelectorAll('div[view-name="TextView"]');
        for (const tv of allTextViews) {
          // 查找带有 -webkit-line-clamp 的 span（通常是产品标题）
          const span = tv.querySelector('span[style*="-webkit-line-clamp"]');
          if (span) {
            const text = span.textContent.trim();
            // 产品标题特征：英文开头、长度10-200、包含产品关键词
            if (text && text.length >= 10 && text.length <= 200 && /^[A-Z]/.test(text)) {
              // 检查是否包含产品关键词
              const productKeywords = ['Stainless', 'Steel', 'Kitchen', 'Cabinet', 'Grill', 'Outdoor', 'Tool', 'BBQ', 'Oven', 'Wardrobe', 'Sideboard', 'Bathroom', 'Wine'];
              if (productKeywords.some(kw => text.includes(kw))) {
                return text;
              }
            }
          }
        }

        return candidates.length > 0 ? candidates[0] : null;
      });
      if (titleFromMessageCard) {
        console.log('  [标题] 从消息卡片提取成功');
        return { title: titleFromMessageCard, sceneInfo: titleContext.sceneInfo };
      }

      // 2.4 从 data-original 属性提取产品相关内容
      // 注意：data-original 可能包含产品描述而非标题，需要严格过滤
      const titleFromOriginal = await page.evaluate(() => {
        const messageItems = document.querySelectorAll('.message-item-wrapper[data-original]');
        const candidates = [];
        for (const item of messageItems) {
          const original = item.getAttribute('data-original') || '';
          // 过滤条件：长度10-300、包含产品关键词
          // 排除：产品描述（包含逗号+空格后跟小写字母的连续句子）
          if (original.length > 10 && original.length <= 300 &&
              (original.includes('Stainless') || original.includes('Steel') ||
               original.includes('Cabinet') || original.includes('Kitchen') ||
               original.includes('Grill') || original.includes('Outdoor') ||
               original.includes('Tool') || original.includes('BBQ') ||
               original.includes('柜') || original.includes('厨'))) {
            // 排除产品描述（通常是多句子，包含 "The ... is ..." 结构）
            const isDescription = /[,.] [a-z]/.test(original) && original.includes(' is ') && original.split(' ').length > 20;
            if (!isDescription) {
              if (/^[A-Z]/.test(original)) return original; // 英文优先
              candidates.push(original);
            }
          }
        }
        return candidates.length > 0 ? candidates[0] : null;
      });
      if (titleFromOriginal) {
        console.log('  [标题] 从 data-original 提取成功');
        return { title: titleFromOriginal, sceneInfo: titleContext.sceneInfo };
      }

      // 注意：聊天关键词提取已移到策略5，作为最终兜底
    }

    // ============================================================
    // 策略3：从页面 JSON 数据提取
    // ============================================================
    const titleFromJson = await page.evaluate(() => {
      const results = [];
      const scripts = document.querySelectorAll('script');
      for (const script of scripts) {
        const content = script.textContent || '';
        const patterns = [
          /"productName":"([^"]+)"/g,
          /"title":"([^"]{30,200})"/g,
          /"subject":"([^"]{30,200})"/g,
          /"productTitle":"([^"]{30,200})"/g
        ];
        for (const regex of patterns) {
          let match;
          while ((match = regex.exec(content)) !== null) {
            const val = match[1];
            if (val && val.length > 20 && /^[A-Z]/.test(val)) {
              results.push(val);
            }
          }
        }
      }
      if (results.length > 0) {
        const counts = {};
        results.forEach(r => counts[r] = (counts[r] || 0) + 1);
        return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
      }
      return null;
    });
    if (titleFromJson) {
      console.log('  [标题] 从JSON数据提取成功');
      return { title: titleFromJson, sceneInfo: titleContext.sceneInfo };
    }

    // ============================================================
    // 策略4：跳转产品详情页提取
    // ============================================================
    const productUrl = await page.evaluate(() => {
      const links = document.querySelectorAll('a[href*="alibaba.com/product-detail"], a[href*="alibaba.com/offer"]');
      if (links.length > 0) return links[0].href;
      const allLinks = document.querySelectorAll('a');
      for (const a of allLinks) {
        const href = a.href || '';
        if (href.includes('alibaba.com') && (href.includes('product') || href.includes('offer'))) {
          return href;
        }
      }
      return null;
    });
    if (productUrl) {
      try {
        const productPage = await context.newPage();
        await productPage.goto(productUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
        await sleep(3000);
        const title = await productPage.evaluate(() => {
          const h1 = document.querySelector('h1');
          return h1 ? h1.textContent.trim() : document.title;
        });
        await productPage.close();
        if (title) {
          console.log('  [标题] 从产品详情页提取成功');
          return { title, sceneInfo: titleContext.sceneInfo };
        }
      } catch (e) {
        console.log('  [标题] 产品详情页访问失败');
      }
    }

    // ============================================================
    // 策略5：从侧边栏行为数据提取（客户最常采购行业）
    // 注意：这里提取的是行业名称，不是产品标题
    // 返回 { isIndustry: true, value: string } 结构
    // ============================================================
    const behaviorData = await page.evaluate(() => {
      // 尝试从客户行为卡片提取采购行业
      const selectors = [
        '.alicrm-customer-behavioral-card-purchase-industry .content',
        '.customer-behavioral-card .purchase-industry',
        '[class*="purchase-industry"] .content',
        '[class*="purchaseIndustry"]'
      ];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          const text = el.textContent.trim();
          // 提取第一个行业作为产品类型
          if (text && text.length > 3) {
            // 分割多个行业，取第一个
            const industries = text.split(/[|,，、]/).map(s => s.trim()).filter(s => s.length > 2);
            if (industries.length > 0) {
              return { isIndustry: true, value: industries[0] };
            }
          }
        }
      }
      return null;
    });
    if (behaviorData && behaviorData.isIndustry) {
      console.log('  [标题] 从客户行为数据提取行业:', behaviorData.value);
      // 保存行为数据供后续分类使用
      titleContext.sceneInfo.behaviorIndustry = behaviorData.value;
      // 注意：行为数据是行业名称，不直接作为标题返回
      // 继续尝试聊天关键词提取
    }

    // ============================================================
    // 策略6：从聊天记录提取产品关键词（最终兜底）
    // 注意：这里返回的是产品类型，不是完整标题
    // ============================================================
    const keywordsFromChat = await page.evaluate(() => {
      const chatArea = document.querySelector('.im-message-flow, .scroll-box, .mc-history-wrapper');
      if (!chatArea) return null;
      const chatText = chatArea.innerText || '';
      // 扩展关键词映射，增加更多变体
      // 注意：优先匹配更具体的关键词（按长度降序排序）
      const keywordMap = {
        'Outdoor Kitchen': 'Outdoor Kitchen',
        'Tool Cabinet': 'Tool Cabinet',
        'Bathroom Cabinet': 'Bathroom Cabinet',
        'Shoe Cabinet': 'Shoe Cabinet',
        'Gun Cabinet': 'Gun Cabinet',
        'Sink Cabinet': 'Sink Cabinet',
        'BBQ Grill': 'BBQ Grill',
        'barbecue': 'BBQ Grill', '烧烤': 'BBQ Grill',
        'Grill': 'BBQ Grill',
        'Kitchen': 'Kitchen Cabinet', '厨房': 'Kitchen Cabinet',
        'Cabinet': 'Cabinet', '柜': 'Cabinet',
        'outdoor': 'Outdoor Kitchen', '户外': 'Outdoor Kitchen',
        'Stainless': 'Stainless Steel', '不锈钢': 'Stainless Steel',
        'Tool': 'Tool Cabinet', '工具': 'Tool Cabinet',
        'Wardrobe': 'Wardrobe', '衣柜': 'Wardrobe',
        'Bathroom': 'Bathroom Cabinet', '浴室': 'Bathroom Cabinet',
        'Shoe': 'Shoe Cabinet', '鞋柜': 'Shoe Cabinet',
        'Sideboard': 'Sideboard', '餐边柜': 'Sideboard',
        'Gun': 'Gun Cabinet', '枪柜': 'Gun Cabinet',
        'sink': 'Sink Cabinet', '水槽': 'Sink Cabinet',
        'refrigerator': 'Refrigerator Cabinet', '冰箱': 'Refrigerator Cabinet'
      };
      const lowerChat = chatText.toLowerCase();
      // 按关键词长度降序排序，优先匹配更具体的关键词
      const sortedKeywords = Object.entries(keywordMap).sort((a, b) => b[0].length - a[0].length);
      for (const [keyword, productType] of sortedKeywords) {
        if (lowerChat.includes(keyword.toLowerCase())) {
          return productType;
        }
      }
      return null;
    });
    if (keywordsFromChat) {
      console.log('  [标题] 从聊天记录提取产品类型（兜底）:', keywordsFromChat);
      return { title: keywordsFromChat, sceneInfo: titleContext.sceneInfo };
    }

    // ============================================================
    // 策略7：识别纯 TM 询盘，返回标记
    // ============================================================
    const isPureTM = await page.evaluate(() => {
      const tip = document.querySelector('.inquiry-tip');
      const hasProduct = document.querySelector('[data-expinfo*="extBizType"]');
      return tip?.textContent.includes('Inquiry from TM') && !hasProduct;
    });
    if (isPureTM) {
      console.log('  [标题] 纯 TM 询盘，无产品关联');
      return { title: 'TM咨询', sceneInfo: titleContext.sceneInfo };
    }

    return { title: null, sceneInfo: titleContext.sceneInfo };
  } catch (e) {
    console.log(`  [标题] 获取失败: ${e.message}`);
    return { title: null, sceneInfo: titleContext.sceneInfo };
  }
}


// ============ 调试函数：截图保存DOM ============
async function debugInquiryPage(page, inquiryId) {
  const debugDir = './debug-dumps';
  const fs = require('fs');
  if (!fs.existsSync(debugDir)) fs.mkdirSync(debugDir, { recursive: true });

  const prefix = `${debugDir}/${inquiryId}`;

  // 截图
  await page.screenshot({ path: `${prefix}.png`, fullPage: true });
  console.log(`  [调试] 截图已保存: ${prefix}.png`);

  // DOM
  const html = await page.content();
  fs.writeFileSync(`${prefix}.html`, html);
  console.log(`  [调试] DOM已保存: ${prefix}.html`);

  // SSR JSON 数据
  const jsonData = await page.evaluate(() => {
    const results = [];
    const scripts = document.querySelectorAll('script');
    for (const script of scripts) {
      const content = script.textContent || '';
      if (content.includes('productName') || content.includes('productTitle') || content.includes('subject')) {
        results.push(content.substring(0, 5000));
      }
    }
    return results;
  });
  if (jsonData.length > 0) {
    fs.writeFileSync(`${prefix}-json.json`, JSON.stringify(jsonData, null, 2));
    console.log(`  [调试] JSON数据已保存: ${prefix}-json.json`);
  }
}

// ============ 链接导航函数 ============

/**
 * 导航到询盘页面
 * 用于获取所有反馈/询盘列表
 */
async function navigateToInquiryPage(page) {
  try {
    console.log('导航到询盘页面...');
    await page.goto(ALIBABA_LINKS.inquiryPage, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await sleep(5000);

    // 点击"日期"按钮
    console.log('  [排序] 点击日期按钮...');
    const dateBtn = page.locator('a.aui-menu-button[data-role="date-selector"]').first();
    await dateBtn.waitFor({ timeout: 10000 });
    await dateBtn.click();
    await sleep(1500);

    // 选择"按创建时间从新到旧"
    console.log('  [排序] 选择按创建时间从新到旧...');
    const sortItem = page.locator('span[data-widget-point="menuLabel"]', { hasText: '按创建时间从新到旧' }).first();
    await sortItem.waitFor({ timeout: 10000 });
    await sortItem.click();
    await sleep(3000);

    // 滚动到底部，点击每页100条
    console.log('  [分页] 设置每页100条...');
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await sleep(1500);
    const pageSizeBtn = page.locator('a[data-page-size="100"]').first();
    await pageSizeBtn.waitFor({ timeout: 10000 });
    await pageSizeBtn.click();
    await sleep(5000);

    console.log('询盘页面已加载');
    return true;
  } catch (e) {
    console.error(`导航到询盘页面失败: ${e.message}`);
    return false;
  }
}

// ============ 数据提取函数 ============
function extractPeriod(chatText) {
  const times = chatText.match(/(\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2})/g);
  if (!times || times.length === 0) return '';
  const earliest = times[times.length - 1];
  const m = earliest.match(/\d{4}-(\d{2})-(\d{2}) (\d{2}:\d{2})/);
  if (!m) return '';
  return parseInt(m[1]) + '/' + parseInt(m[2]) + ' ' + m[3];
}

function extractMonth(chatText) {
  const m = chatText.match(/\d{4}-(\d{2})-\d{2}/);
  if (!m) return '3月';
  return parseInt(m[1]) + '月';
}

function extractStatus(chatText) {
  if (/下单|付款|order confirmed|payment confirmed/i.test(chatText)) return '有效客户';
  if (/个人买家/.test(chatText)) return '个人买家';
  const lines = chatText.split('\n').filter(l => l.trim());
  const last20 = lines.slice(-20).join('\n');
  if (/已读/.test(last20)) return '已读未回';
  return '未读未回';
}

function extractHandler(chatText) {
  if (/Jane Tang/i.test(chatText)) return 'Jane Tang';
  if (/Stephen Yang/i.test(chatText)) return 'Stephen Yang';
  if (/Hyrley|Victor/i.test(chatText)) return 'Hyrley Victor';
  return 'Hyrley Victor';
}

function buildSummary(data, chatText) {
  const prices = chatText.match(/\$[\d,]+(?:\.\d+)?/g) || [];
  const priceStr = prices.length > 0 ? '，已报价' + prices[prices.length - 1].replace('$', 'USD') : '，待报价';
  const intent = (data.status === '有效客户') ? '高意向客户' : '潜在客户';
  return `${intent}，询${data.product}${priceStr}，${data.status}`;
}

// ============ 聊天内容产品提取 ============
// 当客户没有通过询盘/TM卡片进来（productTitle 为 null）时，从聊天内容分析产品
const PRODUCT_HINT_WORDS = [
  'cabinet', 'kitchen', 'grill', 'tool', 'outdoor', 'stainless', 'steel',
  'wardrobe', 'shelf', 'storage', 'bbq', 'furniture', 'drawer', 'sideboard',
  'wine', 'bookcase', 'closet', 'rack', 'chest', 'workbench', 'kamado',
  'barbecue', 'smoker', 'cupboard', 'locker', 'toolbox', 'shed', 'pod',
  'island', 'countertop', 'sink', 'faucet', 'oven', 'refrigerator',
];

function looksLikeProduct(text) {
  const lower = text.toLowerCase();
  return PRODUCT_HINT_WORDS.some(kw => lower.includes(kw));
}

function extractProductFromChat(chatText) {
  if (!chatText) return null;

  const lines = chatText.split('\n').map(l => l.trim()).filter(l => l.length > 8);

  // 内部辅助：将描述解析为产品类型，新发现写入 chat-products.json
  function resolveDesc(desc) {
    if (!desc || !looksLikeProduct(desc)) return null;
    // 先查聊天产品缓存
    if (chatProductsMap[desc] && chatProductsMap[desc] !== '其他') return chatProductsMap[desc];
    // 再用关键词分类
    const classified = classifyProduct(desc);
    if (classified !== '其他') return classified;
    // 新发现：写入缓存供用户补充，报告显示"其他"
    if (!chatProductsMap[desc]) {
      chatProductsMap[desc] = '其他';
      chatProductsDirty = true;
      console.log(`  [聊天产品] 新发现已保存: ${desc}`);
    }
    return null;
  }

  // 模式1：客户明确表达需求的句子
  const inquiryPatterns = [
    /i(?:'m| am) (?:looking for|interested in|inquiring about|searching for)\s+(.{10,100})/i,
    /(?:do you (?:have|sell|make|produce|manufacture))\s+(.{10,100})/i,
    /(?:price|quote|quotation)\s+(?:for|of)\s+(.{10,100})/i,
    /(?:product|item|model)[:\s]+([A-Za-z].{10,80})/i,
  ];

  for (const line of lines) {
    if (/[\u4e00-\u9fa5]/.test(line)) continue;
    if (/^(hi|hello|dear|good morning|good afternoon|thank|yes|no|ok|sure|great|noted|understood|perfect)/i.test(line)) continue;

    for (const pattern of inquiryPatterns) {
      const m = line.match(pattern);
      if (m && m[1]) {
        const result = resolveDesc(m[1].trim().replace(/[.,!?;]$/, '').substring(0, 80));
        if (result) return result;
      }
    }
  }

  // 模式2：找含产品关键词的英文行
  const candidates = lines
    .filter(l => /^[A-Z]/.test(l) && l.length > 20 && l.length < 120)
    .filter(l => !/^(Hi|Hello|Dear|Good|Thank|Please|Yes|No|Ok|Sure|Great|Noted|I |We |My |Our )/i.test(l))
    .filter(l => !/[\u4e00-\u9fa5]/.test(l))
    .filter(l => looksLikeProduct(l));

  for (const line of candidates) {
    const result = resolveDesc(line);
    if (result) return result;
  }

  return null;
}

// ============ 主函数 ============
async function main() {
  // 获取命令行参数
  const targetInquiry = process.argv[2];
  if (!targetInquiry) {
    console.error('用法: node inquiry-analyzer.js <目标询盘号>');
    console.error('示例: node inquiry-analyzer.js 13789026663');
    process.exit(1);
  }

  // 确保输出目录存在
  if (!fs.existsSync('chats')) fs.mkdirSync('chats');
  if (!fs.existsSync('reports')) fs.mkdirSync('reports');
  if (!fs.existsSync('csv-reports')) fs.mkdirSync('csv-reports');

  // 自动清理旧文件：每个目录只保留最近 10 个文件
  cleanOldFiles('reports', 10);
  cleanOldFiles('csv-reports', 10);
  cleanOldFiles('chats', 10);
  cleanOldFiles('okki-reports', 10);

  // 检查 OpenClaw 是否在运行
  const http = require('http');
  const isRunning = await new Promise(resolve => {
    const req = http.get(OPENCLAW_CDP_URL, () => resolve(true));
    req.on('error', () => resolve(false));
    req.setTimeout(3000, () => { req.destroy(); resolve(false); });
  });
  if (!isRunning) {
    console.error('❌ OpenClaw 浏览器未运行，请先手动启动：');
    console.error(`   node "${OPENCLAW_PATH}" browser start`);
    process.exit(1);
  }
  console.log('✅ OpenClaw 浏览器已运行');

  const browser = await connectBrowser();
  console.log('Browser Relay 连接成功');

  const context = browser.contexts()[0];

  // 打开登录页确认已登录
  console.log('正在打开阿里巴巴，确认登录状态...');
  const loginPage = await context.newPage();
  await loginPage.goto('https://www.alibaba.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(3000);
  await loginPage.close();
  console.log('✅ 已连接阿里巴巴，继续执行...');

  // 每次都新开一个 tab 导航到询盘页面
  console.log('打开阿里巴巴询盘页面...');
  let aliPage = await context.newPage();
  const success = await navigateToInquiryPage(aliPage);
  if (!success) {
    console.error('无法打开询盘页面，请确保已登录阿里巴巴');
    process.exit(1);
  }

  console.log('收集询盘列表...');
  const items = await collectInquiries(aliPage, targetInquiry);
  console.log(`找到 ${items.length} 个询盘（含目标盘）`);

  // 动态获取产品分组列表
  console.log('获取产品分组列表...');
  const productGroups = await fetchProductGroups(context);
  console.log(`已加载 ${productGroups.length} 个产品分组`);

  // 加载用户自定义映射
  const userMapping = loadUserMapping();
  if (Object.keys(userMapping).length > 0) {
    console.log(`已加载 ${Object.keys(userMapping).length} 个用户自定义映射`);
  }

  // 检查是否需要配置向导（首次运行且无映射）
  const needConfig = productGroups.length > 0 && Object.keys(userMapping).length === 0 && !fs.existsSync(MAPPING_FILE);
  if (needConfig) {
    console.log('\n========== 首次运行检测 ==========');
    console.log('检测到未配置产品分组映射，是否运行配置向导？');
    console.log('配置向导将帮助您为每个产品分组指定对应的产品类型。');
    console.log('');
    console.log('选择：');
    console.log('  1. 运行配置向导（交互式配置）');
    console.log('  2. 自动配置（使用建议类型）');
    console.log('  3. 跳过（稍后手动配置）');

    // 简化处理：自动配置
    console.log('\n[自动配置] 正在为分组分配建议类型...');
    autoConfigureProductMapping(productGroups);
  }

  const results = [];
  const seenCustomers = new Set(); // 用于去重：同一客户只记录第一条

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    console.log(`\n[${i+1}/${items.length}] 处理询盘 ${item.no}`);

    try {
      await aliPage.goto(item.href, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await sleep(5000);

      // 点击"客户/Customer"标签以获取客户详细信息
      try {
        const customerTabClicked = await aliPage.evaluate(() => {
          const tabs = Array.from(document.querySelectorAll('*'));
          for (const tab of tabs) {
            const text = tab.innerText?.trim();
            if (text === '客户' || text === 'Customer' || text === '客户信息') {
              if (tab.tagName === 'BUTTON' || tab.tagName === 'A' || tab.classList.contains('tab') || tab.classList.contains('button')) {
                tab.click();
                return true;
              }
              const clickable = tab.closest('button, a, [role="button"], [class*="tab"], [class*="button"]');
              if (clickable) {
                clickable.click();
                return true;
              }
            }
          }
          return false;
        });
        if (customerTabClicked) {
          await sleep(2000);
        }
      } catch (e) {
        console.log(`  [提示] 未找到客户标签或点击失败: ${e.message}`);
      }

      const { chatText } = await readChatHistory(aliPage);

      const timeCheck = isInTimeWindow(chatText);
      if (!timeCheck.pass) {
        console.log(`  [跳过] 开始时间 ${timeCheck.earliest} 不在窗口内`);
        console.log(`  窗口：${timeCheck.windowStart?.toLocaleString()} ~ ${timeCheck.todayEnd?.toLocaleString()}`);
        continue;
      }
      console.log(`  [通过] 开始时间 ${timeCheck.earliest}`);

      const country = await readCountryFromDetail(aliPage);
      console.log(`  国家: ${country}`);

      // 如果获取到国家信息且不在基础列表中，则保存为新国家
      if (country && country.length > 0) {
        const baseCountries = BASE_COUNTRIES;
        if (!baseCountries.includes(country)) {
          saveNewCountry(country);
        }
      }

      let customerName = item.customerName || '';
      if (!customerName) {
        customerName = await readCustomerName(aliPage);
      }
      // 过滤"manager assigned"等占位符，替换为"待确认"
      if (customerName && /^(manager assigned|未分配|待分配)$/i.test(customerName.trim())) {
        customerName = '待确认';
      }
      console.log(`  客户: ${customerName}`);

      // 生成文件名：客户名称+时间戳
      const ts = new Date().toISOString().replace(/[T:]/g, '-').substring(0, 16);
      const safeCustomerName = (customerName || 'unknown').replace(/[<>:"/\\|?*]/g, '_');
      const chatFilename = `chats/${safeCustomerName}_${ts}.txt`;
      fs.writeFileSync(chatFilename, chatText);

      const level = parseLevelFromSrc(item.levelSrc);
      console.log(`  L+: ${level} (src: ${item.levelSrc.split('/').pop()?.substring(0,20)})`);

      const titleResult = await getProductTitle(aliPage, context);
      const rawTitle = titleResult.title;

      // 如果标题获取失败，启用调试模式
      if (!rawTitle) {
        console.log('  [标题] 未获取到标题，启动调试...');
        await debugInquiryPage(aliPage, item.no);
      }

      // 过滤无效标题：必须是英文、排除地址/多品类/聊天片段/文件名
      const rawTrimmed = rawTitle ? rawTitle.trim() : null;
      const productTitle = (rawTrimmed &&
        rawTrimmed.length > 10 &&
        !/^inquiry from/i.test(rawTrimmed) &&
        // 必须是纯英文标题（排除中文、西语、法语、德语、意语、俄语等）
        /^[A-Za-z0-9\s\-\'\.\,\&\+\(\)\/]+$/.test(rawTrimmed) &&
        // 过滤地址字符串（含街道/城市/国家）
        !/\b(street|avenue|road|drive|lane|ave|blvd|close|glebe|houliston|inverkeithing|nottinghamshire|united kingdom|united states|england|scotland|australia|canada)\b/i.test(rawTrimmed) &&
        !/\b[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}\b/.test(rawTrimmed) &&
        // 过滤多品类字符串（3个以上 | 分隔）
        !(rawTrimmed.split('|').length >= 3) &&
        // 过滤文件名
        !rawTrimmed.match(/\.(pdf|jpg|png|doc|xlsx?|csv)$/i) &&
        // 过滤聊天片段（对话开头词）
        !/^(to start|i'll need|i need|please|hello|hi |dear |good |thank|what is|can you|could you|sry|sorry|our customers|because|we use)/i.test(rawTrimmed) &&
        // 过滤句子型内容（包含多个小写单词连接词）
        !(/\b(because|our|this|with|you|can|the|we|sry|sorry|pls|please|those|these)\b.*\b(is|are|was|were|have|has|will|would|could|can)\b/i.test(rawTrimmed))
      ) ? rawTrimmed : null;

      // ============ 产品分类逻辑（三步判断） ============
      // 第一步：有标题时，优先使用标题进行分类
      // 第二步：标题分类失败，才从聊天内容判断
      // 第三步：都失败，返回"其他"
      let product = '其他';

      if (productTitle) {
        // 【有标题】三步判断流程
        // 第1步：查标题缓存（direct -> forced）
        if (titleCache.direct[productTitle]) {
          product = titleCache.direct[productTitle];
          console.log(`  [分类] 第1步-缓存命中 direct: ${product}`);
        } else if (titleCache.forced[productTitle]) {
          product = titleCache.forced[productTitle].type;
          console.log(`  [分类] 第1步-缓存命中 forced: ${product}`);
        } else {
          // 第2步：关键词分类
          product = classifyProduct(productTitle);
          if (product !== '其他') {
            console.log(`  [分类] 第2步-关键词分类: ${product}`);
          } else {
            // 第3步：强制分类（去产品分组页面搜索）
            console.log(`  [分类] 第3步-启动强制分类...`);
            const forcedResult = await classifyProductForced(productTitle, context, productGroups, userMapping);
            if (forcedResult && forcedResult.type && forcedResult.type !== '其他' && forcedResult.type !== productTitle) {
              titleCache.forced[productTitle] = { group: forcedResult.group, type: forcedResult.type };
              titleCacheDirty = true;
              product = forcedResult.type;
              console.log(`  [分类] 第3步-强制分类成功: ${forcedResult.group} → ${product}`);
            } else if (forcedResult && forcedResult.type) {
              product = forcedResult.type;
              console.log(`  [分类] 第3步-强制分类结果: ${product}`);
            } else {
              console.log(`  [分类] 第3步-强制分类失败，保持"其他"`);
            }
          }
        }
      } else {
        // 【无标题】从聊天内容分析产品
        // 先尝试从询盘卡片提取标题
        const titleFromChat = (() => {
          const m = chatText.match(/询盘\n(.+?)\n采购数量/s);
          return m ? m[1].trim() : null;
        })();

        if (titleFromChat) {
          // 查缓存
          if (titleCache.direct[titleFromChat]) {
            product = titleCache.direct[titleFromChat];
            console.log(`  [分类] 聊天标题-缓存命中 direct: ${product}`);
          } else if (titleCache.forced[titleFromChat]) {
            product = titleCache.forced[titleFromChat].type;
            console.log(`  [分类] 聊天标题-缓存命中 forced: ${product}`);
          } else {
            // 关键词分类
            product = classifyProduct(titleFromChat);
            if (product !== '其他') {
              console.log(`  [分类] 聊天标题-关键词分类: ${product}`);
            }
          }
        }

        // 如果还是"其他"，从聊天内容关键词分析
        if (product === '其他') {
          const productFromChat = classifyProduct(chatText);
          if (productFromChat !== '其他') {
            product = productFromChat;
            console.log(`  [分类] 聊天内容-关键词分析: ${product}`);
          }
        }

        // 最后尝试提取产品描述
        if (product === '其他') {
          const chatProduct = extractProductFromChat(chatText);
          if (chatProduct) {
            product = chatProduct;
            console.log(`  [分类] 聊天内容-产品提取: ${product}`);
          }
        }

        // 最后尝试使用行为数据中的行业信息
        if (product === '其他' && titleResult.sceneInfo?.behaviorIndustry) {
          const industryProduct = classifyProduct(titleResult.sceneInfo.behaviorIndustry);
          if (industryProduct !== '其他') {
            product = industryProduct;
            console.log(`  [分类] 行为数据-行业分类: ${product} (来源: ${titleResult.sceneInfo.behaviorIndustry})`);
          }
        }
      }

      console.log(`  商品标题: ${productTitle}`);
      console.log(`  产品型号: ${product}`);

      // 去重：同一客户名只保留第一条
      const dedupeKey = customerName.toLowerCase().trim();
      if (customerName && seenCustomers.has(dedupeKey)) {
        console.log(`  [跳过] 重复询盘（${customerName}）`);
        continue;
      }
      if (customerName) seenCustomers.add(dedupeKey);

      const period = extractPeriod(chatText);
      const month = extractMonth(chatText);
      const status = extractStatus(chatText);
      const handler = item.handler || extractHandler(chatText);

      const data = {
        inquiryId: item.no,
        month,
        product,
        period,
        status,
        country,
        customerName,
        level,
        handler,
        chatText,
      };
      data.summary = buildSummary(data, chatText);

      console.log(`  状态: ${status} | 回复人: ${handler}`);
      console.log(`  总结: ${data.summary}`);

      results.push(data);

    } catch (e) {
      console.error(`  处理出错: ${e.message}`);
      // Browser/context/tab 断开时，重新连接 browser 并重试当前询盘
      if (/Target page, context or browser has been closed/i.test(e.message)) {
        console.log('  [重连] 连接断开，正在重新连接浏览器...');
        try {
          const newBrowser = await connectBrowser();
          const newContext = newBrowser.contexts()[0];
          aliPage = await newContext.newPage();
          console.log('  [重连] 重连成功，重试当前询盘...');
          i--; // 重试当前询盘
        } catch (reconnectErr) {
          console.error(`  [重连失败] ${reconnectErr.message}`);
        }
      }
    }
  }

  // 统计每个业务员的客户数
  const handlerStats = {};
  for (const r of results) {
    const handler = r.handler || '未知';
    handlerStats[handler] = (handlerStats[handler] || 0) + 1;
  }

  // 格式化统计结果
  let statsText = '';
  let total = 0;
  for (const [handler, count] of Object.entries(handlerStats)) {
    statsText += `${handler}：${count}\n`;
    total += count;
  }
  statsText += `合计：${total}`;

  // 输出 Markdown 表格
  const windowEnd = new Date(TIME_WINDOW_END);
  const registerDate = `${windowEnd.getFullYear()}/${windowEnd.getMonth()+1}/${windowEnd.getDate()}`;
  const currentMonth = `${windowEnd.getMonth()+1}月`;

  console.log('\n\n========== 询盘分析表格 ==========\n');
  console.log('| 询盘单号 | 月份 | 登记日期 | 询盘回复人 | 产品型号 | 时间段 | 客户类型 | 总新客数 | 国家 | 客户名称 | L几 | 业务具体客户数 | 新增业务具体客户数 |');
  console.log('|----------|------|----------|------------|----------|--------|----------|----------|------|----------|-----|----------------|-------------------|');
  for (const r of results) {
    console.log(`| ${r.inquiryId} | ${currentMonth} | ${registerDate} | ${r.handler} | ${r.product} | ${r.period} | ${r.status} |  | ${r.country} | ${r.customerName} | ${r.level} |  |  |`);
  }

  // 保存到文件
  let md = '| 询盘单号 | 月份 | 登记日期 | 询盘回复人 | 产品型号 | 时间段 | 客户类型 | 总新客数 | 国家 | 客户名称 | L几 | 业务具体客户数 | 新增业务具体客户数 |\n';
  md += '|----------|------|----------|------------|----------|--------|----------|----------|------|----------|-----|----------------|-------------------|\n';
  for (const r of results) {
    md += `| ${r.inquiryId} | ${currentMonth} | ${registerDate} | ${r.handler} | ${r.product} | ${r.period} | ${r.status} |  | ${r.country} | ${r.customerName} | ${r.level} |  |  |\n`;
  }
  const ts = new Date().toISOString().replace(/[T:]/g, '-').substring(0, 16);
  const reportFile = `reports/inquiry-report-${targetInquiry}-${ts}.md`;
  fs.writeFileSync(reportFile, md);
  console.log(`\n表格已保存到 ${reportFile}`);

  // 生成 CSV 格式
  let csv = '询盘单号,月份,登记日期,询盘回复人,产品型号,时间段,客户类型,总新客数,国家,客户名称,L几,业务具体客户数,新增业务具体客户数\n';
  for (const r of results) {
    const escapeCsv = (str) => {
      if (!str) return '';
      str = String(str);
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };
    csv += `${escapeCsv(r.inquiryId)},${escapeCsv(currentMonth)},${escapeCsv(registerDate)},${escapeCsv(r.handler)},${escapeCsv(r.product)},${escapeCsv(r.period)},${escapeCsv(r.status)},,${escapeCsv(r.country)},${escapeCsv(r.customerName)},${escapeCsv(r.level)},,\n`;
  }
  const csvFile = `csv-reports/inquiry-report-${targetInquiry}-${ts}.csv`;
  fs.writeFileSync(csvFile, csv);
  console.log(`CSV 已保存到 ${csvFile}`);
  console.log(`\n业务员客户统计：\n${statsText}`);

  await browser.close().catch(() => {});
  if (titleCacheDirty) saveTitleCache(titleCache);
  if (chatProductsDirty) {
    saveChatProducts(chatProductsMap);
    console.log('  [聊天产品] 新发现已保存到 chat-products.json，可手动编辑补充产品类型');
  }
}

main().catch(e => console.error('Fatal:', e.message));
