const { chromium } = require('playwright');
const { readFileSync, existsSync, mkdirSync } = require('fs');
const { join, dirname, basename } = require('path');

async function render() {
  const htmlFile = process.argv[2];
  if (!htmlFile) {
    console.log('Usage: node render.mjs <html-file>');
    process.exit(1);
  }

  const htmlPath = join(process.cwd(), htmlFile);
  const outputDir = join(process.cwd(), 'output');
  
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const htmlContent = readFileSync(htmlPath, 'utf-8');
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.setViewportSize({ width: 1200, height: 5000 });
  
  const posters = await page.locator('.poster').all();
  const baseName = basename(htmlFile, '.html');
  
  for (let i = 0; i < posters.length; i++) {
    const poster = posters[i];
    const box = await poster.boundingBox();
    if (!box) continue;
    
    const classes = await poster.getAttribute('class') || '';
    let suffix = `${i + 1}`;
    if (classes.includes('xhs')) suffix = 'xhs';
    else if (classes.includes('square')) suffix = 'square';
    else if (classes.includes('wide')) suffix = 'wide';
    
    const pngName = `${baseName}-${suffix}.png`;
    
    await page.screenshot({
      path: join(outputDir, pngName),
      clip: { x: box.x, y: box.y, width: box.width, height: box.height }
    });
    
    console.log(`✓ ${pngName} (${box.width}×${box.height})`);
  }

  await browser.close();
  console.log(`\nDone! Saved to ${outputDir}`);
}

render().catch(console.error);
