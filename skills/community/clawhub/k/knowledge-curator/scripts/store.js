/**
 * store.js - 存储管理模块
 * 
 * 负责知识库的存储、索引、去重和增量更新
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 默认配置
const DEFAULT_CONFIG = {
  knowledgeBasePath: './knowledge-base',
  indexPath: './knowledge-base/index.json',
  categories: ['科技', '生活', '学习', '娱乐', '工作', '健康'],
  duplicateThreshold: 0.85
};

/**
 * 确保目录存在
 * @param {string} dirPath - 目录路径
 */
function ensureDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * 生成唯一 ID
 * @param {string} url - 原始 URL
 * @returns {string} 唯一 ID
 */
function generateId(url) {
  const timestamp = Date.now();
  const hash = crypto.createHash('md5').update(url + timestamp).digest('hex').substring(0, 8);
  return `kb-${timestamp}-${hash}`;
}

/**
 * 生成内容指纹（用于去重）
 * @param {string} content - 内容文本
 * @returns {string} 内容指纹
 */
function generateFingerprint(content) {
  // 提取关键特征生成指纹
  const normalized = content.toLowerCase().replace(/\s+/g, ' ').trim();
  const keyPart = normalized.substring(0, 500);
  return crypto.createHash('md5').update(keyPart).digest('hex');
}

/**
 * 计算内容相似度
 * @param {string} content1 - 内容 1
 * @param {string} content2 - 内容 2
 * @returns {number} 相似度 (0-1)
 */
function calculateSimilarity(content1, content2) {
  // 简化版 Jaccard 相似度
  const words1 = new Set(content1.toLowerCase().split(/\s+/));
  const words2 = new Set(content2.toLowerCase().split(/\s+/));
  
  const intersection = new Set([...words1].filter(w => words2.has(w)));
  const union = new Set([...words1, ...words2]);
  
  return intersection.size / union.size;
}

/**
 * 加载索引
 * @param {string} indexPath - 索引文件路径
 * @returns {Object} 索引对象
 */
