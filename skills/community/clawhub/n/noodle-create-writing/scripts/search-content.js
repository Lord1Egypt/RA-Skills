/**
 * 搜索相关内容模块
 * 使用Tavily API搜索与主题相关的信息
 */

const { execSync } = require('child_process');
const path = require('path');

// 面食相关关键词库
const NOODLE_KEYWORDS = {
  // 浇头/配料
  toppings: ['浇头', '配料', '臊子', '码子', '配菜', '佐料'],
  
  // 汤底/汤头
  soup: ['汤底', '汤头', '高汤', '清汤', '红汤', '白汤'],
  
  // 面条类型
  noodleTypes: ['细面', '宽面', '拉面', '刀削面', '手擀面', '机制面'],
  
  // 吃法/习俗
  eatingHabits: ['吃法', '习俗', '传统', '讲究', '规矩', '礼仪'],
  
  // 季节限定
  seasonal: ['时令', '季节', '春季', '夏季', '秋季', '冬季', '限定'],
  
  // 地方特色
  regional: ['地方特色', '地域', '本地', '传统', '老字号', '非遗'],
  
  // 健康营养
  health: ['健康', '营养', '养生', '好处', '功效', '营养价值'],
  
  // 文化内涵
  culture: ['文化', '内涵', '历史', '渊源', '故事', '传说', '民俗']
};

// 默认搜索关键词
const DEFAULT_KEYWORDS = {
  noodle: ['面', '面条', '面食', '汤面', '拌面'],
  general: ['怎么吃', '吃什么', '哪里吃', '什么时候吃', '好处', '文化']
};

/**
 * 搜索相关内容
 * @param {Object} options 搜索选项
 * @returns {Promise<Object>} 搜索结果
 */
async function searchContent(options) {
  const {
    topic,
    keywords = [],
    count = 10,
    days = 30,
    deep = false,
    verbose = false
  } = options;
  
  // 构建搜索查询
  const searchQueries = buildSearchQueries(topic, keywords);
  
  if (verbose) {
    console.log(`🔍 搜索查询：${searchQueries.join(', ')}`);
  }
  
  // 执行搜索（这里使用tavily-search技能）
  const searchResults = [];
  
  for (const query of searchQueries.slice(0, 3)) { // 限制前3个查询
    try {
      const result = await executeTavilySearch(query, count, days, deep);
      if (result && result.sources) {
        searchResults.push(...result.sources);
        
        if (verbose) {
          console.log(`✅ 搜索 "${query}" 获得 ${result.sources.length} 个结果`);
        }
      }
    } catch (error) {
      if (verbose) {
        console.warn(`⚠️ 搜索 "${query}" 失败：${error.message}`);
      }
    }
    
    // 避免请求过快
    await sleep(1000);
  }
  
  // 去重结果
  const uniqueResults = removeDuplicates(searchResults);
  
  return {
    topic,
    keywords,
    searchQueries,
    sources: uniqueResults.slice(0, count * 2), // 保留更多结果供后续处理
    totalResults: uniqueResults.length,
    searchDate: new Date().toISOString()
  };
}

/**
 * 构建搜索查询
 */
function buildSearchQueries(topic, userKeywords) {
  const queries = [];
  
  // 1. 基础查询：主题 + 通用关键词
  for (const generalKeyword of DEFAULT_KEYWORDS.general) {
    queries.push(`${topic} ${generalKeyword}`);
  }
  
  // 2. 用户指定关键词
  for (const keyword of userKeywords) {
    if (keyword.trim()) {
      queries.push(`${topic} ${keyword}`);
    }
  }
  
  // 3. 面食相关关键词（如果主题包含面食相关词汇）
  if (isNoodleRelated(topic)) {
    for (const category in NOODLE_KEYWORDS) {
      for (const keyword of NOODLE_KEYWORDS[category]) {
        queries.push(`${topic} ${keyword}`);
      }
    }
  }
  
  // 4. 组合查询
  if (userKeywords.length >= 2) {
    queries.push(`${topic} ${userKeywords.slice(0, 3).join(' ')}`);
  }
  
  // 去重并限制数量
  return [...new Set(queries)].slice(0, 10);
}

/**
 * 判断是否与面食相关
 */
function isNoodleRelated(text) {
  const noodleIndicators = ['面', '面条', '面食', '汤面', '拌面', '拉面', '刀削面'];
  return noodleIndicators.some(indicator => text.includes(indicator));
}

/**
 * 执行Tavily搜索
 */
async function executeTavilySearch(query, count, days, deep) {
  try {
    // 构建命令
    const tavilySkillPath = path.join(__dirname, '../../tavily-search');
    const cmd = [
      'node',
      path.join(tavilySkillPath, 'scripts/search.mjs'),
      `"${query}"`,
      `-n ${count}`,
      days ? `--days ${days}` : '',
      deep ? '--deep' : '',
      '--topic general'
    ].filter(Boolean).join(' ');
    
    // 执行命令
    const output = execSync(cmd, { 
      encoding: 'utf8',
      cwd: tavilySkillPath,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // 解析输出（Tavily搜索返回markdown格式）
    return parseTavilyOutput(output);
  } catch (error) {
    console.error(`执行Tavily搜索失败：${error.message}`);
    return null;
  }
}

/**
 * 解析Tavily输出
 */
function parseTavilyOutput(output) {
  try {
    const lines = output.split('\n');
    const sources = [];
    let currentSource = null;
    
    for (const line of lines) {
      // 匹配来源行：- **标题** (relevance: XX%)
      const sourceMatch = line.match(/^- \*\*(.*?)\*\* \(relevance: (\d+)%\)/);
      if (sourceMatch) {
        if (currentSource) {
          sources.push(currentSource);
        }
        currentSource = {
          title: sourceMatch[1].trim(),
          relevance: parseInt(sourceMatch[2]),
          content: ''
        };
        continue;
      }
      
      // 匹配URL行
      const urlMatch = line.match(/^\s+(https?:\/\/[^\s]+)/);
      if (urlMatch && currentSource) {
        currentSource.url = urlMatch[1].trim();
        continue;
      }
      
      // 收集内容（在标题和URL之后的行）
      if (currentSource && line.trim() && !line.startsWith('  ') && !line.match(/^[=-]+$/)) {
        currentSource.content += line.trim() + ' ';
      }
    }
    
    // 添加最后一个来源
    if (currentSource) {
      sources.push(currentSource);
    }
    
    // 提取总结（第一段）
    const summaryMatch = output.match(/^## Answer\s*\n\s*\n(.+?)\s*\n\s*\n---/s);
    const summary = summaryMatch ? summaryMatch[1].trim() : '';
    
    return {
      summary,
      sources,
      rawOutput: output
    };
  } catch (error) {
    console.error('解析Tavily输出失败：', error);
    return { summary: '', sources: [], rawOutput: output };
  }
}

/**
 * 去重搜索结果
 */
function removeDuplicates(results) {
  const seen = new Set();
  return results.filter(result => {
    const key = result.url || result.title;
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    return true;
  });
}

/**
 * 睡眠函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = { searchContent, NOODLE_KEYWORDS, DEFAULT_KEYWORDS };