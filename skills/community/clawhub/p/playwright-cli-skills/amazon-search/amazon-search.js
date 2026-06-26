#!/usr/bin/env node

/**
 * Amazon Product Search Automation
 * Usage: node amazon-search.js "your search keyword"
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const keyword = process.argv[2];

if (!keyword) {
    console.error('❌ 错误：请提供搜索关键词');
    console.error('用法: node amazon-search.js "graduation party favor bags"');
    process.exit(1);
}

// 转换关键词用于文件名
const filenameKeyword = keyword.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9\-]/g, '');
const date = new Date().toISOString().split('T')[0];
const outputDir = path.join(process.env.HOME || '/tmp', 'amazon-search-project', 'data');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}
const outputFile = path.join(outputDir, `amazon-${filenameKeyword}-top10-${date}.csv`);

console.log(`🔍 开始搜索亚马逊商品: ${keyword}`);
console.log(`📁 输出文件: ${outputFile}`);

// JavaScript 代码用于提取数据
const extractScript = `
const products = Array.from(document.querySelectorAll('[data-component-type="s-search-result"]')).slice(0,10).map((el, i) => {
  const asin = el.getAttribute('data-asin');
  const title = el.querySelector('h2')?.textContent?.trim() || '';
  const priceEl = el.querySelector('.a-price .a-offscreen');
  const price = priceEl ? priceEl.textContent.trim() : '';
  const ratingEl = el.querySelector('[aria-label*="out of 5 stars"]');
  const rating = ratingEl ? ratingEl.getAttribute('aria-label').match(/[\\d.]+/)?.[0] : '';
  const reviewsEl = el.querySelector('a[href*="customerReviews"] span');
  const reviews = reviewsEl ? reviewsEl.textContent.replace(/[()]/g, '') : '';
  const img = el.querySelector('img')?.src || '';
  const salesInfo = el.querySelector('[aria-label*="bought in past month"]')?.textContent || '';
  
  return {
    rank: i+1,
    asin,
    title: title.replace(/,/g, ';').replace(/"/g, "'").substring(0,100),
    price,
    rating,
    reviews,
    salesInfo: salesInfo.replace(/,/g, ';'),
    img,
    link: asin ? 'https://www.amazon.com/dp/' + asin : ''
  };
});
JSON.stringify(products);
`;

try {
    // Step 1: 加载登录状态
    console.log('📋 Step 1: 加载登录状态...');
const authFile = path.join(process.env.HOME, 'amazon-search-project', 'amazon-auth.json');
    execSync(`playwright-cli state-load ${authFile}`, { 
        stdio: process.env.DEBUG ? 'inherit' : 'pipe',
        timeout: 30000 
    });

    // Step 2: 搜索商品
    console.log('🔎 Step 2: 搜索商品...');
    const encodedKeyword = encodeURIComponent(keyword).replace(/%20/g, '+');
    execSync(`playwright-cli goto "https://www.amazon.com/s?k=${encodedKeyword}&s=best-selling"`, {
        stdio: process.env.DEBUG ? 'inherit' : 'pipe',
        timeout: 60000
    });

    // Step 3: 等待页面加载
    console.log('⏳ Step 3: 等待页面加载...');
    execSync('sleep 3', { stdio: 'pipe' });

    // Step 4: 提取数据
    console.log('📊 Step 4: 提取商品数据...');
    const result = execSync(`playwright-cli eval "${extractScript}" --raw`, {
        encoding: 'utf8',
        timeout: 30000
    });

    // 解析 JSON 数据
    const lines = result.split('\n');
    let jsonData = null;
    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
            try {
                jsonData = JSON.parse(trimmed);
                break;
            } catch (e) {
                // 继续尝试下一行
            }
        }
    }

    if (!jsonData) {
        throw new Error('无法解析商品数据');
    }

    // 生成 CSV
    const csvHeader = '排名,商品名称,评分,评价数,价格,销量信息,图片URL,商品链接,ASIN';
    const csvRows = jsonData.map(p => {
        return `${p.rank},"${p.title}",${p.rating},${p.reviews},"${p.price}","${p.salesInfo}","${p.img}","${p.link}",${p.asin}`;
    });

    const csvContent = [csvHeader, ...csvRows].join('\n');
    fs.writeFileSync(outputFile, csvContent);

    console.log('');
    console.log(`✅ 完成！CSV 文件已生成: ${outputFile}`);
    console.log('');
    console.log('📊 数据预览（前5行）：');
    
    const preview = csvContent.split('\n').slice(0, 6);
    preview.forEach((line, i) => {
        if (i === 0) {
            console.log('\x1b[1m%s\x1b[0m', line); // 加粗表头
        } else {
            const cols = line.split(',');
            console.log(`${cols[0]}. ${cols[1].replace(/"/g, '').substring(0, 50)}... | ⭐${cols[2]} | 💰${cols[4]}`);
        }
    });

    console.log('');
    console.log(`📈 共提取 ${jsonData.length} 个商品`);

} catch (error) {
    console.error('❌ 错误:', error.message);
    if (error.stderr) {
        console.error('详细错误:', error.stderr.toString());
    }
    process.exit(1);
}
