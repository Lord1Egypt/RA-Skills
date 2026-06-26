#!/usr/bin/env node

/**
 * 获取每日新闻列表
 * 用法：node get-daily.js [date]
 * 示例：node get-daily.js 2026-03-10
 */

const https = require('https');

function getDailyNews(date = null) {
  // 如果没有传入日期，使用当前日期
  if (!date) {
    const now = new Date();
    date = now.toISOString().split('T')[0];
  }

  // 验证日期格式
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(date)) {
    console.error('❌ 日期格式错误，请使用 YYYY-MM-DD 格式（如：2026-03-10）');
    process.exit(1);
  }

  const url = `https://api.cjiot.cc/api/v1/daily?date=${date}`;

  https.get(url, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      try {
        const result = JSON.parse(data);
        
        if (result.code !== 200) {
          console.error(`❌ API 返回错误：${result.message || '未知错误'}`);
          process.exit(1);
        }

        const newsData = result.data;
        
        console.log(`\n📰 ${newsData.date} 每日新闻摘要\n`);
        console.log(`📋 共 ${newsData.article_count} 条新闻\n`);
        console.log('━'.repeat(60));

        // 按热度排序
        const sortedArticles = [...newsData.articles].sort((a, b) => b.heat - a.heat);

        sortedArticles.forEach((article, index) => {
          const rank = index + 1;
          const heat = article.heat.toFixed(0);
          const title = article.title;
          const summary = article.summary ? 
            (article.summary.length > 50 ? article.summary.substring(0, 50) + '...' : article.summary) 
            : '无摘要';
          
          console.log(`\n${rank}. 🔥${heat} ${title}`);
          console.log(`   ${summary}`);
          console.log(`   [ID: ${article.article_id}]`);
        });

        console.log('\n' + '━'.repeat(60));
        console.log('\n💡 使用 node get-article.js <article_id> 查看新闻详情\n');

      } catch (error) {
        console.error(`❌ 解析 JSON 失败：${error.message}`);
        process.exit(1);
      }
    });
  }).on('error', (error) => {
    console.error(`❌ 请求失败：${error.message}`);
    process.exit(1);
  });
}

// 获取命令行参数
const dateArg = process.argv[2];
getDailyNews(dateArg);
