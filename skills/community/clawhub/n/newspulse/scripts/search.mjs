#!/usr/bin/env node
/**
 * 📰 NewsPulse - 关键词过滤
 * 根据关键词筛选相关新闻
 */

import fetch from 'node-fetch';

// 新闻源 RSS
const RSS_SOURCES = [
    { name: 'CoinDesk', url: 'https://www.coindesk.com/arc/outboundfeeds/rss/' },
    { name: 'Cointelegraph', url: 'https://cointelegraph.com/rss' },
    { name: 'The Block', url: 'https://www.theblockcrypto.com/rss' },
    { name: 'Decrypt', url: 'https://decrypt.co/feed' },
    { name: 'Bitcoin Magazine', url: 'https://bitcoinmagazine.com/.rss/feed.xml' }
];

// 解析 RSS 的简单函数
async function fetchRSS(url) {
    try {
        const response = await fetch(url, { timeout: 5000 });
        const text = await response.text();
        
        const items = [];
        const itemRegex = /<item>([\s\S]*?)<\/item>/g;
        let match;
        
        while ((match = itemRegex.exec(text)) !== null) {
            const item = match[1];
            const title = item.match(/<title>([\s\S]*?)<\/title>/)?.[1] || '';
            const link = item.match(/<link>([\s\S]*?)<\/link>/)?.[1] || '';
            const pubDate = item.match(/<pubDate>([\s\S]*?)<\/pubDate>/)?.[1] || '';
            const description = item.match(/<description>([\s\S]*?)<\/description>/)?.[1] || '';
            
            if (title && link) {
                items.push({ title, link, pubDate, description });
            }
        }
        
        return items;
    } catch (e) {
        return [];
    }
}

// 检查是否匹配关键词
function matchesKeyword(text, keywords) {
    if (!keywords || keywords.length === 0) return true;
    const lowerText = text.toLowerCase();
    return keywords.some(kw => lowerText.includes(kw.toLowerCase()));
}

// 计算时间差
function timeAgo(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // 秒
    
    if (diff < 60) return `${diff}秒前`;
    if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`;
    return `${Math.floor(diff / 86400)}天前`;
}

async function searchNews(keywords = [], limit = 10) {
    console.log('📰 搜索新闻中...\n');
    
    // 抓取所有新闻源
    const allNews = [];
    
    for (const source of RSS_SOURCES) {
        const items = await fetchRSS(source.url);
        items.forEach(item => {
            item.source = source.name;
            allNews.push(item);
        });
    }
    
    // 过滤关键词
    let filtered = allNews.filter(item => 
        matchesKeyword(item.title, keywords) || 
        matchesKeyword(item.description, keywords)
    );
    
    // 按时间排序
    filtered = filtered.sort((a, b) => 
        new Date(b.pubDate || 0) - new Date(a.pubDate || 0)
    ).slice(0, limit);
    
    if (filtered.length === 0) {
        console.log(`❌ 未找到匹配 "${keywords.join(', ')}" 的新闻`);
        return;
    }
    
    console.log(`📰 NewsPulse - 关键词搜索结果"${keywords.join(', ')}"\n`);
    console.log(`时间      来源            标题`);
    console.log(`────────────────────────────────────────────────────────────────────────────`);
    
    filtered.forEach(item => {
        const time = timeAgo(item.pubDate).padEnd(8);
        const source = item.source.padEnd(14);
        const title = item.title.substring(0, 60) + (item.title.length > 60 ? '...' : '');
        
        console.log(`${time} ${source} ${title}`);
        if (item.link) {
            console.log(`         🔗 ${item.link}`);
        }
        console.log();
    });
    
    console.log(`💡 提示：node scripts/search.mjs bitcoin,eth --limit 15`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
📰 NewsPulse - 关键词搜索

用法:
  node scripts/search.mjs bitcoin         # 搜索 Bitcoin 相关新闻
  node scripts/search.mjs eth,defi        # 搜索多个关键词
  node scripts/search.mjs --limit 20      # 限制结果数量

选项:
  --help, -h        显示帮助
  --limit N         限制显示条数 (默认 10)
  
支持的关键词:
  - 币种：bitcoin, eth, sol, btc 等
  - 主题：defi, nft, regulation, hack 等
  - 平台：aave, compound, uniswap 等
`);
    process.exit(0);
}

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 10;

// 提取关键词 (先移除 --limit 和对应的值)
const cleanedArgs = [];
let skipNext = false;
for (let i = 0; i < args.length; i++) {
    if (args[i] === '--limit') {
        skipNext = true;
        continue;
    }
    if (skipNext) {
        skipNext = false;
        continue;
    }
    if (!args[i].startsWith('--')) {
        cleanedArgs.push(args[i]);
    }
}

const keywords = cleanedArgs.join(',').split(',').filter(k => k.trim());

if (keywords.length === 0) {
    console.log('❌ 请提供关键词');
    console.log('用法：node scripts/search.mjs bitcoin,eth');
    process.exit(1);
}

await searchNews(keywords, limit);
