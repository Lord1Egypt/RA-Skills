/**
 * 补充缺失的周数据
 */
const { chromium } = require('playwright');
const fs = require('fs');

// 缺失的日期
const missingDates = [
    'March 24, 2025', 'March 31, 2025', 'May 5, 2025',
    'June 2, 2025', 'June 9, 2025', 'July 7, 2025',
    'July 14, 2025', 'August 4, 2025', 'September 1, 2025',
    'September 8, 2025', 'September 22, 2025', 'October 6, 2025',
    'November 3, 2025', 'December 1, 2025', 'December 8, 2025',
    'December 15, 2025', 'January 5, 2026', 'February 2, 2026',
    'February 9, 2026', 'March 2, 2026'
];

async function fillMissingData() {
    const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    console.log('🌐 导航到 Rankings 页面...');
    await page.goto('https://openrouter.ai/rankings', { timeout: 90000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(10000);
    
    const collected = [];
    
    // 更密集的悬停
    const chartInfo = await page.evaluate(() => {
        const svgs = document.querySelectorAll('svg');
        let chart = null, maxArea = 0;
        for (const svg of svgs) {
            const rect = svg.getBoundingClientRect();
            if (rect.width * rect.height > maxArea && rect.width > 200) {
                maxArea = rect.width * rect.height;
                chart = svg;
            }
        }
        if (!chart) return null;
        const rect = chart.getBoundingClientRect();
        return { width: rect.width, height: rect.height, left: rect.left, top: rect.top };
    });
    
    if (!chartInfo) {
        console.log('❌ 未找到图表');
        await browser.close();
        return;
    }
    
    console.log(`📊 图表：${chartInfo.width}x${chartInfo.height}`);
    
    // 更密集的采样（每 1% 一个点）
    for (let i = 0; i <= 100; i++) {
        const x = chartInfo.left + (chartInfo.width * (i / 100));
        const y = chartInfo.top + (chartInfo.height * 0.3);
        
        await page.mouse.move(x, y);
        await page.waitForTimeout(500);
        
        const tooltip = await page.evaluate(() => {
            const el = document.querySelector('[class*="Tooltip"], [class*="tooltip"]');
            return el?.textContent?.trim() || '';
        });
        
        if (tooltip && tooltip.length > 30) {
            collected.push({ position: i/100, tooltip });
        }
    }
    
    await browser.close();
    
    // 保存
    fs.writeFileSync('/root/.openclaw/workspace/skills/playwright_ocr/output/missing_weeks.json', 
        JSON.stringify({ collected }, null, 2));
    
    console.log(`✅ 采集完成：${collected.length} 个数据点`);
}

fillMissingData().catch(console.error);
