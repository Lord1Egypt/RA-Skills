const CDP = require('chrome-remote-interface');

(async () => {
  const client = await CDP({ port: 9222 });
  const { Page, Runtime } = client;

  try {
    await Page.enable();
    
    const keyword = 'لغز ممغنط';
    const url = 'https://www.noon.com/saudi-ar/search/?q=' + encodeURIComponent(keyword);
    
    console.log('Navigating to:', url);
    await Page.navigate({ url });
    
    console.log('Waiting for load...');
    await Page.loadEventFired();
    
    // Wait for content
    await new Promise(r => setTimeout(r, 15000));
    
    // Scroll to load more
    console.log('Scrolling...');
    for (let i = 0; i < 10; i++) {
      await Runtime.evaluate({ expression: 'window.scrollBy(0, 800)' });
      await new Promise(r => setTimeout(r, 1000));
    }
    
    // Get product info
    const result = await Runtime.evaluate({
      expression: `
        (() => {
          const products = [];
          const containers = document.querySelectorAll('[data-qa*="plp-product"], .ProductCard, [class*="productCard"]');
          console.log('Found containers:', containers.length);
          
          containers.forEach((el, i) => {
            try {
              const titleEl = el.querySelector('[data-qa*="productImagePLP"]');
              let title = titleEl ? titleEl.getAttribute('data-qa') || '' : '';
              title = title.replace('productImagePLP_', '').trim();
              
              if (!title || title.length < 3) return;
              
              const txt = el.innerText || '';
              let rating = txt.match(/(\d\.\d)/)?.[1] || 'N/A';
              let reviews = txt.match(/(\d+[\d,]*K?)/)?.[1] || 'N/A';
              let price = txt.match(/(\d+)\s*ر\.س/i)?.[1] || 'N/A';
              if (price !== 'N/A') price += ' ر.س';
              
              products.push({ title, rating, reviews, price });
            } catch(e) {}
          });
          
          return products;
        })()
      `
    });
    
    console.log('\n=== PRODUCTS ===');
    console.log(JSON.stringify(result.result.value, null, 2));
    
  } catch (e) {
    console.error('Error:', e.message);
  } finally {
    await client.close();
  }
})();
