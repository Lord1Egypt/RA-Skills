const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function scrape() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 800 });
  
  const keyword = 'لغز ممغنط';
  const url = 'https://www.noon.com/saudi-ar/search/?q=' + encodeURIComponent(keyword);
  
  console.log('Loading:', url);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  
  await new Promise(r => setTimeout(r, 8000));
  
  // Scroll
  for (let i = 0; i < 5; i++) {
    await page.evaluate(() => window.scrollBy(0, 500));
    await new Promise(r => setTimeout(r, 1000));
  }
  
  const products = await page.evaluate(() => {
    const results = [];
    // Try multiple selectors
    const els = document.querySelectorAll('[data-qa*="plp-product"], .ProductCard, .productCard, .product-card');
    
    els.forEach(el => {
      try {
        // Try to get title from various sources
        let title = '';
        const img = el.querySelector('img');
        if (img) {
          title = img.getAttribute('alt') || img.getAttribute('title') || '';
        }
        if (!title) {
          const titleEl = el.querySelector('[data-qa*="productTitle"]');
          if (titleEl) title = titleEl.innerText || '';
        }
        
        if (!title || title.length < 3) return;
        
        const txt = el.innerText || '';
        const price = txt.match(/(\d+[\d,]*)\s*ر\.س/i)?.[1] || 'N/A';
        const rating = txt.match(/(\d\.\d)/)?.[1] || 'N/A';
        const reviews = txt.match(/\((\d+[\d,]*K?)\)/)?.[1] || '0';
        
        results.push({ title: title.trim(), price, rating, reviews });
      } catch(e) {}
    });
    
    return results;
  });
  
  console.log('Found:', products.length);
  console.log(JSON.stringify(products, null, 2));
  
  await browser.close();
}

scrape().catch(console.error);
