/**
 * main.js - Knowledge Curator 主入口
 * 
 * 整合所有模块，提供统一的 CLI 和 API 接口
 */

const path = require('path');
const fetch = require('./fetch');
const summarize = require('./summarize');
const categorize = require('./categorize');
const store = require('./store');
const query = require('./query');

// 默认配置
const CONFIG = {
  knowledgeBasePath: path.join(__dirname, '../knowledge-base'),
  indexPath: path.join(__dirname, '../knowledge-base/index.json'),
  categories: ['科技', '生活', '学习', '娱乐', '工作', '健康'],
  duplicateThreshold: 0.85,
  requestDelay: 1000
};

/**
 * 处理用户发送的链接
 * @param {string} url - 用户发送的 URL
 * @param {Object} options - 选项 {category, notes, platform}
 * @returns {Promise<Object>} 处理结果
 */
async function processLink(url, options = {}) {
  console.log(`🔄 开始处理链接：${url}`);
  
  try {
    // 1. 抓取内容
    console.log('📥 正在抓取内容...');
    const content = await fetch.fetchContent(url);
    
    // 2. 生成摘要和知识点
    console.log('📝 正在生成摘要...');
    const processed = await summarize.processContent(content);
    
    // 3. 自动分类（如果用户未指定）
    let category = options.category;
    if (!category) {
      console.log('🏷️ 正在自动分类...');
      const classification = categorize.categorize(processed);
      category = classification.category;
      
      if (classification.uncertain) {
        console.log('⚠️ 分类置信度较低，可能需要手动调整');
      }
    }
    
    // 4. 存储到知识库
    console.log('💾 正在保存到知识库...');
    const entry = {
      ...processed,
      category,
      notes: options.notes || '',
      platform: content.platform?.name || '网页'
    };
    
    const storeResult = store.storeEntry(entry, CONFIG);
    
    if (storeResult.success) {
      console.log('✅ 保存成功!');
      return {
        success: true,
        message: '已保存到知识库',
        entry: storeResult.entry,
        category,
        filePath: storeResult.filePath
      };
    } else if (storeResult.reason === 'duplicate') {
      console.log('⚠️ 检测到重复内容');
      return {
        success: false,
        reason: 'duplicate',
        message: '内容已存在于知识库中',
        duplicate: storeResult.duplicate
      };
    } else {
      throw new Error(`存储失败：${storeResult.reason}`);
    }
  } catch (error) {
    console.error('❌ 处理失败:', error.message);
    return {
      success: false,
      reason: 'error',
      message: error.message
    };
  }
}

/**
 * 搜索知识库
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @returns {Array<Object>} 搜索结果
 */
function searchKnowledge(query, options = {}) {
  console.log(`🔍 搜索：${query}`);
  
  if (options.semantic) {
    return query.semanticSearch(query, CONFIG);
  } else {
    return query.search(query, options, CONFIG);
  }
}

/**
 * 列出知识库内容
 * @param {string} category - 分类名称
 * @param {Object} options - 选项
 * @returns {Array<Object>} 条目列表
 */
function listKnowledge(category = null, options = {}) {
  console.log(`📋 列出内容${category ? ` - ${category}` : ''}`);
  return query.listByCategory(category, options, CONFIG);
}

/**
 * 查看条目详情
 * @param {string} entryId - 条目 ID
 * @returns {Object|null} 条目详情
 */
function viewEntry(entryId) {
  console.log(`📖 查看条目：${entryId}`);
  return query.getEntryDetail(entryId, CONFIG);
}

/**
 * 删除条目
 * @param {string} entryId - 条目 ID
 * @returns {Object} 删除结果
 */
function deleteEntry(entryId) {
  console.log(`🗑️ 删除条目：${entryId}`);
  return store.deleteEntry(entryId, CONFIG);
}

/**
 * 获取统计信息
 * @returns {Object} 统计信息
 */
function getStats() {
  return store.getStats(CONFIG);
}

/**
 * 导出知识库
 * @param {string} format - 导出格式
 * @param {Object} options - 导出选项
 * @returns {string} 导出内容
 */
function exportKnowledge(format = 'markdown', options = {}) {
  const entries = store.getEntries(options, CONFIG);
  return query.exportResults(entries, format);
}

/**
 * 批量处理链接
 * @param {Array<string>} urls - URL 列表
 * @param {Object} options - 处理选项
 * @returns {Promise<Array<Object>>} 处理结果列表
 */
async function batchProcessLinks(urls, options = {}) {
  console.log(`🔄 开始批量处理 ${urls.length} 条链接...`);
  
  const results = [];
  
  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    console.log(`\n[${i + 1}/${urls.length}] 处理：${url}`);
    
    const result = await processLink(url, options);
    results.push(result);
    
    // 延迟避免反爬
    if (i < urls.length - 1) {
      await new Promise(resolve => setTimeout(resolve, CONFIG.requestDelay));
    }
  }
  
  const successCount = results.filter(r => r.success).length;
  console.log(`\n📊 完成：成功 ${successCount} 条，失败 ${urls.length - successCount} 条`);
  
  return results;
}

/**
 * 解析命令
 * @param {string} command - 用户命令
 * @returns {Object} 解析结果
 */
