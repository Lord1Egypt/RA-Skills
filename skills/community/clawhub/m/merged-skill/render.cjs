const { chromium } = require('playwright');
const { readFileSync } = require('fs');
const { join, dirname } = require('path');

async function render() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const htmlPath = join(__dirname, 'xian-pro.html');
  const htmlContent = readFileSync(htmlPath, 'utf-8');
  
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.setViewportSize({ width: 1200, height: 5000 });
  
  // Render poster 1
  const poster1 = await page.locator('#poster-1').boundingBox();
  await page.screenshot({
    path: join(__dirname, 'posters', 'poster-1-xian-forest.png'),
    clip: { x: poster1.x, y: poster1.y, width: 1080, height: 1440 }
  });
  console.log('✓ poster-1-xian-forest.png');
  
  // Render poster 2
  const poster2 = await page.locator('#poster-2').boundingBox();
  await page.screenshot({
    path: join(__dirname, 'posters', 'poster-2-xingcheng-blue.png'),
    clip: { x: poster2.x, y: poster2.y, width: 1080, height: 1440 }
  });
  console.log('✓ poster-2-xingcheng-blue.png');
  
  // Render poster 3
  const poster3 = await page.locator('#poster-3').boundingBox();
  await page.screenshot({
    path: join(__dirname, 'posters', 'poster-3-studio-pink.png'),
    clip: { x: poster3.x, y: poster3.y, width: 1080, height: 1440 }
  });
  console.log('✓ poster-3-studio-pink.png');
  
  await browser.close();
  console.log('\nDone! PNGs saved to posters/');
}

render().catch(console.error);
