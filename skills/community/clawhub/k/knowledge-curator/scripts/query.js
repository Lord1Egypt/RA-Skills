/**
 * query.js - 查询检索模块
 * 
 * 提供知识库的搜索、过滤和检索功能
 */

const fs = require('fs');
const path = require('path');
const store = require('./store');

/**
 * 简单分词器
 * @param {string} text - 待分词文本
 * @returns {Array<string>} 词数组
 */
function tokenize(text) {
  if (!text) return [];
  // 中文按字符分词，英文按空格分词
  const chinese = text.match(/[\u4e00-\u9fa5]+/g) || [];
  const english = text.match(/[a-zA-Z0-9]+/g) || [];
  return [...chinese, ...english].map(w => w.toLowerCase());
}

/**
 * 计算查询与内容的匹配度
 * @param {string} query - 查询词
 * @param {Object} entry - 知识条目
 * @returns {number} 匹配度分数
 */
function calculateMatchScore(query, entry) {
  const queryTokens = tokenize(query);
  if (queryTokens.length === 0) return 0;
  
  let score = 0;
  
  // 标题匹配（权重最高）
  const titleLower = (entry.title || '').toLowerCase();
  for (const token of queryTokens) {
    if (titleLower.includes(token)) {
      score += 10;
    }
  }
  
  // 标签匹配（权重高）
  const tags = entry.tags || [];
  for (const token of queryTokens) {
    for (const tag of tags) {
      if (tag.toLowerCase().includes(token)) {
        score += 5;
      }
    }
  }
  
  // 分类匹配
  if (queryTokens.includes(entry.category?.toLowerCase())) {
    score += 3;
  }
  
  return score;
}

/**
 * 搜索知识库
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @param {Object} config - 配置对象
 * @returns {Array<Object>} 搜索结果
 */
function search(query, options = {}, config = store.DEFAULT_CONFIG) {
  const indexPath = path.resolve(config.indexPath);
  const index = store.loadIndex(indexPath);
  
  if (!query || query.trim() === '') {
    return index.entries;
  }
  
  const results = [];
  const queryTokens = tokenize(query);
  
  for (const entry of index.entries) {
    // 基础过滤
    if (options.category && entry.category !== options.category) {
      continue;
    }
    
    // 计算匹配度
    let score = calculateMatchScore(query, entry);
    
    // 读取文件内容进行全文搜索
    try {
      if (fs.existsSync(entry.filePath)) {
        const content = fs.readFileSync(entry.filePath, 'utf-8');
        const contentLower = content.toLowerCase();
        
        for (const token of queryTokens) {
          if (contentLower.includes(token)) {
            score += 1;
          }
        }
      }
    } catch (error) {
      // 文件读取失败，跳过全文搜索
    }
    
    if (score > 0) {
      results.push({
        ...entry,
        score,
        matchType: score >= 10 ? 'title' : score >= 5 ? 'tag' : 'content'
      });
    }
  }
  
  // 按分数排序
  results.sort((a, b) => b.score - a.score);
  
  // 限制结果数量
  const limit = options.limit || 20;
  return results.slice(0, limit);
}

/**
 * 按分类列出条目
 * @param {string} category - 分类名称
 * @param {Object} options - 选项
 * @param {Object} config - 配置对象
 * @returns {Array<Object>} 条目列表
 */
function listByCategory(category, options = {}, config = store.DEFAULT_CONFIG) {
  const filters = {};
  
  if (category && category !== '全部') {
    filters.category = category;
  }
  
  if (options.limit) {
    filters.limit = options.limit;
  }
  
  return store.getEntries(filters, config);
}

/**
 * 获取单个条目详情
 * @param {string} entryId - 条目 ID
 * @param {Object} config - 配置对象
 * @returns {Object|null} 条目详情
 */
function getEntryDetail(entryId, config = store.DEFAULT_CONFIG) {
  const indexPath = path.resolve(config.indexPath);
  const index = store.loadIndex(indexPath);
  
  const entry = index.entries.find(e => e.id === entryId);
  if (!entry) {
    return null;
  }
  
  // 读取完整内容
  try {
    if (fs.existsSync(entry.filePath)) {
      const content = fs.readFileSync(entry.filePath, 'utf-8');
      return {
        ...entry,
        fullContent: content
      };
    }
  } catch (error) {
    console.error('读取文件失败:', error.message);
  }
  
  return entry;
}

/**
 * 获取热门标签
 * @param {Object} config - 配置对象
 * @param {number} limit - 返回数量
 * @returns {Array<Object>} 标签列表
 */
