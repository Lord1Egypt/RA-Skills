#!/usr/bin/env node

/**
 * News Fetcher V2 - 新闻获取工具
 * 
 * 用法:
 *   node fetch_news.mjs <url> --direct
 *   node fetch_news.mjs <url> --search "关键词"
 */

import fetch from 'node-fetch';

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;

const args = process.argv.slice(2);
const url = args.find(a => !a.startsWith('--'));
const useDirect = args.includes('--direct');
const searchIndex = args.indexOf('--search');
const searchQuery = searchIndex > -1 ? args[searchIndex + 1] : null;

if (!url && !searchQuery) {
  console.log('News Fetcher V2 - 新闻获取工具\n');
  console.log('用法:');
  console.log('  node fetch_news.mjs <url> --direct');
  console.log('  node fetch_news.mjs <url> --search "关键词"');
  console.log('\n说明:');
  console.log('  --direct  直接访问网页');
  console.log('  --search  使用 Tavily 搜索相关报道');
  process.exit(1);
}

// 使用 Tavily 搜索
async function searchAlternatives(query) {
  if (!TAVILY_API_KEY) {
    throw new Error('需要设置 TAVILY_API_KEY 环境变量');
  }

  const response = await fetch('https://api.tavily.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${TAVILY_API_KEY}`
    },
    body: JSON.stringify({
      query: `${query} (site:bbc.com OR site:reuters.com OR site:apnews.com OR site:aljazeera.com)`,
      max_results: 10
    })
  });

  const data = await response.json();
  return data.results || [];
}

// 直接获取
async function fetchDirect(targetUrl) {
  const response = await fetch(targetUrl, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; NewsFetcher/2.0)'
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const text = await response.text();
  return { raw_content: text };
}

// 主函数
async function main() {
  console.log('━'.repeat(50));
  console.log('📰 News Fetcher V2');
  console.log('━'.repeat(50) + '\n');

  // 搜索模式
  if (searchQuery) {
    console.log(`🔍 搜索相关文章: "${searchQuery}"\n`);
    const results = await searchAlternatives(searchQuery);
    
    if (results.length === 0) {
      console.log('❌ 未找到相关文章');
      return;
    }
    
    console.log(`✓ 找到 ${results.length} 篇相关文章:\n`);
    results.forEach((r, i) => {
      console.log(`${i + 1}. ${r.title || '无标题'}`);
      console.log(`   📎 ${r.url}`);
      if (r.content) {
        console.log(`   📝 ${r.content.substring(0, 100)}...`);
      }
      console.log('');
    });
    return;
  }

  // 直接访问模式
  console.log(`🔗 访问链接: ${url}\n`);

  try {
    const result = await fetchDirect(url);
    
    if (result.raw_content && result.raw_content.length > 300) {
      console.log(`✅ 成功获取`);
      console.log(`   📊 ${result.raw_content.length} 字符\n`);
      console.log('─'.repeat(50));
      console.log('📄 内容:\n');
      console.log(result.raw_content.substring(0, 5000));
    } else {
      console.log('❌ 内容不足');
    }
  } catch (err) {
    console.log(`❌ ${err.message}`);
    console.log('\n💡 建议:');
    console.log('   1. 搜索替代信源（BBC/Reuters/AP）');
    console.log('   2. 使用 --search 参数搜索相关报道');
  }
}

main().catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
