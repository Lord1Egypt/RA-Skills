/**
 * Playwright 数据提取脚本 v2.0 - 质量增强版
 * 自动打开网页，悬停图表，截取数据，包含日期验证和 Total 核对
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function extractData(config) {
    const startTime = Date.now();
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });
    
    const page = await browser.newPage();
    const screenshots = [];
    const qualityReport = {
        totalSamples: 0,
        validDates: [],
        invalidDates: [],
        totalValues: [],
        screenshotSizes: []
    };
    
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
    
    // 计算目标日期（前一天）
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const targetDate = yesterday.toISOString().split('T')[0]; // YYYY-MM-DD
    
    // 格式化目标日期为英文格式用于匹配
    const targetDateEn = yesterday.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    console.log(`📅 目标日期：${targetDate} (${targetDateEn})`);
    
    // 悬停位置 - 增加采样密度（间隔≤0.01）
    const positions = config.positions || [
        0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 
        0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.92, 
        0.94, 0.95, 0.96, 0.97, 0.98, 0.99
    ];
    
    qualityReport.totalSamples = positions.length;
    
    // 扩大截图范围：包含日期标签和坐标轴（最小 600x800）
    const screenshotWidth = Math.max(600, chartInfo.width * 0.8);
    const screenshotHeight = Math.max(800, chartInfo.height * 0.6);
    
    for (let i = 0; i < positions.length; i++) {
        const offset = positions[i];
        const x = chartInfo.left + (chartInfo.width * offset);
        const y = chartInfo.top + (chartInfo.height * 0.3);
        
        // 悬停
        await page.mouse.move(x, y);
        await page.waitForTimeout(1500);
        
        // 扩大截图范围 - 确保包含日期标签
        const screenshotPath = path.join(config.outputDir, `hover_${i}.png`);
        const clipX = Math.max(0, x - screenshotWidth / 2);
        const clipY = Math.max(0, chartInfo.top - screenshotHeight * 0.3);
        const clipWidth = Math.min(screenshotWidth, config.pageWidth - clipX);
        const clipHeight = Math.min(screenshotHeight, config.pageHeight - clipY);
        
        await page.screenshot({
            path: screenshotPath,
            clip: { 
                x: clipX, 
                y: clipY, 
                width: clipWidth, 
                height: clipHeight 
            }
        });
        
        qualityReport.screenshotSizes.push({
            position: offset,
            size: `${clipWidth}x${clipHeight}`
        });
        
        // 获取 Tooltip 文本
        const tooltipText = await page.evaluate(() => {
            const tooltip = document.querySelector('[class*="Tooltip"], [class*="tooltip"]');
            return tooltip?.textContent?.trim() || '';
        });
        
        // 提取日期和 Total 值进行验证
        let extractedDate = null;
        let totalValue = null;
        
        if (tooltipText) {
            // 提取日期（支持 "March 19, 2026" 格式）
            const dateMatch = tooltipText.match(/(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}/);
            if (dateMatch) {
                extractedDate = dateMatch[0];
                qualityReport.validDates.push({ position: offset, date: extractedDate });
            }
            
            // 提取 Total 值
            const totalMatch = tooltipText.match(/Total\s+([\d.]+)B/);
            if (totalMatch) {
                totalValue = parseFloat(totalMatch[1]);
                qualityReport.totalValues.push({ position: offset, total: totalValue });
            }
        }
        
        screenshots.push({
            position: offset,
            screenshot: screenshotPath,
            tooltip: tooltipText,
            extractedDate: extractedDate,
            totalValue: totalValue,
            isTargetDate: extractedDate === targetDateEn
        });
        
        const statusIcon = extractedDate === targetDateEn ? '🎯' : '✅';
        console.log(`${statusIcon} 位置 ${offset.toFixed(2)}: ${extractedDate || '无日期'} | Total: ${totalValue || 'N/A'}B`);
    }
    
    await browser.close();
    
    // 验证：检查是否采集到目标日期
    const targetDateSamples = screenshots.filter(s => s.isTargetDate);
    const hasTargetDate = targetDateSamples.length > 0;
    
    if (!hasTargetDate) {
        console.log(`⚠️  警告：未找到目标日期 ${targetDateEn} 的数据`);
        console.log(`   采集到的日期：${[...new Set(screenshots.map(s => s.extractedDate).filter(Boolean))]}`);
    }
    
    // 验证：检查 Total 值一致性
    const uniqueTotals = [...new Set(qualityReport.totalValues.map(v => v.total))];
    if (uniqueTotals.length > 1) {
        console.log(`⚠️  警告：Total 值不一致 (${uniqueTotals.length} 个不同值)`);
    }
    
    // 保存结果
    const resultPath = path.join(config.outputDir, 'extraction_result.json');
    const result = {
        extraction_date: new Date().toISOString(),
        source_url: config.url,
        chart_info: chartInfo,
        target_date: targetDate,
        target_date_en: targetDateEn,
        has_target_date: hasTargetDate,
        screenshots: screenshots,
        quality_report: {
            ...qualityReport,
            targetDateFound: hasTargetDate,
            uniqueTotalValues: uniqueTotals,
            executionTimeMs: Date.now() - startTime
        }
    };
    fs.writeFileSync(resultPath, JSON.stringify(result, null, 2));
    
    // 生成 CSV 数据（供上传脚本使用）
    const csvData = [];
    for (const sample of screenshots) {
        if (sample.tooltip && sample.isTargetDate) {
            // 解析 tooltip 数据 - 改进的正则表达式
            // 格式：模型名 + 数字+B，如 "Claude Sonnet 4.639.5B"
            const tooltip = sample.tooltip;
            
            // 先移除日期、Total、Daily Pace 等非模型数据
            let cleaned = tooltip.replace(/^[A-Za-z]+\s+\d{1,2},\s+\d{4}/, ''); // 移除日期
            cleaned = cleaned.replace(/Total\s+[\d.]+B/, ''); // 移除 Total
            cleaned = cleaned.replace(/Daily\s+Pace.*$/, ''); // 移除 Daily Pace
            
            // 解析模型和数据：模型名 + 数字+B
            // 关键改进：模型名可能包含数字（如 4.5, M2.5），需要更精确的匹配
            const modelPattern = /([A-Za-z][A-Za-z0-9\s\-\.\(\)]*?)\s+([\d.]+)B/g;
            let match;
            const foundModels = new Set(); // 去重
            
            while ((match = modelPattern.exec(cleaned)) !== null) {
                let modelName = match[1].trim();
                const tokens = (parseFloat(match[2]) * 1000000000).toFixed(0);
                
                // 清理模型名（移除末尾的年份数字等）
                modelName = modelName.replace(/\d{4}\s*$/, '').trim();
                
                // 跳过无效数据
                if (!modelName || modelName.length < 2 || foundModels.has(modelName)) {
                    continue;
                }
                
                foundModels.add(modelName);
                csvData.push({
                    date: sample.extractedDate || targetDateEn,
                    model: modelName,
                    tokens: tokens
                });
            }
        }
    }
    
    // 保存 CSV
    const csvPath = path.join(config.outputDir, 'extracted_data.csv');
    const csvContent = 'date,model,tokens\n' + 
        csvData.map(row => `"${row.date}","${row.model}",${row.tokens}`).join('\n');
    fs.writeFileSync(csvPath, csvContent);
    
    console.log(`\n💾 结果已保存：${resultPath}`);
    console.log(`📄 CSV 数据：${csvPath}`);
    console.log(`📸 截图数量：${screenshots.length}`);
    console.log(`🎯 目标日期数据：${targetDateSamples.length} 条`);
    console.log(`⏱️  执行时间：${((Date.now() - startTime) / 1000).toFixed(1)}秒`);
    
    return { 
        chart_info: chartInfo, 
        screenshots,
        quality_report: result.quality_report
    };
}

// 主函数
const config = {
    url: process.env.TARGET_URL || 'https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F',
    outputDir: process.env.OUTPUT_DIR || '/root/.openclaw/workspace/skills/playwright_ocr/output',
    positions: [
        0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 
        0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.92, 
        0.94, 0.95, 0.96, 0.97, 0.98, 0.99
    ],
    pageWidth: 1920,  // 页面宽度
    pageHeight: 1080   // 页面高度
};

// 创建输出目录
if (!fs.existsSync(config.outputDir)) {
    fs.mkdirSync(config.outputDir, { recursive: true });
}

console.log('=' .repeat(60));
console.log('🤖 Playwright_OCR 数据提取 v2.0 - 质量增强版');
console.log('=' .repeat(60));

extractData(config).catch(console.error);