function loadIndex(indexPath) {
  try {
    if (fs.existsSync(indexPath)) {
      const data = fs.readFileSync(indexPath, 'utf-8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('加载索引失败:', error.message);
  }
  
  return {
    version: '1.0',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    entries: [],
    categories: {},
    stats: {
      total: 0,
      byCategory: {}
    }
  };
}

/**
 * 保存索引
 * @param {string} indexPath - 索引文件路径
 * @param {Object} index - 索引对象
 */
function saveIndex(indexPath, index) {
  ensureDirectory(path.dirname(indexPath));
  index.updatedAt = new Date().toISOString();
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf-8');
}

/**
 * 检查是否重复
 * @param {Object} index - 索引对象
 * @param {string} url - 新 URL
 * @param {string} content - 新内容
 * @param {number} threshold - 相似度阈值
 * @returns {Object|null} 重复条目或 null
 */
function checkDuplicate(index, url, content, threshold = 0.85) {
  // URL 完全匹配
  const urlMatch = index.entries.find(entry => entry.originalUrl === url);
  if (urlMatch) {
    return { type: 'url', entry: urlMatch };
  }
  
  // 内容相似度匹配
  const newFingerprint = generateFingerprint(content);
  for (const entry of index.entries) {
    if (entry.fingerprint === newFingerprint) {
      return { type: 'fingerprint', entry };
    }
  }
  
  // 标题相似度匹配
  const newTitle = content.substring(0, 100).toLowerCase();
  for (const entry of index.entries) {
    const similarity = calculateSimilarity(newTitle, entry.title.toLowerCase());
    if (similarity > threshold) {
      return { type: 'title', entry, similarity };
    }
  }
  
  return null;
}

/**
 * 存储知识条目
 * @param {Object} entry - 知识条目
 * @param {Object} config - 配置对象
 * @returns {Object} 存储结果
 */
function storeEntry(entry, config = DEFAULT_CONFIG) {
  const knowledgeBasePath = path.resolve(config.knowledgeBasePath);
  const indexPath = path.resolve(config.indexPath);
  
  // 确保目录存在
  ensureDirectory(knowledgeBasePath);
  for (const category of config.categories) {
    ensureDirectory(path.join(knowledgeBasePath, category));
  }
  
  // 加载索引
  const index = loadIndex(indexPath);
  
  // 检查重复
  const duplicate = checkDuplicate(index, entry.url, entry.content || entry.title, config.duplicateThreshold);
  if (duplicate) {
    return {
      success: false,
      reason: 'duplicate',
      duplicate: duplicate.entry,
      duplicateType: duplicate.type,
      similarity: duplicate.similarity
    };
  }
  
  // 生成条目 ID
  const entryId = generateId(entry.url);
  entry.id = entryId;
  entry.createdAt = new Date().toISOString();
  entry.fingerprint = generateFingerprint(entry.content || entry.title);
  
  // 生成文件名
  const safeTitle = entry.title.replace(/[<>:"/\\|?*]/g, '_').substring(0, 50);
  const fileName = `${entryId}-${safeTitle}.md`;
  const filePath = path.join(knowledgeBasePath, entry.category, fileName);
  
  // 生成 Markdown 内容
  const markdownContent = generateMarkdown(entry);
  
  // 写入文件
  fs.writeFileSync(filePath, markdownContent, 'utf-8');
  
  // 更新索引
  const indexEntry = {
    id: entryId,
    title: entry.title,
    originalUrl: entry.url,
    category: entry.category,
    tags: entry.tags || [],
    filePath,
    fileName,
    createdAt: entry.createdAt,
    fingerprint: entry.fingerprint
  };
  
  index.entries.push(indexEntry);
  index.stats.total = index.entries.length;
  
  // 更新分类统计
  if (!index.stats.byCategory[entry.category]) {
    index.stats.byCategory[entry.category] = 0;
  }
  index.stats.byCategory[entry.category]++;
  
  // 保存索引
  saveIndex(indexPath, index);
  
  return {
    success: true,
    entry: indexEntry,
    filePath
  };
}

/**
 * 生成 Markdown 格式内容
 * @param {Object} entry - 知识条目
 * @returns {string} Markdown 内容
 */
function generateMarkdown(entry) {
  const date = new Date(entry.createdAt || Date.now());
  const dateStr = date.toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  const tags = (entry.tags || []).map(tag => `#${tag.replace(/^#/, '')}`).join(' ');
  
  let markdown = `# ${entry.title}\n\n`;
  markdown += `**原始链接**: [${entry.url}](${entry.url})\n`;
  markdown += `**来源平台**: ${entry.platform || '未知'}\n`;
  markdown += `**收藏日期**: ${dateStr}\n`;
  markdown += `**分类**: ${entry.category}\n`;
  markdown += `**标签**: ${tags || '无'}\n\n`;
  
  if (entry.summary) {
    markdown += `## 摘要\n\n${entry.summary}\n\n`;
  }
  
  if (entry.keyPoints && entry.keyPoints.length > 0) {
    markdown += `## 关键知识点\n\n`;
    for (const point of entry.keyPoints) {
      markdown += `- ${point}\n`;
    }
    markdown += '\n';
  }
  
  if (entry.content) {
    markdown += `## 原文内容\n\n${entry.content}\n\n`;
  }
  
  if (entry.notes) {
    markdown += `## 备注\n\n${entry.notes}\n\n`;
  }
  
  markdown += `---\n*由 Knowledge Curator 自动整理*\n`;
  
  return markdown;
}

/**
 * 删除条目
 * @param {string} entryId - 条目 ID
 * @param {Object} config - 配置对象
 * @returns {Object} 删除结果
 */
function deleteEntry(entryId, config = DEFAULT_CONFIG) {
  const indexPath = path.resolve(config.indexPath);
  const index = loadIndex(indexPath);
  
  const entryIndex = index.entries.findIndex(e => e.id === entryId);
  if (entryIndex === -1) {
    return { success: false, reason: 'not_found' };
  }
  
  const entry = index.entries[entryIndex];
  
  // 删除文件
  try {
    if (fs.existsSync(entry.filePath)) {
      fs.unlinkSync(entry.filePath);
    }
  } catch (error) {
    console.error('删除文件失败:', error.message);
  }
  
  // 从索引中移除
  index.entries.splice(entryIndex, 1);
  index.stats.total = index.entries.length;
  
  // 更新分类统计
  if (index.stats.byCategory[entry.category]) {
    index.stats.byCategory[entry.category]--;
  }
  
  saveIndex(indexPath, index);
  
  return { success: true, deletedEntry: entry };
}

/**
 * 获取条目列表
 * @param {Object} filters - 过滤条件
 * @param {Object} config - 配置对象
 * @returns {Array<Object>} 条目列表
 */
function getEntries(filters = {}, config = DEFAULT_CONFIG) {
  const indexPath = path.resolve(config.indexPath);
  const index = loadIndex(indexPath);
  
  let entries = [...index.entries];
  
  // 按分类过滤
  if (filters.category) {
    entries = entries.filter(e => e.category === filters.category);
  }
  
  // 按标签过滤
  if (filters.tags && filters.tags.length > 0) {
    entries = entries.filter(e => 
      filters.tags.some(tag => e.tags.includes(tag))
    );
  }
  
  // 按时间范围过滤
  if (filters.startDate) {
    const startDate = new Date(filters.startDate);
    entries = entries.filter(e => new Date(e.createdAt) >= startDate);
  }
  if (filters.endDate) {
    const endDate = new Date(filters.endDate);
    entries = entries.filter(e => new Date(e.createdAt) <= endDate);
  }
  
  // 排序
  entries.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  
  // 分页
  if (filters.limit) {
    entries = entries.slice(0, filters.limit);
  }
  if (filters.offset) {
    entries = entries.slice(filters.offset);
  }
  
  return entries;
}

/**
 * 获取统计信息
 * @param {Object} config - 配置对象
 * @returns {Object} 统计信息
 */
function getStats(config = DEFAULT_CONFIG) {
  const indexPath = path.resolve(config.indexPath);
  const index = loadIndex(indexPath);
  return index.stats;
}

// 导出模块
module.exports = {
  storeEntry,
  deleteEntry,
  getEntries,
  getStats,
  loadIndex,
  saveIndex,
  checkDuplicate,
  calculateSimilarity,
  generateMarkdown,
  DEFAULT_CONFIG
};

// CLI 模式支持
if (require.main === module) {
  const command = process.argv[2];
  
  if (command === 'stats') {
    const stats = getStats();
    console.log('\n=== 知识库统计 ===');
    console.log(`总条目数：${stats.total}`);
    console.log('分类分布:');
    for (const [category, count] of Object.entries(stats.byCategory)) {
      console.log(`  ${category}: ${count}条`);
    }
  } else if (command === 'list') {
    const category = process.argv[3];
    const entries = getEntries(category ? { category } : {});
    console.log(`\n=== 知识库条目 (${entries.length}条) ===`);
    for (const entry of entries.slice(0, 10)) {
      console.log(`[${entry.category}] ${entry.title} (${entry.createdAt.split('T')[0]})`);
    }
  } else {
    console.log('用法:');
    console.log('  node store.js stats          - 查看统计');
    console.log('  node store.js list [category] - 列出条目');
  }
}
