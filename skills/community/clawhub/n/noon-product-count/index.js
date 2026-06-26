const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

// 搜索单个关键词的商品数量
async function searchCount(keyword) {
  let browser;
  
  try {
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
    await new Promise(r => setTimeout(r, 10000));
    
    // 再搜索
    const encodedKeyword = encodeURIComponent(keyword.trim());
    const url = 'https://www.noon.com/saudi-ar/search/?q=' + encodedKeyword;
    
    console.log('   访问: ' + url);
    
    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: 90000
    });
    
    console.log('   等待加载...');
    await new Promise(r => setTimeout(r, 25000));
    
    // 获取页面文本
    const text = await page.evaluate(() => document.body.innerText);
    
    await browser.close();
    
    // 提取数量 - 格式: "1,572 نتائج البحث"
    const match = text.match(/([\d,]+)\s*نتائج/);
    if (match) {
      return match[1].replace(/,/g, '');
    }
    
    return '0';
    
  } catch (error) {
    if (browser) await browser.close();
    return '错误: ' + error.message;
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('用法: node index.js "阿语关键词"');
  console.error('示例: node index.js "سماعات بلوتوث"');
  console.error('批量: node index.js "سماعات" "بلوتوث"');
  process.exit(1);
}

async function main() {
  console.log('============================================================');
  console.log('🔍 Noon 商品数量统计');
  console.log('============================================================\n');
  
  for (const keyword of args) {
    console.log('关键词: ' + keyword);
    
    const count = await searchCount(keyword);
    console.log('📊 商品数量: ' + count);
    console.log('');
  }
}

main();
