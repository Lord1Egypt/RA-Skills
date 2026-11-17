const { chromium } = require('playwright');
const { readFileSync, readdirSync, existsSync, mkdirSync } = require('fs');
const { join, dirname, basename } = require('path');

/**
 * Render social card posters from HTML to PNG
 * Usage: node render.mjs <task-dir> [--output <dir>]
 * 
 * Finds all .html files in task-dir, renders each .poster element to PNG
 */

async function render() {
  const args = process.argv.slice(2);
  const taskDir = args[0] || '.';
  const outputDir = args.includes('--output') 
    ? args[args.indexOf('--output') + 1] 
    : join(taskDir, 'output');

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Find all HTML files
  const htmlFiles = readdirSync(taskDir).filter(f => f.endsWith('.html'));
  
  if (htmlFiles.length === 0) {
    console.log('No HTML files found in', taskDir);
    await browser.close();
    return;
  }

  for (const htmlFile of htmlFiles) {
    const htmlPath = join(taskDir, htmlFile);
    const htmlContent = readFileSync(htmlPath, 'utf-8');
    
    console.log(`Rendering ${htmlFile}...`);
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    await page.setViewportSize({ width: 1200, height: 5000 });
    
    // Find all poster elements
    const posters = await page.locator('.poster').all();
    
    for (let i = 0; i < posters.length; i++) {
      const poster = posters[i];
      const box = await poster.boundingBox();
      
      if (!box) continue;
      
      // Get poster class for filename
      const classes = await poster.getAttribute('class');
      const posterType = classes.includes('xhs') ? 'xhs' 
        : classes.includes('square') ? 'square' 
        : classes.includes('wide') ? 'wide' : `${i+1}`;
      
      const pngName = basename(htmlFile, '.html') + `-${posterType}.png`;
      
      await page.screenshot({
        path: join(outputDir, pngName),
        clip: { x: box.x, y: box.y, width: box.width, height: box.height }
      });
      
      console.log(`  ✓ ${pngName} (${box.width}×${box.height})`);
    }
  }

  await browser.close();
  console.log(`\nDone! PNGs saved to ${outputDir}`);
}

render().catch(console.error);
