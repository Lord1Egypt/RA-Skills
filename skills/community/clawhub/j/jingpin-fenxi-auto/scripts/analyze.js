#!/usr/bin/env node
/**
 * 竞品分析核心脚本
 * 用法: node analyze.js <竞品关键词或URL> [竞品2] [竞品3] ...
 * 
 * 功能:
 * 1. 多竞品信息抓取
 * 2. 结构化分析报告生成
 * 3. JSON/Markdown 格式导出
 * 
 * 依赖: 无外部依赖，使用内置 http 模块
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  red: '\x1b[31m',
};

// 工具函数：简易 HTML 解析
function extractText(html, maxLen = 500) {
  if (!html) return '';
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, maxLen);
}

// 工具函数：简易 fetch
function fetch(url, options = {}) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const reqOptions = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        ...options.headers,
      },
      timeout: 15000,
    };

    const req = lib.get(url, reqOptions, (res) => {
      // 处理重定向
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
        return fetch(res.headers.location, options).then(resolve).catch(reject);
      }

      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('请求超时')); });
  });
}

// 抓取竞品网站信息
async function crawlCompetitor(url) {
  try {
    console.log(`${colors.blue}[抓取]${colors.reset} ${url}`);
    const html = await fetch(url);
    const text = extractText(html, 2000);
    
    // 提取标题
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '未知网站';
    
    // 提取 meta description
    const descMatch = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i) 
                   || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i);
    const description = descMatch ? descMatch[1].trim() : '';
    
    // 提取 meta keywords
    const keywordsMatch = html.match(/<meta[^>]+name=["']keywords["'][^>]+content=["']([^"']+)["']/i)
                       || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']keywords["']/i);
    const keywords = keywordsMatch ? keywordsMatch[1].trim() : '';

    return {
      url,
      title,
      description,
      keywords,
      contentSnippet: text,
      status: 'success',
      crawledAt: new Date().toISOString(),
    };
  } catch (error) {
    console.log(`${colors.red}[失败]${colors.reset} ${url}: ${error.message}`);
    return {
      url,
      status: 'failed',
      error: error.message,
      crawledAt: new Date().toISOString(),
    };
  }
}

// 搜索竞品信息（使用 DuckDuckGo HTML）
async function searchCompetitor(keyword) {
  try {
    console.log(`${colors.blue}[搜索]${colors.reset} ${keyword}`);
    const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(keyword)}&ia=web`;
    const html = await fetch(searchUrl);
    
    // 解析搜索结果
    const results = [];
    const resultRegex = /<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<a[^>]+class="result__snippet"[^>]*>([\s\S]*?)<\/a>/gi;
    let match;
    let count = 0;
    
    while ((match = resultRegex.exec(html)) !== null && count < 5) {
      const url = match[1];
      const title = extractText(match[2], 200).trim();
      const snippet = extractText(match[3], 300).trim();
      
      if (url && title) {
        results.push({ url, title, snippet });
        count++;
      }
    }
    
    return {
      keyword,
      results,
      status: 'success',
      searchedAt: new Date().toISOString(),
    };
  } catch (error) {
    console.log(`${colors.red}[失败]${colors.reset} ${keyword}: ${error.message}`);
    return {
      keyword,
      status: 'failed',
      error: error.message,
      searchedAt: new Date().toISOString(),
    };
  }
}

// 生成竞品对比分析报告
function generateReport(competitors, outputFormat = 'markdown') {
  const report = {
    generatedAt: new Date().toISOString(),
    competitorCount: competitors.length,
    competitors: competitors.map(c => ({
      name: c.name || extractText(c.title || c.url, 50),
      url: c.url,
      title: c.title,
      description: c.description,
      keywords: c.keywords,
      contentSnippet: c.contentSnippet,
      status: c.status,
    })),
  };

  if (outputFormat === 'json') {
    return JSON.stringify(report, null, 2);
  }

  // Markdown 格式
  let md = `# 竞品分析报告\n\n`;
  md += `> 生成时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
  md += `## 📊 概览\n\n`;
  md += `- 分析竞品数: ${competitors.length}\n`;
  md += `- 成功抓取: ${competitors.filter(c => c.status === 'success').length}\n`;
  md += `- 抓取失败: ${competitors.filter(c => c.status === 'failed').length}\n\n`;
  
  md += `## 📋 竞品详情\n\n`;
  
  competitors.forEach((c, i) => {
    md += `### ${i + 1}. ${c.name || c.url}\n\n`;
    md += `- **网站**: ${c.url}\n`;
    md += `- **标题**: ${c.title || '未知'}\n`;
    md += `- **描述**: ${c.description || '无'}\n`;
    md += `- **关键词**: ${c.keywords || '无'}\n`;
    md += `- **状态**: ${c.status === 'success' ? '✅ 成功' : '❌ 失败'}\n`;
    if (c.status === 'failed') {
      md += `- **失败原因**: ${c.error || '未知'}\n`;
    }
    if (c.contentSnippet) {
      md += `- **内容摘要**: ${c.contentSnippet.substring(0, 300)}...\n`;
    }
    md += `\n---\n\n`;
  });

  md += `## 🔍 关键发现\n\n`;
  md += generateKeyFindings(competitors);

  md += `\n---\n\n`;
  md += `*本报告由 竞品分析自动化 Skill 生成*\n`;

  return md;
}

// 生成关键发现
function generateKeyFindings(competitors) {
  const findings = [];
  
  const successCount = competitors.filter(c => c.status === 'success').length;
  findings.push(`1. **抓取情况**: ${successCount}/${competitors.length} 个竞品成功抓取`);
  
  // 分析描述关键词
  const allKeywords = competitors
    .filter(c => c.keywords)
    .flatMap(c => c.keywords.split(',').map(k => k.trim()))
    .reduce((acc, k) => { acc[k] = (acc[k] || 0) + 1; return acc; }, {});
  
  const topKeywords = Object.entries(allKeywords)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([k]) => k);
  
  if (topKeywords.length > 0) {
    findings.push(`2. **热门关键词**: ${topKeywords.join('、')}`);
  }
  
  findings.push(`3. **建议**: 定期监控竞品动态，关注产品迭代和价格调整`);
  
  return findings.join('\n');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
${colors.bright}竞品分析自动化工具${colors.reset}

${colors.green}用法:${colors.reset}
  node analyze.js <竞品关键词或URL> [竞品2] [竞品3] ...

${colors.green}示例:${colors.reset}
  node analyze.js 智能手表 小米 华为
  node analyze.js https://www.example.com
  node analyze.js 电商平台 --format json

${colors.green}参数:${colors.reset}
  --format <json|markdown>  输出格式（默认 markdown）
  --output <文件名>         保存到文件
`);
    process.exit(0);
  }

  const format = args.includes('--format') 
    ? args[args.indexOf('--format') + 1] || 'markdown'
    : 'markdown';
  
  const outputFile = args.includes('--output')
    ? args[args.indexOf('--output') + 1]
    : null;

  const inputs = args.filter(a => !a.startsWith('--'));

  console.log(`\n${colors.bright}${colors.green}🔍 竞品分析开始${colors.reset}\n`);

  const competitors = [];

  for (const input of inputs) {
    if (input.startsWith('http://') || input.startsWith('https://')) {
      // URL 直接抓取
      const result = await crawlCompetitor(input);
      competitors.push({
        name: input.replace(/^https?:\/\//, '').split('/')[0],
        ...result,
      });
    } else {
      // 关键词搜索
      const result = await searchCompetitor(input);
      if (result.results && result.results.length > 0) {
        // 取第一个结果进行抓取
        const firstResult = result.results[0];
        const crawlResult = await crawlCompetitor(firstResult.url);
        competitors.push({
          name: input,
          searchResults: result.results,
          ...crawlResult,
        });
      } else {
        competitors.push({
          name: input,
          status: 'failed',
          error: '未找到相关结果',
        });
      }
    }
  }

  // 生成报告
  const report = generateReport(competitors, format);

  if (outputFile) {
    const ext = format === 'json' ? 'json' : 'md';
    const filename = outputFile.endsWith(`.${ext}`) ? outputFile : `${outputFile}.${ext}`;
    fs.writeFileSync(filename, report, 'utf8');
    console.log(`\n${colors.green}[保存]${colors.reset} 报告已保存到: ${filename}`);
  } else {
    console.log(`\n${colors.green}[报告]${colors.reset}\n`);
    console.log(report);
  }

  console.log(`\n${colors.green}✅ 分析完成${colors.reset}\n`);
}

main().catch(err => {
  console.error(`${colors.red}[错误]${colors.reset}`, err.message);
  process.exit(1);
});
