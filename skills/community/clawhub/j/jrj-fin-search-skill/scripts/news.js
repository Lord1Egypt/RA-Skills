#!/usr/bin/env node

/**
 * 资讯与研报搜索脚本
 * 
 * 使用方法：
 *   node news.js search --keywords="..." [--start="..."] [--end="..."] [--source="..."] [--format=json]
 *   node news.js reports [--keywords="..."] [--start="..."] [--format=json]
 * 
 * 环境变量：
 *   JRJ_API_KEY - API Key（必须）
 */

const https = require('https');
const http = require('http');

// ==================== 配置 ====================

const DEFAULT_API_URL = 'https://quant-gw.jrj.com';
const API_URL = process.env.JRJ_API_URL || DEFAULT_API_URL;
const API_KEY = process.env.JRJ_API_KEY;

// ==================== 工具函数 ====================

function parseArgs() {
  const args = process.argv.slice(2);
  
  // 第一个参数是子命令
  const command = args[0];
  
  const options = {
    command: command,
    keywords: '',
    start: '',
    end: '',
    source: '',
    limit: null,
    format: 'json',
  };

  for (const arg of args.slice(1)) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      if (key === 'keywords') options.keywords = value || '';
      else if (key === 'start') options.start = value || '';
      else if (key === 'end') options.end = value || '';
      else if (key === 'source') options.source = value || '';
      else if (key === 'limit') options.limit = parseInt(value, 10);
      else if (key === 'format') options.format = value || 'json';
      else if (key === 'help') {
        printHelp();
        process.exit(0);
      }
    }
  }

  return options;
}

function printHelp() {
  console.log(`
资讯与研报搜索工具

用法:
  node news.js <命令> [选项]

命令:
  search    搜索资讯
  reports   搜索研报

资讯搜索 (search):
  node news.js search --keywords=<关键词> --start=<开始时间> [选项]

  必填参数:
    --keywords=<关键词>    搜索关键词，多个以空格分隔
    --start=<开始时间>     开始时间，格式: YYYY-MM-DD HH:mm:ss

  可选参数:
    --end=<结束时间>       结束时间，格式: YYYY-MM-DD HH:mm:ss
    --source=<来源>        资讯来源，多个以空格分隔
    --limit=<数量>         返回数量，默认 20
    --format=<格式>        输出格式: json(默认), markdown

  示例:
    node news.js search --keywords="贵州茅台" --start="2026-03-20 00:00:00"
    node news.js search --keywords="贵州茅台" --start="2026-03-20 00:00:00" --end="2026-03-23 23:59:59"
    node news.js search --keywords="人工智能" --start="2026-03-01 00:00:00" --source="财联社 证券时报" --limit=50

研报搜索 (reports):
  node news.js reports --keywords=<关键词> --start=<开始时间> [选项]

  必填参数:
    --keywords=<关键词>    摘要关键词，多个以空格分隔
    --start=<开始时间>     发布日期起始，格式: YYYY-MM-DD HH:mm:ss

  可选参数:
    --limit=<数量>         返回数量，默认 20
    --format=<格式>        输出格式: json(默认), markdown

  示例:
    node news.js reports --keywords="人工智能 大模型" --start="2026-03-01 00:00:00"
    node news.js reports --keywords="新能源" --start="2026-03-01 00:00:00" --limit=30 --format=markdown

环境变量:
  JRJ_API_KEY   API Key

资讯来源:
  财联社, 金十数据, 证券时报, 中国证券报, 上海证券报, 证券日报
`);
}

function error(msg) {
  console.error(`错误: ${msg}`);
  process.exit(1);
}

// ==================== API 调用 ====================

