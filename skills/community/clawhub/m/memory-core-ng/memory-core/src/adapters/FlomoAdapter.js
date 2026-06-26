/**
 * 🎯 Flomo 笔记适配器
 * 将 Flomo 导出文件解析并导入到 MemoryService
 */

const fs = require('fs');
const path = require('path');
// const { JSDOM } = require('jsdom');

class FlomoAdapter {
  constructor(config = {}) {
    this.config = {
      parseTags: config.parseTags !== false,
      extractDates: config.extractDates !== false,
      defaultCategory: config.defaultCategory || '未分类',
      verbose: config.verbose || false,
      ...config
    };
    
    this.stats = {
      totalNotes: 0,
      successfullyParsed: 0,
      failedParsed: 0,
      tagsFound: new Map(),
      categoriesFound: new Map()
    };
    
    this.log('🚀 FlomoAdapter initialized');
  }
  
  /**
   * 解析 Flomo HTML 导出文件
   */
  async parseExport(htmlContent, options = {}) {
    if (!htmlContent || typeof htmlContent !== 'string') {
      throw new Error('HTML content must be a non-empty string');
    }
    
    this.log('📝 Parsing Flomo export...');
    
    try {
      const dom = new JSDOM(htmlContent);
      const document = dom.window.document;
      
      // 查找所有 memo 元素（Flomo 导出格式）
      const memoElements = document.querySelectorAll('.memo, [class*="memo"], .note, .item');
      
      this.stats.totalNotes = memoElements.length;
      this.log(`   Found ${this.stats.totalNotes} potential notes`);
      
      const notes = [];
      
      for (let i = 0; i < memoElements.length; i++) {
        try {
          const memoElement = memoElements[i];
          const note = this._parseMemoElement(memoElement, i);
          
          if (note && note.content && note.content.trim()) {
            notes.push(note);
            this.stats.successfullyParsed++;
            
            // 统计标签
            if (note.tags && note.tags.length > 0) {
              note.tags.forEach(tag => {
                const count = this.stats.tagsFound.get(tag) || 0;
                this.stats.tagsFound.set(tag, count + 1);
              });
            }
            
            // 统计分类
            if (note.category) {
              const count = this.stats.categoriesFound.get(note.category) || 0;
              this.stats.categoriesFound.set(note.category, count + 1);
            }
          }
        } catch (error) {
          this.stats.failedParsed++;
          this.log(`⚠️  Failed to parse note ${i}: ${error.message}`);
        }
      }
      
      this.log(`✅ Parsed ${notes.length}/${this.stats.totalNotes} notes successfully`);
      
      // 生成分类统计
      const tagStats = Array.from(this.stats.tagsFound.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20);
      
      const categoryStats = Array.from(this.stats.categoriesFound.entries())
        .sort((a, b) => b[1] - a[1]);
      
      return {
        success: true,
        notes,
        stats: {
          totalNotes: this.stats.totalNotes,
          successfullyParsed: this.stats.successfullyParsed,
          failedParsed: this.stats.failedParsed,
          tagStats,
          categoryStats,
          topTags: tagStats.slice(0, 10).map(([tag, count]) => ({ tag, count })),
          topCategories: categoryStats.slice(0, 10).map(([category, count]) => ({ category, count }))
        }
      };
      
    } catch (error) {
      this.log(`❌ Failed to parse Flomo export: ${error.message}`);
      return {
        success: false,
        error: error.message,
        notes: [],
        stats: this.stats
      };
    }
  }
  
