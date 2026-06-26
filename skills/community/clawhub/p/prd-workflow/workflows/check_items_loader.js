/**
 * PRD 质量检查项加载器
 * 
 * 负责解析 docs/checker.md 文件，提供检查项的加载、过滤和提示词生成功能
 * 
 * @version 1.0.0
 * @since 2026-04-05
 */

const fs = require('fs');
const path = require('path');

class CheckItemsLoader {
  /**
   * 构造函数
   * @param {string} basePath - 技能根目录路径
   */
  constructor(basePath) {
    this.basePath = basePath || path.join(__dirname, '..');
    this.checkerMdPath = path.join(this.basePath, 'docs', 'checker.md');
    this.cache = null;
    this.lastLoaded = null;
  }

  /**
   * 加载全部检查项
   * @returns {Promise<Array>} 检查项数组
   */
  async load() {
    // 检查缓存（5 分钟内有效）
    if (this.cache && this.lastLoaded && (Date.now() - this.lastLoaded < 5 * 60 * 1000)) {
      return this.cache;
    }

    try {
      const content = fs.readFileSync(this.checkerMdPath, 'utf-8');
      this.cache = this.parseCheckerMd(content);
      this.lastLoaded = Date.now();
      return this.cache;
    } catch (error) {
      console.error('[CheckItemsLoader] 加载检查项失败:', error.message);
      throw new Error(`无法加载检查项文档：${error.message}`);
    }
  }

