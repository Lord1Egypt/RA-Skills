const { chromium } = require('playwright');

module.exports = async function(context, input) {
  const { url, action } = input;
  
  if (!url) {
    return { error: "Please provide a URL" };
  }

  console.log(`Launching browser to visit: ${url}`);
  
  const browser = await chromium.launch({ headless: true }); // 生产环境建议 headless: true
  const page = await browser.newPage();
  
  try {
    await page.goto(url, { waitUntil: 'networkidle' });
    
    let result = {};
    
    if (action === 'title' || !action) {
      result.title = await page.title();
      result.message = `Page title is: ${result.title}`;
    }
    
    if (action === 'screenshot') {
      const path = '/tmp/screenshot.png';
      await page.screenshot({ path: path });
      result.screenshot_path = path;
      result.message = "Screenshot taken successfully.";
    }

    return result;
    
  } catch (e) {
    return { error: e.message };
  } finally {
    await browser.close();
  }
};
