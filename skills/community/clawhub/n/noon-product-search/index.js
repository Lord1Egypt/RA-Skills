const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function scrapeNoon(keyword) {
  let browser;
  
  try {
    console.log('🔌 启动浏览器...');
    browser = await puppeteer.launch({
      headless: false,
      args: ['--disable-blink-features=AutomationControlled']
    });
    
    const page = await browser.newPage();
    
    // 先访问主页初始化 session
    console.log('   初始化 session...');
    await page.goto('https://www.noon.com/saudi-ar/', {
      waitUntil: 'domcontentloaded',
      timeout: 90000
    });
    await new Promise(r => setTimeout(r, 8000));
    
    // 搜索
    const url = 'https://www.noon.com/saudi-ar/search/?q=' + encodeURIComponent(keyword.trim());
    console.log('🌐 访问: ' + url);
    
    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: 90000
    });
    
    console.log('⏳ 等待加载...');
    await new Promise(r => setTimeout(r, 25000));
    
    // 点击加载更多按钮
    console.log('   点击加载更多...');
    for (let c = 0; c < 10; c++) {
      try {
        await page.evaluate(() => {
          document.querySelectorAll('button').forEach(b => {
            const text = b.innerText || '';
            if (text.includes('المزيد') || text.includes('more')) {
              b.click();
            }
          });
        });
        await new Promise(r => setTimeout(r, 2000));
      } catch (e) {}
    }
    
    // 滚动加载更多
    console.log('   滚动加载...');
    for (let i = 0; i < 60; i++) {
      await page.evaluate(() => window.scrollBy(0, 600));
      await new Promise(r => setTimeout(r, 600));
    }
    
    await new Promise(r => setTimeout(r, 3000));
    
    // 获取商品数据
    const products = await page.evaluate(() => {
      let prods = [];
      
      // noon 商品容器选择器
      const selectors = [
        '[data-qa*="plp-product"]',
        '[class*="ProductCard"]',
        '[class*="productCard"]'
      ];
      
      let containers = [];
      for (let sel of selectors) {
        containers = document.querySelectorAll(sel);
        if (containers.length > 0) break;
      }
      
      console.log('   找到容器:', containers.length);
      
      containers.forEach(el => {
        try {
          const txt = el.innerText || '';
          
          // 标题 - 从 data-qa 属性获取
          let title = '';
          const titleEl = el.querySelector('[data-qa*="productImagePLP"]');
          if (titleEl) {
            title = titleEl.getAttribute('data-qa') || '';
            title = title.replace('productImagePLP_', '').trim();
          }
          
          if (!title || title.length < 5) return;
          
          // 评分
          let rating = 'N/A';
          const ratingMatch = txt.match(/(\d\.\d)/);
          if (ratingMatch) rating = ratingMatch[1];
          
          // 评价数
          let reviews = 'N/A';
          const reviewsMatch = txt.match(/(\d+[\d,]*[Kk]?)\s*\)?/);
          if (reviewsMatch) reviews = reviewsMatch[1];
          
          // 价格
          let price = 'N/A';
          const priceEl = el.querySelector('[class*="price"], [class*="Price"], [class*="PriceValue"]');
          if (priceEl) {
            const pt = priceEl.innerText || '';
            const pm = pt.match(/(\d+)/);
            if (pm) price = pm[1] + ' ر.س';
          }
          
          // 备选：从文本找价格
          if (price === 'N/A') {
            const priceText = txt.replace(/\n/g, ' ');
            const pms = priceText.match(/(\d+)\s*ر\.س/i);
            if (pms) price = pms[1] + ' ر.س';
          }
          
          prods.push({ title, rating, reviews, price });
        } catch (e) {}
      });
      
      return prods;
    });
    
    await browser.close();
    
    // 去重
    const seen = new Set();
    const unique = products.filter(p => {
      const key = p.title.substring(0, 30);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
    
    return unique.slice(0, 60);
    
  } catch (error) {
    if (browser) await browser.close();
    throw error;
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('用法: node index.js "阿语关键词"');
  console.error('示例: node index.js "عربة تسوق"');
  process.exit(1);
}

async function main() {
  const keyword = args[0];
  
  console.log('============================================================');
  console.log('🔍 搜索: "' + keyword + '"');
  console.log('============================================================\n');
  
  try {
    const products = await scrapeNoon(keyword);
    
    if (!products || products.length === 0) {
      console.log('⚠️ 未找到商品');
      process.exit(1);
    }
    
    console.log('\n📦 共 ' + products.length + ' 个商品\n');
    
    products.forEach(function(p, i) {
      console.log('📦 商品 ' + (i + 1));
      console.log('   标题: ' + p.title.substring(0, 70) + (p.title.length > 70 ? '...' : ''));
      console.log('   评分: ' + p.rating);
      console.log('   评价数: ' + (p.reviews === 'N/A' ? 'N/A' : '(' + p.reviews + ')'));
      console.log('   价格: ' + p.price);
      console.log('');
    });
    
  } catch (error) {
    console.error('❌ 错误: ' + error.message);
    process.exit(1);
  }
}

main();