function getPopularTags(config = store.DEFAULT_CONFIG, limit = 10) {
  const indexPath = path.resolve(config.indexPath);
  const index = store.loadIndex(indexPath);
  
  const tagCount = {};
  
  for (const entry of index.entries) {
    for (const tag of (entry.tags || [])) {
      const normalizedTag = tag.replace(/^#/, '');
      tagCount[normalizedTag] = (tagCount[normalizedTag] || 0) + 1;
    }
  }
  
  // 排序并返回前 N 个
  const sortedTags = Object.entries(tagCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([tag, count]) => ({ tag, count }));
  
  return sortedTags;
}

/**
 * 获取最近添加的条目
 * @param {number} limit - 返回数量
 * @param {Object} config - 配置对象
 * @returns {Array<Object>} 条目列表
 */
function getRecentEntries(limit = 10, config = store.DEFAULT_CONFIG) {
  return store.getEntries({ limit }, config);
}

/**
 * 导出搜索结果
 * @param {Array<Object>} results - 搜索结果
 * @param {string} format - 导出格式 (markdown, json, csv)
 * @returns {string} 导出内容
 */
function exportResults(results, format = 'markdown') {
  if (format === 'json') {
    return JSON.stringify(results, null, 2);
  }
  
  if (format === 'csv') {
    const headers = ['ID', '标题', '分类', '标签', '日期', '链接'];
    const rows = results.map(r => [
      r.id,
      `"${r.title.replace(/"/g, '""')}"`,
      r.category,
      `"${(r.tags || []).join(';')}"`,
      r.createdAt.split('T')[0],
      r.originalUrl
    ]);
    
    return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }
  
  // 默认 Markdown 格式
  let markdown = `# 知识库导出\n\n`;
  markdown += `导出时间：${new Date().toLocaleString('zh-CN')}\n`;
  markdown += `条目数量：${results.length}\n\n`;
  markdown += `---\n\n`;
  
  for (const result of results) {
    markdown += `## ${result.title}\n\n`;
    markdown += `- **分类**: ${result.category}\n`;
    markdown += `- **标签**: ${(result.tags || []).join(', ')}\n`;
    markdown += `- **日期**: ${result.createdAt.split('T')[0]}\n`;
    markdown += `- **链接**: ${result.originalUrl}\n\n`;
  }
  
  return markdown;
}

/**
 * 语义搜索（简化版）
 * 使用关键词扩展和同义词匹配
 * @param {string} query - 查询词
 * @param {Object} config - 配置对象
 * @returns {Array<Object>} 搜索结果
 */
function semanticSearch(query, config = store.DEFAULT_CONFIG) {
  // 简单的同义词扩展
  const synonyms = {
    'AI': ['人工智能', '机器学习', '深度学习'],
    '编程': ['代码', '开发', '写代码', 'programming'],
    '学习': ['教程', '课程', '培训', '教育'],
    '工作': ['职场', '上班', '职业', '就业'],
    '健康': ['运动', '健身', '养生', '医疗']
  };
  
  let expandedQuery = query;
  
  // 扩展查询词
  for (const [key, values] of Object.entries(synonyms)) {
    if (query.includes(key)) {
      expandedQuery += ' ' + values.join(' ');
    }
  }
  
  // 使用扩展后的查询进行搜索
  return search(expandedQuery, {}, config);
}

// 导出模块
module.exports = {
  search,
  listByCategory,
  getEntryDetail,
  getPopularTags,
  getRecentEntries,
  exportResults,
  semanticSearch,
  calculateMatchScore,
  tokenize
};

// CLI 模式支持
if (require.main === module) {
  const command = process.argv[2];
  const query = process.argv[3];
  
  if (command === 'search' && query) {
    const results = search(query, { limit: 10 });
    console.log(`\n=== 搜索结果："${query}" (${results.length}条) ===\n`);
    for (const result of results) {
      console.log(`[${result.category}] ${result.title}`);
      console.log(`  标签：${(result.tags || []).join(' ')}`);
      console.log(`  匹配度：${result.score} | 类型：${result.matchType}`);
      console.log();
    }
  } else if (command === 'list') {
    const category = process.argv[3];
    const entries = listByCategory(category || '全部');
    console.log(`\n=== ${category || '全部'}分类 (${entries.length}条) ===\n`);
    for (const entry of entries) {
      console.log(`[${entry.id}] ${entry.title} (${entry.createdAt.split('T')[0]})`);
    }
  } else if (command === 'tags') {
    const tags = getPopularTags();
    console.log('\n=== 热门标签 ===\n');
    for (const tag of tags) {
      console.log(`#${tag.tag} (${tag.count}次)`);
    }
  } else {
    console.log('用法:');
    console.log('  node query.js search <关键词>  - 搜索');
    console.log('  node query.js list [分类]      - 列出');
    console.log('  node query.js tags             - 热门标签');
  }
}