async function fetchAPI(path, body) {
  if (!API_KEY) error('请设置环境变量 JRJ_API_KEY');

  const url = new URL(path, API_URL);
  const bodyStr = JSON.stringify(body);

  return new Promise((resolve, reject) => {
    const protocol = url.protocol === 'https:' ? https : http;
    const req = protocol.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.code !== 0) {
            reject(new Error(`API错误 [${json.code}]: ${json.msg}`));
          } else {
            resolve(json.data);
          }
        } catch (e) {
          reject(new Error(`响应解析失败: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// ==================== 搜索资讯 ====================

async function searchNews(options) {
  const { keywords, start, end, source, limit } = options;
  
  if (!keywords) error('缺少必填参数 --keywords');
  if (!start) error('缺少必填参数 --start');
  
  const body = {
    keywords: keywords,
    makeDateStart: start,
    source: source || '',
  };
  
  // 可选参数
  if (end) body.makeDateEnd = end;
  if (limit) body.limit = limit;
  
  const data = await fetchAPI('/v1/news/search', body);
  
  // 检查是否有更多数据
  if (data.truncated) {
    console.warn('提示: 可能有更多资讯未返回，建议缩小时间范围或调整 --limit 值。');
  }
  
  // 标准化输出（新响应格式：{items, count, truncated?}）
  const items = data.items || [];
  return {
    total: data.count || items.length,
    items: items.map(item => ({
      title: item.title,
      makeDate: item.makeDate,
      source: item.source,
      url: item.url,
      summary: item.summary,
    })),
  };
}

// ==================== 搜索研报 ====================

async function searchReports(options) {
  const { keywords, start, limit } = options;
  
  if (!keywords) error('缺少必填参数 --keywords');
  if (!start) error('缺少必填参数 --start');
  
  const body = {
    keywords: keywords,
    declareDateStart: start,
  };
  
  // 可选参数
  if (limit) body.limit = limit;
  
  const data = await fetchAPI('/v1/news/reports', body);
  
  // 检查是否有更多数据
  if (data.truncated) {
    console.warn('提示: 可能有更多研报未返回，建议缩小时间范围或调整 --limit 值。');
  }
  
  // 标准化输出（新响应格式：{items, count, truncated?}）
  const items = data.items || [];
  
  return {
    total: data.count || items.length,
    items: items.map(item => ({
      title: item.title,
      orgName: item.orgName,
      declareDate: item.declareDate,
      abstract: item.abstract,
    })),
  };
}

// ==================== 输出格式化 ====================

function formatNewsMarkdown(result) {
  let md = `## 资讯搜索结果\n\n`;
  md += `共找到 **${result.total}** 条相关资讯\n\n`;
  
  result.items.forEach((item, index) => {
    md += `### ${index + 1}. ${item.title}\n\n`;
    md += `- **时间**: ${item.makeDate}\n`;
    md += `- **来源**: ${item.source}\n`;
    if (item.url) md += `- **链接**: ${item.url}\n`;
    md += `\n`;
    if (item.summary) {
      md += `> ${item.summary.substring(0, 200)}${item.summary.length > 200 ? '...' : ''}\n`;
    }
    md += `\n---\n\n`;
  });
  
  return md;
}

function formatReportsMarkdown(result) {
  let md = `## 研报搜索结果\n\n`;
  md += `共找到 **${result.total}** 篇相关研报\n\n`;
  
  result.items.forEach((item, index) => {
    md += `### ${index + 1}. ${item.title}\n\n`;
    md += `- **机构**: ${item.orgName}\n`;
    md += `- **发布日期**: ${item.declareDate}\n`;
    md += `\n`;
    if (item.abstract) {
      // 摘要可能很长，截取
      const abstract = item.abstract.replace(/\n/g, ' ').substring(0, 300);
      md += `> ${abstract}${item.abstract.length > 300 ? '...' : ''}\n`;
    }
    md += `\n---\n\n`;
  });
  
  return md;
}

// ==================== 主函数 ====================

async function main() {
  const options = parseArgs();
  
  if (!options.command) {
    printHelp();
    process.exit(1);
  }
  
  try {
    let result;
    
    switch (options.command) {
      case 'search':
        result = await searchNews(options);
        break;
        
      case 'reports':
        result = await searchReports(options);
        break;
        
      case 'help':
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
        break;
        
      default:
        error(`未知命令: ${options.command}，使用 --help 查看帮助`);
    }
    
    // 输出结果
    if (options.format === 'markdown') {
      if (options.command === 'search') {
        console.log(formatNewsMarkdown(result));
      } else if (options.command === 'reports') {
        console.log(formatReportsMarkdown(result));
      }
    } else {
      console.log(JSON.stringify(result, null, 2));
    }
    
  } catch (err) {
    error(err.message);
  }
}

main();