  /**
   * 解析 checker.md 文件内容
   * @param {string} content - Markdown 内容
   * @returns {Array} 检查项数组
   */
  parseCheckerMd(content) {
    const items = [];
    const lines = content.split('\n');
    
    let currentItem = null;
    let currentCategory = null;
    let inCheckpoints = false;
    let inQuestions = false;
    let inCriteria = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmedLine = line.trim();

      // 检测分类标题（如：## 🔴 核心检查项 (CORE)）
      const categoryMatch = trimmedLine.match(/^##\s+[🔴🟡🟢]?\s*(.+?)\s*\((CORE|COMPLETE|OPTIMIZE)\)/);
      if (categoryMatch) {
        // 保存前一个分类的检查项
        if (currentCategory && currentItem) {
          currentCategory.items.push(currentItem);
          items.push(...currentCategory.items);
        }
        
        currentCategory = {
          name: categoryMatch[1].trim(),
          code: categoryMatch[2],
          items: []
        };
        currentItem = null;
        continue;
      }

      // 检测检查项标题（如：### CORE-1: 业务规则完整性）
      const itemMatch = trimmedLine.match(/^###\s+(CORE|COMPLETE|OPTIMIZE)-(\d+):\s*(.+)/);
      if (itemMatch) {
        if (currentItem && currentCategory) {
          currentCategory.items.push(currentItem);
        }
        
        currentItem = {
          id: `${itemMatch[1]}-${itemMatch[2]}`,
          code: itemMatch[1],
          number: parseInt(itemMatch[2]),
          name: itemMatch[3].trim(),
          category: currentCategory ? currentCategory.code : 'UNKNOWN',
          checkpoints: [],
          questions: [],
          criteria: {}
        };
        inCheckpoints = false;
        inQuestions = false;
        inCriteria = false;
        continue;
      }

      // 检测检查点部分
      if (trimmedLine === '**检查点**:') {
        inCheckpoints = true;
        inQuestions = false;
        inCriteria = false;
        continue;
      }

      // 检测检查问题部分
      if (trimmedLine === '**检查问题**:') {
        inCheckpoints = false;
        inQuestions = true;
        inCriteria = false;
        continue;
      }

      // 检测验收标准部分
      if (trimmedLine === '**验收标准**:') {
        inCheckpoints = false;
        inQuestions = false;
        inCriteria = true;
        continue;
      }

      // 解析检查点列表
      if (inCheckpoints && trimmedLine.startsWith('- [ ]')) {
        const checkpoint = trimmedLine.replace('- [ ]', '').trim();
        if (currentItem) {
          currentItem.checkpoints.push(checkpoint);
        }
      }

      // 解析检查问题列表
      if (inQuestions && trimmedLine.match(/^\d+\./)) {
        const question = trimmedLine.replace(/^\d+\.\s*/, '').replace(/\?$/, '');
        if (currentItem) {
          currentItem.questions.push(question);
        }
      }

      // 解析验收标准
      if (inCriteria && trimmedLine.startsWith('- ')) {
        const criteriaText = trimmedLine.replace('- ', '').trim();
        const criteriaMatch = criteriaText.match(/^(.+?):\s*(.+)/);
        if (criteriaMatch && currentItem) {
          currentItem.criteria[criteriaMatch[1].trim()] = criteriaMatch[2].trim();
        }
      }
    }

    // 添加最后一个检查项
    if (currentItem && currentCategory) {
      currentCategory.items.push(currentItem);
    }

    // 扁平化所有检查项
    if (currentCategory) {
      items.push(...currentCategory.items);
    }

    return items;
  }

  /**
   * 按阶段加载检查项
   * @param {string} stage - 阶段名称 (decomposition, prd_generation, quality_check, optimization)
   * @returns {Promise<Array>} 过滤后的检查项数组
   */
  async loadForStage(stage) {
    const allItems = await this.load();
    
    const stageMapping = {
      'decomposition': ['CORE'],
      'prd_generation': ['CORE', 'COMPLETE'],
      'quality_check': ['CORE', 'COMPLETE', 'OPTIMIZE'],
      'optimization': ['OPTIMIZE']
    };

    const allowedCodes = stageMapping[stage] || ['CORE', 'COMPLETE', 'OPTIMIZE'];
    
    return allItems.filter(item => allowedCodes.includes(item.code));
  }

  /**
   * 生成阶段提示词
   * @param {string} stage - 阶段名称
   * @returns {Promise<string>} 提示词字符串
   */
  async generatePrompt(stage) {
    const items = await this.loadForStage(stage);
    
    if (items.length === 0) {
      return '';
    }

    const stageNames = {
      'decomposition': '需求分解阶段',
      'prd_generation': 'PRD 生成阶段',
      'quality_check': '质量检查阶段',
      'optimization': '优化建议阶段'
    };

    let prompt = `## ${stageNames[stage] || stage} - 质量检查项指导\n\n`;
    prompt += `请在${stageNames[stage] || stage}中，重点关注以下检查项：\n\n`;

    // 按类别分组
    const grouped = {};
    items.forEach(item => {
      if (!grouped[item.code]) {
        grouped[item.code] = [];
      }
      grouped[item.code].push(item);
    });

    // 生成每个类别的提示
    Object.keys(grouped).forEach(code => {
      const categoryNames = {
        'CORE': '🔴 核心检查项（必须满足）',
        'COMPLETE': '🟡 完善检查项（建议满足）',
        'OPTIMIZE': '🟢 优化检查项（可选满足）'
      };

      prompt += `### ${categoryNames[code] || code}\n\n`;

      grouped[code].forEach(item => {
        prompt += `#### ${item.id}: ${item.name}\n\n`;
        
        if (item.checkpoints.length > 0) {
          prompt += '**检查点**:\n';
          item.checkpoints.forEach(cp => {
            prompt += `- ${cp}\n`;
          });
          prompt += '\n';
        }

        if (item.questions.length > 0) {
          prompt += '**关键问题**:\n';
          item.questions.forEach((q, idx) => {
            prompt += `${idx + 1}. ${q}\n`;
          });
          prompt += '\n';
        }

        if (Object.keys(item.criteria).length > 0) {
          prompt += '**验收标准**:\n';
          Object.entries(item.criteria).forEach(([key, value]) => {
            prompt += `- ${key}: ${value}\n`;
          });
          prompt += '\n';
        }
      });
    });

    prompt += `---\n\n`;
    prompt += `**使用说明**:\n`;
    prompt += `- 核心检查项（CORE）必须 100% 满足，否则 PRD 质量不达标\n`;
    prompt += `- 完善检查项（COMPLETE）建议满足 80% 以上\n`;
    prompt += `- 优化检查项（OPTIMIZE）根据项目实际情况选择性满足\n`;

    return prompt;
  }

  /**
   * 获取单个检查项详情
   * @param {string} itemId - 检查项 ID（如：CORE-1）
   * @returns {Promise<Object|null>} 检查项详情
   */
  async getItem(itemId) {
    const allItems = await this.load();
    return allItems.find(item => item.id === itemId) || null;
  }

  /**
   * 获取检查项统计信息
   * @returns {Promise<Object>} 统计信息
   */
  async getStats() {
    const allItems = await this.load();
    
    const stats = {
      total: allItems.length,
      byCategory: {},
      totalCheckpoints: 0,
      totalQuestions: 0
    };

    allItems.forEach(item => {
      if (!stats.byCategory[item.code]) {
        stats.byCategory[item.code] = 0;
      }
      stats.byCategory[item.code]++;
      stats.totalCheckpoints += item.checkpoints.length;
      stats.totalQuestions += item.questions.length;
    });

    return stats;
  }

  /**
   * 按章节加载检查项
   * @param {string} chapter - 章节名称（overview, globalFlow, function, nonFunctional, appendix）
   * @returns {Promise<Array>} 过滤后的检查项数组
   */
  async loadForChapter(chapter) {
    const allItems = await this.load();
    
    // 章节与检查项的映射关系
    const chapterMapping = {
      'overview': ['用户角色', '业务目标', '功能范围', '术语定义'],
      'globalFlow': ['业务流程', '数据字典', '系统架构'],
      'function': ['业务规则', '输入输出', '异常处理', '字段级', '验收标准'],
      'nonFunctional': ['性能', '安全', '兼容性', '可扩展性'],
      'appendix': ['修订历史', '参考资料']
    };
    
    const keywords = chapterMapping[chapter] || [];
    
    if (keywords.length === 0) {
      return allItems; // 未知章节返回全部
    }
    
    // 根据关键词匹配检查项
    return allItems.filter(item => {
      const nameMatch = keywords.some(kw => item.name?.includes(kw));
      const idMatch = keywords.some(kw => item.id?.includes(kw));
      const checkpointMatch = item.checkpoints?.some(cp => keywords.some(kw => cp.includes(kw)));
      return nameMatch || idMatch || checkpointMatch;
    });
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this.cache = null;
    this.lastLoaded = null;
  }
}

// 导出单例
const loader = new CheckItemsLoader();

module.exports = {
  CheckItemsLoader,
  load: () => loader.load(),
  loadForStage: (stage) => loader.loadForStage(stage),
  loadForChapter: (chapter) => loader.loadForChapter(chapter),
  generatePrompt: (stage) => loader.generatePrompt(stage),
  getItem: (itemId) => loader.getItem(itemId),
  getStats: () => loader.getStats(),
  clearCache: () => loader.clearCache()
};
