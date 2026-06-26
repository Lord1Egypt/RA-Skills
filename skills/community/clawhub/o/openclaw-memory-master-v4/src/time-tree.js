/**
 * Memory-Master v3.0.0 - 时间树结构
 * 实现自然时间查询：今天、昨天、本周、上周、这个月等
 */

const fs = require('fs');
const path = require('path');

// 时间表达式映射
const TimeExpressions = {
  // 相对时间
  '今天': { type: 'day', offset: 0 },
  '今天': { type: 'day', offset: 0 },
  '今日': { type: 'day', offset: 0 },
  '昨天': { type: 'day', offset: -1 },
  '昨日': { type: 'day', offset: -1 },
  '前天': { type: 'day', offset: -2 },
  '明天': { type: 'day', offset: 1 },
  '明日': { type: 'day', offset: 1 },
  '后天': { type: 'day', offset: 2 },
  
  // 周
  '本周': { type: 'week', offset: 0 },
  '这周': { type: 'week', offset: 0 },
  '上周': { type: 'week', offset: -1 },
  '上个星期': { type: 'week', offset: -1 },
  '下周': { type: 'week', offset: 1 },
  '下个星期': { type: 'week', offset: 1 },
  
  // 月
  '本月': { type: 'month', offset: 0 },
  '这个月': { type: 'month', offset: 0 },
  '上月': { type: 'month', offset: -1 },
  '上个月': { type: 'month', offset: -1 },
  '下月': { type: 'month', offset: 1 },
  '下个月': { type: 'month', offset: 1 },
  
  // 年
  '今年': { type: 'year', offset: 0 },
  '这一年': { type: 'year', offset: 0 },
  '去年': { type: 'year', offset: -1 },
  '明年': { type: 'year', offset: 1 },
  
  // 模糊时间
  '最近': { type: 'recent', days: 7 },
  '近期': { type: 'recent', days: 14 },
  '最近一周': { type: 'recent', days: 7 },
  '最近两周': { type: 'recent', days: 14 },
  '最近一个月': { type: 'recent', days: 30 },
  '前段时间': { type: 'recent', days: 30 }
};

// 星期映射
const WeekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

class TimeTree {
  constructor(baseDir = null) {
    this.baseDir = baseDir || path.join(process.cwd(), 'memory', 'time-tree');
    this.ensureDirectoryStructure();
  }