function parseCommand(command) {
  const trimmed = command.trim();
  
  // 搜索命令
  if (trimmed.startsWith('/kb search') || trimmed.startsWith('/kb 搜索')) {
    const query = trimmed.replace(/^\/kb\s+(search|搜索)\s+/, '');
    return { action: 'search', query };
  }
  
  // 列出命令
  if (trimmed.startsWith('/kb list') || trimmed.startsWith('/kb 列表')) {
    const category = trimmed.replace(/^\/kb\s+(list|列表)\s+/, '').trim() || null;
    return { action: 'list', category };
  }
  
  // 查看详情
  if (trimmed.startsWith('/kb view') || trimmed.startsWith('/kb 查看')) {
    const entryId = trimmed.replace(/^\/kb\s+(view|查看)\s+/, '').trim();
    return { action: 'view', entryId };
  }
  
  // 删除
  if (trimmed.startsWith('/kb delete') || trimmed.startsWith('/kb 删除')) {
    const entryId = trimmed.replace(/^\/kb\s+(delete|删除)\s+/, '').trim();
    return { action: 'delete', entryId };
  }
  
  // 统计
  if (trimmed === '/kb stats' || trimmed === '/kb 统计') {
    return { action: 'stats' };
  }
  
  // 导出
  if (trimmed.startsWith('/kb export') || trimmed.startsWith('/kb 导出')) {
    const format = trimmed.split(/\s+/)[2] || 'markdown';
    return { action: 'export', format };
  }
  
  // 最近添加
  if (trimmed === '/kb recent' || trimmed === '/kb 最近') {
    return { action: 'recent' };
  }
  
  // 帮助
  if (trimmed === '/kb help' || trimmed === '/kb 帮助') {
    return { action: 'help' };
  }
  
  return null;
}

/**
 * 执行命令
 * @param {string} command - 用户命令
 * @returns {Promise<Object>} 执行结果
 */
async function executeCommand(command) {
  const parsed = parseCommand(command);
  
  if (!parsed) {
    return { success: false, message: '未知命令，使用 /kb help 查看帮助' };
  }
  
  switch (parsed.action) {
    case 'search':
      const results = searchKnowledge(parsed.query);
      return {
        success: true,
        action: 'search',
        query: parsed.query,
        results,
        count: results.length
      };
      
    case 'list':
      const entries = listKnowledge(parsed.category);
      return {
        success: true,
        action: 'list',
        category: parsed.category || '全部',
        entries,
        count: entries.length
      };
      
    case 'view':
      const entry = viewEntry(parsed.entryId);
      if (entry) {
        return { success: true, action: 'view', entry };
      } else {
        return { success: false, message: '未找到该条目' };
      }
      
    case 'delete':
      const deleteResult = deleteEntry(parsed.entryId);
      if (deleteResult.success) {
        return { success: true, action: 'delete', deletedEntry: deleteResult.deletedEntry };
      } else {
        return { success: false, message: '删除失败：' + deleteResult.reason };
      }
      
    case 'stats':
      const stats = getStats();
      return { success: true, action: 'stats', stats };
      
    case 'export':
      const exported = exportKnowledge(parsed.format);
      return { success: true, action: 'export', format: parsed.format, content: exported };
      
    case 'recent':
      const recent = query.getRecentEntries(10, CONFIG);
      return { success: true, action: 'recent', entries: recent };
      
    case 'help':
      return {
        success: true,
        action: 'help',
        message: `
📚 Knowledge Curator 帮助

保存内容:
  直接发送链接即可自动保存
  或：保存到 [分类]: [链接]

查询命令:
  /kb search <关键词>  - 搜索内容
  /kb list [分类]      - 列出内容
  /kb view <ID>        - 查看详情
  /kb recent           - 最近添加
  /kb stats            - 统计信息
  /kb delete <ID>      - 删除条目
  /kb export [格式]    - 导出知识库
  /kb help             - 显示帮助

分类：科技、生活、学习、娱乐、工作、健康
        `
      };
      
    default:
      return { success: false, message: '未知命令' };
  }
}

// 导出模块
module.exports = {
  processLink,
  searchKnowledge,
  listKnowledge,
  viewEntry,
  deleteEntry,
  getStats,
  exportKnowledge,
  batchProcessLinks,
  executeCommand,
  parseCommand,
  CONFIG
};

// CLI 模式
if (require.main === module) {
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  if (command === 'process' && args[0]) {
    processLink(args[0])
      .then(result => {
        console.log('\n=== 处理结果 ===');
        console.log(JSON.stringify(result, null, 2));
      })
      .catch(err => {
        console.error('错误:', err.message);
        process.exit(1);
      });
  } else if (command === 'search' && args[0]) {
    const results = searchKnowledge(args[0]);
    console.log(`\n=== 搜索结果 (${results.length}条) ===`);
    for (const r of results.slice(0, 10)) {
      console.log(`[${r.category}] ${r.title} (分数：${r.score})`);
    }
  } else if (command === 'stats') {
    const stats = getStats();
    console.log('\n=== 知识库统计 ===');
    console.log(`总数：${stats.total}`);
    console.log('分类:', stats.byCategory);
  } else if (command === 'help' || !command) {
    console.log(`
Knowledge Curator CLI

用法:
  node main.js process <URL>     - 处理链接
  node main.js search <关键词>    - 搜索
  node main.js stats             - 统计
  node main.js help              - 帮助
    `);
  }
}
