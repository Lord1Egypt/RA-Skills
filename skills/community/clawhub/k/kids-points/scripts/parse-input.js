/**
 * 输入验证器
 * 
 * 注意：语义理解由 Agent (LLM) 完成，本模块只负责验证数据格式
 */

/**
 * 验证任务列表格式
 * @param {Array} items - 任务列表
 * @returns {Object} - 验证结果
 */
function validateItems(items) {
  if (!Array.isArray(items)) {
    return { valid: false, error: 'items 必须是数组' };
  }
  
  for (const item of items) {
    if (!item || typeof item !== 'object') {
      return { valid: false, error: '每个 item 必须是对象' };
    }
    
    if (!item.task || typeof item.task !== 'string') {
      return { valid: false, error: '每个 item 必须有 task 字段（字符串）' };
    }
    
    if (item.points !== undefined && typeof item.points !== 'number') {
      return { valid: false, error: 'points 必须是数字' };
    }
    
    if (item.count !== undefined && typeof item.count !== 'number') {
      return { valid: false, error: 'count 必须是数字' };
    }
    
    if (item.note !== undefined && typeof item.note !== 'string') {
      return { valid: false, error: 'note 必须是字符串' };
    }
  }
  
  return { valid: true };
}

/**
 * 解析简单输入（备用方案）
 * 当 Agent 无法提取结构化数据时使用
 */
function parseSimpleInput(input) {
  // 这是一个简单的备用方案，优先使用 Agent 的语义理解
  const tasks = [];
  
  // 尝试提取数字和任务关键词
  const numberMatch = input.match(/(\d+)\s*(课 | 篇 | 个 | 次)/);
  if (numberMatch) {
    tasks.push({
      task: '自主申报',
      count: parseInt(numberMatch[1]),
      unit: numberMatch[2],
      points: parseInt(numberMatch[1]), // 简单计分：1 个=1 分
      note: input
    });
  }
  
  return tasks;
}

module.exports = {
  validateItems,
  parseSimpleInput
};