  /**
   * 确保目录结构存在
   */
  ensureDirectoryStructure() {
    const dirs = [
      this.baseDir,
      path.join(this.baseDir, 'years'),
      path.join(this.baseDir, 'months'),
      path.join(this.baseDir, 'days'),
      path.join(this.baseDir, 'sessions')
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  /**
   * 解析自然语言时间表达式
   * @param {string} expression - 时间表达式，如"今天"、"上周"、"这个月"
   * @param {Date} referenceDate - 参考日期（默认为今天）
   * @returns {object} 时间范围
   */
  parseTimeExpression(expression, referenceDate = new Date()) {
    // 移除空格和标点
    const normalized = expression.trim().replace(/[,.!?]/g, '');
    
    // 查找匹配的时间表达式
    const timeConfig = TimeExpressions[normalized];
    
    if (!timeConfig) {
      // 尝试解析具体日期
      return this.parseSpecificDate(normalized, referenceDate);
    }

    // 根据类型计算时间范围
    switch (timeConfig.type) {
      case 'day':
        return this.calculateDayRange(referenceDate, timeConfig.offset);
      case 'week':
        return this.calculateWeekRange(referenceDate, timeConfig.offset);
      case 'month':
        return this.calculateMonthRange(referenceDate, timeConfig.offset);
      case 'year':
        return this.calculateYearRange(referenceDate, timeConfig.offset);
      case 'recent':
        return this.calculateRecentRange(referenceDate, timeConfig.days);
      default:
        return null;
    }
  }

  /**
   * 解析具体日期
   */
  parseSpecificDate(normalized, referenceDate) {
    // 尝试解析 YYYY-MM-DD 格式
    const dateMatch = normalized.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
    if (dateMatch) {
      const date = new Date(parseInt(dateMatch[1]), parseInt(dateMatch[2]) - 1, parseInt(dateMatch[3]));
      return {
        type: 'day',
        start: this.startOfDay(date),
        end: this.endOfDay(date),
        expression: normalized
      };
    }

    // 尝试解析"周一"、"周二"等
    const weekDayMatch = normalized.match(/周 ([一二三四五六日天])/);
    if (weekDayMatch) {
      const dayMap = { '日': 0, '天': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6 };
      const targetDay = dayMap[weekDayMatch[1]];
      const currentDay = referenceDate.getDay();
      let offset = targetDay - currentDay;
      
      // 如果是未来的日期，默认指上周
      if (offset > 0) {
        offset -= 7;
      }
      
      const targetDate = new Date(referenceDate);
      targetDate.setDate(referenceDate.getDate() + offset);
      
      return {
        type: 'day',
        start: this.startOfDay(targetDate),
        end: this.endOfDay(targetDate),
        expression: normalized
      };
    }

    return null;
  }

  /**
   * 计算日期范围
   */
  calculateDayRange(referenceDate, offset) {
    const targetDate = new Date(referenceDate);
    targetDate.setDate(referenceDate.getDate() + offset);
    
    return {
      type: 'day',
      start: this.startOfDay(targetDate),
      end: this.endOfDay(targetDate),
      expression: offset === 0 ? '今天' : offset === -1 ? '昨天' : `偏移${offset}天`
    };
  }

  /**
   * 计算周范围
   */
  calculateWeekRange(referenceDate, offset) {
    const targetDate = new Date(referenceDate);
    targetDate.setDate(referenceDate.getDate() + (offset * 7));
    
    const dayOfWeek = targetDate.getDay();
    const startOfWeek = new Date(targetDate);
    startOfWeek.setDate(targetDate.getDate() - dayOfWeek);
    
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);
    
    return {
      type: 'week',
      start: this.startOfDay(startOfWeek),
      end: this.endOfDay(endOfWeek),
      expression: offset === 0 ? '本周' : offset === -1 ? '上周' : `偏移${offset}周`
    };
  }

  /**
   * 计算月范围
   */
  calculateMonthRange(referenceDate, offset) {
    const targetDate = new Date(referenceDate);
    targetDate.setMonth(referenceDate.getMonth() + offset);
    
    const startOfMonth = new Date(targetDate.getFullYear(), targetDate.getMonth(), 1);
    const endOfMonth = new Date(targetDate.getFullYear(), targetDate.getMonth() + 1, 0);
    
    return {
      type: 'month',
      start: this.startOfDay(startOfMonth),
      end: this.endOfDay(endOfMonth),
      expression: offset === 0 ? '本月' : offset === -1 ? '上月' : `偏移${offset}月`
    };
  }

  /**
   * 计算年范围
   */
  calculateYearRange(referenceDate, offset) {
    const targetDate = new Date(referenceDate);
    targetDate.setFullYear(referenceDate.getFullYear() + offset);
    
    const startOfYear = new Date(targetDate.getFullYear(), 0, 1);
    const endOfYear = new Date(targetDate.getFullYear(), 11, 31);
    
    return {
      type: 'year',
      start: this.startOfDay(startOfYear),
      end: this.endOfDay(endOfYear),
      expression: offset === 0 ? '今年' : offset === -1 ? '去年' : `偏移${offset}年`
    };
  }

  /**
   * 计算最近范围
   */
  calculateRecentRange(referenceDate, days) {
    const startDate = new Date(referenceDate);
    startDate.setDate(referenceDate.getDate() - days);
    
    return {
      type: 'recent',
      start: this.startOfDay(startDate),
      end: this.endOfDay(referenceDate),
      expression: `最近${days}天`
    };
  }

  /**
   * 获取一天的开始
   */
  startOfDay(date) {
    const result = new Date(date);
    result.setHours(0, 0, 0, 0);
    return result;
  }

  /**
   * 获取一天的结束
   */
  endOfDay(date) {
    const result = new Date(date);
    result.setHours(23, 59, 59, 999);
    return result;
  }

  /**
   * 格式化日期为存储键
   */
  formatDateKey(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  /**
   * 格式化周键
   */
  formatWeekKey(date) {
    const year = date.getFullYear();
    const weekNumber = this.getWeekNumber(date);
    return `${year}-W${String(weekNumber).padStart(2, '0')}`;
  }

  /**
   * 格式化月键
   */
  formatMonthKey(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    return `${year}-${month}`;
  }

  /**
   * 获取周数
   */
  getWeekNumber(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
  }

  /**
   * 检测文本中的时间表达式
   * @param {string} text - 输入文本
   * @returns {array} 检测到的时间表达式列表
   */
  detectTimeExpressions(text) {
    const expressions = [];
    
    // 检测预定义的时间表达式
    for (const expr of Object.keys(TimeExpressions)) {
      if (text.includes(expr)) {
        expressions.push({
          expression: expr,
          type: TimeExpressions[expr].type,
          position: text.indexOf(expr)
        });
      }
    }

    // 检测日期格式
    const dateRegex = /\d{4}[-/]\d{1,2}[-/]\d{1,2}/g;
    let match;
    while ((match = dateRegex.exec(text)) !== null) {
      expressions.push({
        expression: match[0],
        type: 'specific_date',
        position: match.index
      });
    }

    // 检测星期
    const weekDayRegex = /周 ([一二三四五六日天])/g;
    while ((match = weekDayRegex.exec(text)) !== null) {
      expressions.push({
        expression: match[0],
        type: 'weekday',
        position: match.index
      });
    }

    return expressions.sort((a, b) => a.position - b.position);
  }

  /**
   * 从文本中提取时间范围
   * @param {string} text - 输入文本
   * @param {Date} referenceDate - 参考日期
   * @returns {object|null} 时间范围
   */
  extractTimeRange(text, referenceDate = new Date()) {
    const expressions = this.detectTimeExpressions(text);
    
    if (expressions.length === 0) {
      return null;
    }

    // 使用第一个匹配的时间表达式
    const primaryExpr = expressions[0];
    
    if (primaryExpr.type === 'specific_date') {
      return this.parseSpecificDate(primaryExpr.expression, referenceDate);
    }
    
    return this.parseTimeExpression(primaryExpr.expression, referenceDate);
  }

  /**
   * 存储记忆到时间树
   * @param {string} memoryId - 记忆 ID
   * @param {object} memoryData - 记忆数据
   * @param {Date} memoryDate - 记忆日期
   */
  storeMemory(memoryId, memoryData, memoryDate = new Date()) {
    const dateKey = this.formatDateKey(memoryDate);
    const weekKey = this.formatWeekKey(memoryDate);
    const monthKey = this.formatMonthKey(memoryDate);
    const yearKey = memoryDate.getFullYear().toString();

    // 存储到日索引
    const dayIndexPath = path.join(this.baseDir, 'days', `${dateKey}.json`);
    this.appendIndex(dayIndexPath, memoryId);

    // 存储到周索引
    const weekIndexPath = path.join(this.baseDir, 'weeks', `${weekKey}.json`);
    this.appendIndex(weekIndexPath, memoryId);

    // 存储到月索引
    const monthIndexPath = path.join(this.baseDir, 'months', `${monthKey}.json`);
    this.appendIndex(monthIndexPath, memoryId);

    // 存储到年索引
    const yearIndexPath = path.join(this.baseDir, 'years', `${yearKey}.json`);
    this.appendIndex(yearIndexPath, memoryId);
  }

  /**
   * 追加到索引文件
   */
  appendIndex(filePath, memoryId) {
    let index = { memories: [] };
    
    if (fs.existsSync(filePath)) {
      index = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }

    if (!index.memories.includes(memoryId)) {
      index.memories.push(memoryId);
      fs.writeFileSync(filePath, JSON.stringify(index, null, 2), 'utf8');
    }
  }

  /**
   * 查询时间范围内的记忆
   * @param {string} expression - 时间表达式
   * @param {Date} referenceDate - 参考日期
   * @returns {array} 记忆 ID 列表
   */
  queryByTime(expression, referenceDate = new Date()) {
    const timeRange = this.parseTimeExpression(expression, referenceDate);
    
    if (!timeRange) {
      return [];
    }

    // 根据时间范围类型查询
    switch (timeRange.type) {
      case 'day':
        return this.queryByDay(timeRange.start);
      case 'week':
        return this.queryByWeek(timeRange.start);
      case 'month':
        return this.queryByMonth(timeRange.start);
      case 'year':
        return this.queryByYear(timeRange.start);
      case 'recent':
        return this.queryByRange(timeRange.start, timeRange.end);
      default:
        return [];
    }
  }

  /**
   * 查询指定日期的记忆
   */
  queryByDay(date) {
    const dateKey = this.formatDateKey(date);
    const dayIndexPath = path.join(this.baseDir, 'days', `${dateKey}.json`);
    
    if (!fs.existsSync(dayIndexPath)) {
      return [];
    }

    const index = JSON.parse(fs.readFileSync(dayIndexPath, 'utf8'));
    return index.memories || [];
  }

  /**
   * 查询指定周的记忆
   */
  queryByWeek(date) {
    const weekKey = this.formatWeekKey(date);
    const weekIndexPath = path.join(this.baseDir, 'weeks', `${weekKey}.json`);
    
    if (!fs.existsSync(weekIndexPath)) {
      return [];
    }

    const index = JSON.parse(fs.readFileSync(weekIndexPath, 'utf8'));
    return index.memories || [];
  }

  /**
   * 查询指定月的记忆
   */
  queryByMonth(date) {
    const monthKey = this.formatMonthKey(date);
    const monthIndexPath = path.join(this.baseDir, 'months', `${monthKey}.json`);
    
    if (!fs.existsSync(monthIndexPath)) {
      return [];
    }

    const index = JSON.parse(fs.readFileSync(monthIndexPath, 'utf8'));
    return index.memories || [];
  }

  /**
   * 查询指定年的记忆
   */
  queryByYear(date) {
    const yearKey = date.getFullYear().toString();
    const yearIndexPath = path.join(this.baseDir, 'years', `${yearKey}.json`);
    
    if (!fs.existsSync(yearIndexPath)) {
      return [];
    }

    const index = JSON.parse(fs.readFileSync(yearIndexPath, 'utf8'));
    return index.memories || [];
  }

  /**
   * 查询时间范围内的记忆
   */
  queryByRange(startDate, endDate) {
    const memoryIds = new Set();
    
    // 遍历日期范围
    const current = new Date(startDate);
    while (current <= endDate) {
      const dayMemories = this.queryByDay(new Date(current));
      dayMemories.forEach(id => memoryIds.add(id));
      current.setDate(current.getDate() + 1);
    }

    return Array.from(memoryIds);
  }
}

// 导出
module.exports = {
  TimeExpressions,
  WeekDays,
  TimeTree
};

// CLI 测试
if (require.main === module) {
  const timeTree = new TimeTree();
  
  console.log('⏰ Time Tree Test\n');
  console.log('='.repeat(50));

  const testExpressions = [
    '今天',
    '昨天',
    '本周',
    '上周',
    '这个月',
    '最近一周',
    '2026-04-09',
    '周一'
  ];

  const referenceDate = new Date('2026-04-09');
  console.log(`参考日期：${referenceDate.toISOString().split('T')[0]} (${WeekDays[referenceDate.getDay()]})\n`);

  testExpressions.forEach(expr => {
    const result = timeTree.parseTimeExpression(expr, referenceDate);
    if (result) {
      console.log(`${expr}:`);
      console.log(`  类型：${result.type}`);
      console.log(`  开始：${result.start.toISOString().split('T')[0]}`);
      console.log(`  结束：${result.end.toISOString().split('T')[0]}`);
      console.log();
    }
  });

  console.log('='.repeat(50));
  
  // 测试文本检测
  const testTexts = [
    '今天完成了 Memory-Master v3.0.0 的开发',
    '上周我们讨论了时间树的实现',
    '这个月要发布新版本',
    '会议定在 2026-04-15 举行',
    '下周一要演示'
  ];

  console.log('\n文本时间表达式检测:\n');
  testTexts.forEach(text => {
    const expressions = timeTree.detectTimeExpressions(text);
    console.log(`文本：${text}`);
    console.log(`检测到的时间表达式：${expressions.map(e => e.expression).join(', ') || '无'}`);
    console.log();
  });
}
