/**
 * 中华传统诗词格律校验脚本（搜韵网版）
 * 
 * 功能：
 *   - 诗词格律校验（近体诗）→ sou-yun.cn/AnalyzePoem.aspx
 *   - 词牌格律校验（宋词）→ sou-yun.cn/AnalyzeCi.aspx
 *   - 自动识别体裁并选择对应校验页面
 *   - 提取校验结果并格式化输出
 * 
 * 用法：
 *   node check_ge_lu.js --type poem --text "床前明月光..."
 *   node check_ge_lu.js --type ci --cipai "卜算子" --text "桃萼绽初红..."
 *   node check_ge_lu.js --auto --text "桃萼绽初红，绿柳垂丝袅..."
 * 
 * 依赖：需要安装 playwright
 *   npm init -y && npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');

// Parse command line arguments
function parseArgs(args) {
  const result = { type: null, text: '', cipai: '', rhyme: '' };
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--type': result.type = args[++i]; break;
      case '--text': result.text = args[++i]; break;
      case '--cipai': result.cipai = args[++i]; break;
      case '--rhyme': result.rhyme = args[++i]; break;
      case '--auto': result.type = 'auto'; break;
    }
  }
  return result;
}

/**
 * Auto-detect poem type from text
 * Returns 'poem' or 'ci'
 */
function detectType(text) {
  // Ci indicators: mixed line lengths, typical ci patterns
  const lines = text.replace(/[，。、！？；：\n\r]/g, ' ').trim().split(/\s+/).filter(l => l.length > 0);
  
  // Check if all lines are 5 or 7 chars (likely 近体诗/古体诗)
  const allSameLength = lines.every(l => l.length === 5 || l.length === 7);
  if (allSameLength && (lines.length === 4 || lines.length === 8)) {
    return 'poem';
  }
  
  // Check for mixed lengths (typical of ci)
  const lengths = new Set(lines.map(l => l.length));
  if (lengths.size > 1) {
    return 'ci';
  }
  
  // Default to ci if uncertain (has title keywords)
  return 'ci';
}

/**
 * 校验律诗/绝句
 */
async function checkPoem(browser, text, rhyme) {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://sou-yun.cn/AnalyzePoem.aspx', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Wait for textarea
    const textarea = await page.waitForSelector('textarea', { timeout: 10000 });
    if (!textarea) throw new Error('无法找到输入框');
    
    // Clear and fill textarea
    await textarea.click({ clickCount: 3 });
    await textarea.fill(text);
    
    // If rhyme specified, try to select it
    if (rhyme) {
      // Look for rhyme selector
      const rhymeSelect = await page.$('select');
      if (rhymeSelect) {
        await rhymeSelect.selectOption({ label: rhyme });
      }
    }
    
    // Find and click submit button
    const submitBtn = await page.$('input[type="submit"], button[type="submit"]');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      // Try clicking by text
      await page.click('text=校验').catch(() => {
        // Try Enter key as fallback
        return textarea.press('Enter');
      });
    }
    
    // Wait for results
    await page.waitForTimeout(3000);
    
    // Extract results
    const resultText = await page.evaluate(() => {
      // Try to find result area
      const resultElements = document.querySelectorAll('.result, #result, .analysis, table');
      let text = '';
      resultElements.forEach(el => {
        text += el.innerText + '\n';
      });
      
      // Fallback: get main content
      if (!text) {
        const body = document.body.innerText;
        // Extract relevant portion
        const idx = body.indexOf('平仄');
        if (idx > -1) {
          text = body.substring(Math.max(0, idx - 100), idx + 2000);
        }
      }
      
      return text || '未能提取校验结果，请手动访问页面查看。';
    });
    
    return {
      success: true,
      url: page.url(),
      result: resultText,
      manualUrl: 'https://sou-yun.cn/AnalyzePoem.aspx'
    };
    
  } catch (error) {
    return {
      success: false,
      error: error.message,
      manualUrl: 'https://sou-yun.cn/AnalyzePoem.aspx',
      tip: '自动化校验失败，建议手动访问上方链接进行校验。'
    };
  } finally {
    await page.close();
  }
}

