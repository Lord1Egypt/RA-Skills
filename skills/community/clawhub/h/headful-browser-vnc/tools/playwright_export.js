const [,, wsPort, url, outDir] = process.argv;
(async ()=>{
  try {
    if(!wsPort || !url || !outDir){
      console.error('usage: node playwright_export.js <wsPort> <url> <outDir>');
      process.exit(2);
    }
    const { chromium } = require('playwright');
    const browser = await chromium.connectOverCDP(`http://127.0.0.1:${wsPort}`);
    const contexts = browser.contexts();
    const context = contexts.length ? contexts[0] : await browser.newContext({viewport:{width:1366,height:768}});
    const page = await context.newPage();
    await page.goto(url, {waitUntil:'networkidle', timeout:60000});
    await page.waitForTimeout(1000);
    try { await page.screenshot({path:`${outDir}/devtools_page.png`, fullPage:true}); } catch(e){}
    const content = await page.content();
    const fs = require('fs');
    fs.writeFileSync(`${outDir}/devtools_page.html`, content);
    fs.writeFileSync(`${outDir}/devtools_cookies.json`, JSON.stringify(await context.cookies(), null, 2));
    await browser.close();
    console.log('saved to', outDir);
    process.exit(0);
  } catch (err) {
    console.error('export error:', err && err.message ? err.message : err);
    process.exit(1);
  }
})();
