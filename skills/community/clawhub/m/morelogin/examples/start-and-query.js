/**
 * Start the specified MoreLogin configuration file and query the BTC price
 */

const puppeteer = require('puppeteer-core');
const http = require('http');

//Start configuration file
async function startProfile(profileId) {
  console.log(`🚀 Start profile: ${profileId}\n`);
  
  return new Promise((resolve) => {
    const data = JSON.stringify({ profileId: profileId });
    
    const req = http.request({
      hostname: '127.0.0.1',
      port: 40000,
      path: '/api/env/start',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        let parsed = null;
        try {
          parsed = JSON.parse(body);
        } catch (e) {
          parsed = null;
        }
        const profileData = parsed && parsed.data ? parsed.data : {};
        resolve({ 
          statusCode: res.statusCode, 
          body: body.substring(0, 1000),
          success: res.statusCode === 200 && parsed && parsed.code === 0,
          debugPort: profileData.debugPort || profileData.port || null
        });
      });
    });
    
    req.on('error', (e) => resolve({ error: e.message }));
    req.setTimeout(15000, () => {
      req.destroy();
      resolve({ timeout: true });
    });
    
    req.write(data);
    req.end();
  });
}

// Query BTC price
async function getBTCPrice(cdpPort) {
  console.log(`\n🔍 Connect to CDP port: ${cdpPort}\n`);
  
  let browser;
  
  try {
    browser = await puppeteer.connect({
      browserURL: `http://localhost:${cdpPort}`,
      defaultViewport: null
    });
    
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
    
    console.log('🌐 Visit Google to search BTC price...');
    
    await page.goto('https://www.google.com/search?q=BTC+price+USD', {
      waitUntil: 'domcontentloaded',
      timeout: 20000
    }).catch(() => {});
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    console.log('📸 Save screenshot...');
    const screenshotPath = `/Users/kxc/.openclaw/workspace/skills/morelogin/btc-price-${Date.now()}.png`;
    await page.screenshot({ path: screenshotPath, fullPage: false });
    
    const priceData = await page.evaluate(() => {
      const bodyText = document.body.innerText;
      const priceMatch = bodyText.match(/Bitcoin\s*([\d,]+\.\d+)\s*USD/);
      const changeMatch = bodyText.match(/([+\-][\d,]+\.?\d*)\s*\(([\+\-]?[\d.]+%)\)/);
      
      return {
        price: priceMatch ? priceMatch[1] : null,
        change: changeMatch ? changeMatch[1] : null,
        changePercent: changeMatch ? changeMatch[2] : null,
        title: document.title
      };
    });
    
    await page.close();
    
    console.log('\n═══════════════════════════════════════════');
    console.log(' 📊 BTC price query results');
    console.log('═══════════════════════════════════════════');
    
    if (priceData.price) {
      console.log(`💰 BTC price: $${priceData.price} USD`);
      if (priceData.change) {
        console.log(`📈 Change: ${priceData.change} (${priceData.changePercent})`);
      }
    } else {
      console.log('⚠️ Please check the screenshot for price information');
    }
    
    console.log('───────────────────────────────────────────');
    console.log(`📸 Screenshot: ${screenshotPath}`);
    console.log('═══════════════════════════════════════════\n');
    
    return {
      success: true,
      price: priceData.price,
      change: priceData.change,
      changePercent: priceData.changePercent,
      screenshot: screenshotPath
    };
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    return { success: false, error: error.message };
  }
}

// main function
async function main() {
  const profileId = process.argv[2] || '2016127261952372736';
  
  console.log('═══════════════════════════════════════════');
  console.log('MoreLogin BTC price query');
  console.log('═══════════════════════════════════════════\n');
  
  //Try to start the configuration file
  const startResult = await startProfile(profileId);
  console.log('Start result:', startResult);
  
  console.log('\n⏳ Waiting for the configuration file to start...\n');
  await new Promise(resolve => setTimeout(resolve, 10000));
  
  const cdpPort = startResult.debugPort;
  
  if (!cdpPort) {
    console.log('⚠️ CDP port not returned by API, use fallback port 59840\n');
  }
  
  // Query BTC price
  const result = await getBTCPrice(cdpPort || '59840');
  
  console.log('Final result:', JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}

main();
