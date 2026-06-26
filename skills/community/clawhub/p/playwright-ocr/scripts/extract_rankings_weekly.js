/**
 * Playwright 数据提取脚本 - 每周数据
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function extractData(config) {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });
    
    const page = await browser.newPage();
    const screenshots = [];
    
    console.log(`🌐 导航到：${config.url}`);
    await page.goto(config.url, {
        timeout: 90000,
        waitUntil: 'domcontentloaded'
    });
    
    console.log('⏳ 等待图表加载...');
    await page.waitForTimeout(10000);
    
    // 获取图表区域
    const chartInfo = await page.evaluate(() => {
        const svgs = document.querySelectorAll('svg');
        let chartSvg = null;
        let maxArea = 0;
        
        for (const svg of svgs) {
            const rect = svg.getBoundingClientRect();
            if (rect.width * rect.height > maxArea && rect.width > 200) {
                maxArea = rect.width * rect.height;
                chartSvg = svg;
            }
        }
        
        if (!chartSvg) return null;
        const rect = chartSvg.getBoundingClientRect();
        return { width: rect.width, height: rect.height, left: rect.left, top: rect.top };
    });
    
    if (!chartInfo) {
        console.log('❌ 未找到图表');
        await browser.close();
        return null;
    }
    
    console.log(`📊 图表区域：${chartInfo.width.toFixed(0)}x${chartInfo.height.toFixed(0)}`);
    
    // 更密集的悬停位置（每周数据）
    const positions = [];
    for (let i = 0; i <= 100; i += 2) {  // 每 2% 一个点，共 51 个点
        positions.push(i / 100);
    }
    
    console.log(`📍 悬停位置：${positions.length} 个`);
    
    for (let i = 0; i < positions.length; i++) {
        const offset = positions[i];
        const x = chartInfo.left + (chartInfo.width * offset);
        const y = chartInfo.top + (chartInfo.height * 0.3);
        
        // 悬停
        await page.mouse.move(x, y);
        await page.waitForTimeout(800);  // 缩短等待时间
        
        // 获取 Tooltip 文本
        const tooltipText = await page.evaluate(() => {
            const tooltip = document.querySelector('[class*="Tooltip"], [class*="tooltip"]');
            return tooltip?.textContent?.trim() || '';
        });
        
        if (tooltipText && tooltipText.length > 30) {
            screenshots.push({
                position: offset,
                tooltip: tooltipText
            });
            console.log(`  ✅ ${offset.toFixed(2)}: ${tooltipText.substring(0, 60)}...`);
        }
    }
    
    await browser.close();
    
    // 保存结果
    const resultPath = path.join(config.outputDir, 'rankings_weekly.json');
    fs.writeFileSync(resultPath, JSON.stringify({
        extraction_date: new Date().toISOString(),
        source_url: config.url,
        chart_info: chartInfo,
        screenshots: screenshots
    }, null, 2));
    
    console.log(`\n💾 结果已保存：${resultPath}`);
    console.log(`📸 有效截图：${screenshots.length} 个`);
    
    return { chart_info: chartInfo, screenshots };
}

// 主函数
const config = {
    url: process.env.TARGET_URL || 'https://openrouter.ai/rankings',
    outputDir: process.env.OUTPUT_DIR || '/root/.openclaw/workspace/skills/playwright_ocr/output',
};

// 创建输出目录
if (!fs.existsSync(config.outputDir)) {
    fs.mkdirSync(config.outputDir, { recursive: true });
}

console.log('=' .repeat(60));
console.log('🤖 Playwright_OCR 周数据提取');
console.log('=' .repeat(60));

extractData(config).catch(console.error);