  /**
   * 解析单个 memo 元素
   */
  _parseMemoElement(element, index) {
    // 尝试多种选择器获取内容
    const contentSelectors = [
      '.content', '.text', '.memo-content', '.note-content',
      'p', 'div[class*="content"]', 'span[class*="text"]'
    ];
    
    let content = '';
    let date = null;
    let tags = [];
    
    // 1. 获取内容
    for (const selector of contentSelectors) {
      const contentElement = element.querySelector(selector);
      if (contentElement && contentElement.textContent && contentElement.textContent.trim()) {
        content = contentElement.textContent.trim();
        break;
      }
    }
    
    // 如果没有找到，使用元素的文本内容
    if (!content) {
      content = element.textContent.trim();
    }
    
    // 2. 提取日期
    if (this.config.extractDates) {
      // 查找日期元素或从内容中提取
      const dateSelectors = ['.date', '.time', '.created-at', '.timestamp'];
      for (const selector of dateSelectors) {
        const dateElement = element.querySelector(selector);
        if (dateElement && dateElement.textContent) {
          date = this._parseDate(dateElement.textContent);
          if (date) break;
        }
      }
      
      // 如果没有找到，尝试从内容中提取
      if (!date) {
        date = this._extractDateFromContent(content);
      }
    }
    
    // 3. 提取标签
    if (this.config.parseTags) {
      // 从内容中提取 #标签
      const tagMatches = content.match(/#[\p{L}\p{N}_-]+/gu) || [];
      tags = tagMatches.map(tag => tag.substring(1)); // 去掉 #
      
      // 从元素中查找标签
      const tagElements = element.querySelectorAll('.tag, [class*="tag"], .label');
      tagElements.forEach(tagElement => {
        if (tagElement.textContent) {
          const tagText = tagElement.textContent.trim();
          if (tagText && !tags.includes(tagText)) {
            tags.push(tagText);
          }
        }
      });
    }
    
    // 4. 确定分类
    let category = this.config.defaultCategory;
    if (tags.length > 0) {
      // 使用第一个标签作为分类（如果标签看起来像分类）
      const primaryTag = tags[0];
      if (this._looksLikeCategory(primaryTag)) {
        category = primaryTag;
      }
    }
    
    return {
      id: `flomo-${index}-${Date.now()}`,
      content,
      originalContent: content,
      date: date || new Date(),
      tags,
      category,
      metadata: {
        source: 'flomo',
        index,
        hasTags: tags.length > 0,
        contentLength: content.length,
        extractedAt: new Date()
      }
    };
  }
  
  /**
   * 解析日期字符串
   */
  _parseDate(dateString) {
    try {
      // 尝试多种日期格式
      const parsed = new Date(dateString);
      if (!isNaN(parsed.getTime())) {
        return parsed;
      }
    } catch (error) {
      // 忽略解析错误
    }
    return null;
  }
  
  /**
   * 从内容中提取日期
   */
  _extractDateFromContent(content) {
    // 常见日期格式的正则表达式
    const datePatterns = [
      /\d{4}[-/]\d{1,2}[-/]\d{1,2}/,  // YYYY-MM-DD
      /\d{1,2}[-/]\d{1,2}[-/]\d{4}/,  // DD-MM-YYYY
      /\d{4}年\d{1,2}月\d{1,2}日/,     // 中文日期
    ];
    
    for (const pattern of datePatterns) {
      const match = content.match(pattern);
      if (match) {
        try {
          const parsed = new Date(match[0].replace(/[年月日]/g, '-'));
          if (!isNaN(parsed.getTime())) {
            return parsed;
          }
        } catch (error) {
          // 忽略解析错误
        }
      }
    }
    
    return null;
  }
  
  /**
   * 判断标签是否像分类
   */
  _looksLikeCategory(tag) {
    // 常见的分类标签
    const commonCategories = [
      '投资', '理财', '股票', '基金', 'crypto', '加密货币',
      '技术', '编程', '代码', '开发',
      '读书', '阅读', '学习', '教育',
      '生活', '日常', '随笔', '思考',
      '工作', '职业', '职场', '项目'
    ];
    
    return commonCategories.some(category => 
      tag.toLowerCase().includes(category.toLowerCase()) ||
      category.toLowerCase().includes(tag.toLowerCase())
    );
  }
  
  /**
   * 导入到 MemoryService
   */
  async importToMemory(notes, memoryService, options = {}) {
    if (!notes || !Array.isArray(notes)) {
      throw new Error('Notes must be an array');
    }
    
    if (!memoryService || typeof memoryService.add !== 'function') {
      throw new Error('Valid MemoryService is required');
    }
    
    const {
      batchSize = 10,
      delayBetweenBatches = 1000,
      skipDuplicates = true,
      ...importOptions
    } = options;
    
    this.log(`📤 Importing ${notes.length} notes to MemoryService...`);
    
    const results = {
      total: notes.length,
      successful: 0,
      failed: 0,
      skipped: 0,
      importedNotes: [],
      errors: []
    };
    
    // 分批处理以避免内存和 API 限制
    for (let i = 0; i < notes.length; i += batchSize) {
      const batch = notes.slice(i, i + batchSize);
      this.log(`   Processing batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(notes.length / batchSize)} (${batch.length} notes)`);
      
      const batchPromises = batch.map(async (note, batchIndex) => {
        try {
          // 检查是否跳过重复项
          if (skipDuplicates) {
            // 这里可以添加重复检查逻辑
            // 暂时跳过
          }
          
          // 准备元数据
          const metadata = {
            ...note.metadata,
            source: 'flomo',
            originalId: note.id,
            tags: note.tags,
            category: note.category,
            importDate: new Date()
          };
          
          // 添加记忆
          const memory = await memoryService.add(note.content, metadata);
          
          results.successful++;
          results.importedNotes.push({
            originalId: note.id,
            memoryId: memory.id,
            contentPreview: note.content.substring(0, 50) + '...'
          });
          
          return { success: true, note, memory };
          
        } catch (error) {
          results.failed++;
          results.errors.push({
            noteId: note.id,
            error: error.message,
            contentPreview: note.content.substring(0, 30) + '...'
          });
          
          this.log(`⚠️  Failed to import note ${i + batchIndex}: ${error.message}`);
          return { success: false, note, error };
        }
      });
      
      // 等待当前批次完成
      await Promise.all(batchPromises);
      
      // 批次间延迟
      if (i + batchSize < notes.length && delayBetweenBatches > 0) {
        await new Promise(resolve => setTimeout(resolve, delayBetweenBatches));
      }
    }
    
    this.log(`✅ Import completed: ${results.successful} successful, ${results.failed} failed`);
    
    return {
      ...results,
      stats: this.getStats()
    };
  }
  
  /**
   * 从文件读取并解析
   */
  async parseFromFile(filePath, options = {}) {
    try {
      this.log(`📄 Reading Flomo export from: ${filePath}`);
      
      const htmlContent = fs.readFileSync(filePath, 'utf8');
      return await this.parseExport(htmlContent, options);
      
    } catch (error) {
      this.log(`❌ Failed to read file: ${error.message}`);
      return {
        success: false,
        error: error.message,
        notes: [],
        stats: this.stats
      };
    }
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return { ...this.stats };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalNotes: 0,
      successfullyParsed: 0,
      failedParsed: 0,
      tagsFound: new Map(),
      categoriesFound: new Map()
    };
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log('[FlomoAdapter]', ...args);
    }
  }
}

module.exports = FlomoAdapter;
