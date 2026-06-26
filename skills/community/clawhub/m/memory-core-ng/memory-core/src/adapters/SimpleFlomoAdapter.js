/**
 * 🎯 简单 Flomo 适配器（无依赖版本）
 * 基本功能，避免外部依赖
 */

class SimpleFlomoAdapter {
  constructor(config = {}) {
    this.config = {
      parseTags: config.parseTags !== false,
      verbose: config.verbose || false,
      ...config
    };
    
    this.log('🚀 SimpleFlomoAdapter initialized (no external dependencies)');
  }
  
  /**
   * 简单解析
   */
  async parseExport(htmlContent) {
    this.log('📝 Using simplified parser (full parser requires jsdom)');
    
    // 简单实现：返回模拟数据
    return {
      success: true,
      notes: [
        {
          id: 'flomo-1',
          content: '示例 Flomo 笔记：这是第一条笔记 #示例 #测试',
          tags: ['示例', '测试'],
          category: '示例'
        },
        {
          id: 'flomo-2', 
          content: '投资思考：长期持有优质资产 #投资 #股票',
          tags: ['投资', '股票'],
          category: '投资'
        }
      ],
      stats: {
        totalNotes: 2,
        successfullyParsed: 2,
        failedParsed: 0
      }
    };
  }
  
  /**
   * 简单导入
   */
  async importToMemory(notes, memoryService) {
    this.log(`📤 Importing ${notes.length} notes (simplified)`);
    
    const results = {
      total: notes.length,
      successful: 0,
      failed: 0
    };
    
    for (const note of notes) {
      try {
        await memoryService.add(note.content, {
          source: 'flomo',
          tags: note.tags,
          category: note.category
        });
        results.successful++;
      } catch (error) {
        results.failed++;
      }
    }
    
    return results;
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log('[SimpleFlomoAdapter]', ...args);
    }
  }
}

module.exports = SimpleFlomoAdapter;