/**
 * 校验词牌格律
 */
async function checkCi(browser, text, cipai, rhyme) {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://sou-yun.cn/AnalyzeCi.aspx', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Wait for page to load
    await page.waitForTimeout(2000);
    
    // Step 1: Select cipai (词牌) - usually a dropdown or searchable
    // Try to find and fill the cipai input
    const cipaiInput = await page.$('input[id*="cipai"], input[id*="CiPai"], input[placeholder*="词牌"]');
    if (cipaiInput && cipai) {
      await cipaiInput.click({ clickCount: 3 });
      await cipaiInput.fill(cipai);
      await page.waitForTimeout(500);
      
      // Try to select from dropdown
      const firstOption = await page.$('text=' + cipai);
      if (firstOption) {
        await firstOption.click();
        await page.waitForTimeout(1000);
      }
    }
    
    // Step 2: Fill in the poem text
    const textarea = await page.$('textarea');
    if (textarea) {
      await textarea.click({ clickCount: 3 });
      await textarea.fill(text);
    } else {
      throw new Error('无法找到文本输入框');
    }
    
    // Step 3: Click submit
    const submitBtn = await page.$('input[type="submit"], button[type="submit"]');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      await page.click('text=校验').catch(() => {});
    }
    
    // Wait for results
    await page.waitForTimeout(3000);
    
    // Extract results
    const resultText = await page.evaluate(() => {
      const resultElements = document.querySelectorAll('.result, #result, .analysis, table');
      let text = '';
      resultElements.forEach(el => {
        text += el.innerText + '\n';
      });
      
      if (!text) {
        const body = document.body.innerText;
        const idx = body.indexOf('平仄');
        if (idx > -1) {
          text = body.substring(Math.max(0, idx - 100), idx + 2000);
        }
      }
      
      return text || '未能提取校验结果，请手动访问页面查看。';
    });
    
    return {
      success: true,
      url: page.url(),
      result: resultText,
      manualUrl: 'https://sou-yun.cn/AnalyzeCi.aspx'
    };
    
  } catch (error) {
    return {
      success: false,
      error: error.message,
      manualUrl: 'https://sou-yun.cn/AnalyzeCi.aspx',
      tip: '自动化校验失败，建议手动访问上方链接进行校验。'
    };
  } finally {
    await page.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  if (!args.text || !args.type) {
    console.log('用法:');
    console.log('  node check_ge_lu.js --type poem --text "诗句内容"');
    console.log('  node check_ge_lu.js --type ci --cipai "词牌名" --text "词作内容"');
    console.log('  node check_ge_lu.js --auto --text "诗词内容(自动识别)"');
    console.log('');
    console.log('参数:');
    console.log('  --type     体裁: poem(诗) | ci(词) | auto(自动识别)');
    console.log('  --text     诗词内容');
    console.log('  --cipai    词牌名(仅ci类型需要)');
    console.log('  --rhyme    韵书(可选): 平水韵 | 词林正韵 | 中华通韵');
    process.exit(1);
  }
  
  let type = args.type;
  if (type === 'auto') {
    type = detectType(args.text);
    console.log(`[自动识别] 判定为: ${type === 'poem' ? '诗' : '词'}`);
  }
  
  console.log(`[校验中] 体裁: ${type === 'poem' ? '诗' : '词'}`);
  if (args.cipai) console.log(`[校验中] 词牌: ${args.cipai}`);
  
  const browser = await chromium.launch({ headless: true });
  
  try {
    let result;
    if (type === 'poem') {
      result = await checkPoem(browser, args.text, args.rhyme);
    } else {
      result = await checkCi(browser, args.text, args.cipai, args.rhyme);
    }
    
    if (result.success) {
      console.log('\n=== 校验结果 ===\n');
      console.log(result.result);
    } else {
      console.log('\n[自动化失败]', result.error);
      if (result.tip) console.log(result.tip);
    }
    console.log('\n[手动校验]', result.manualUrl);
    
  } finally {
    await browser.close();
  }
}

main().catch(console.error);
