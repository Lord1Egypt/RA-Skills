/**
 * Utils - 通用工具函数
 */

/**
 * 格式化任务状态
 */
function formatStatus(status) {
  const statusMap = {
    pending: '⏳ 待分配',
    in_progress: '🔄 进行中',
    completed: '✅ 已完成',
    cancelled: '❌ 已取消'
  };
  return statusMap[status] || `🔵 ${status}`;
}

/**
 * 格式化优先级
 */
function formatPriority(priority) {
  const priorityMap = {
    1: '🔴 高',
    2: '🟡 中',
    3: '🟢 低'
  };
  return priorityMap[priority] || `⚪ ${priority}`;
}

/**
 * 格式化时间
 */
function formatTime(date) {
  if (!date) return '-';
  const d = new Date(date);
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * 计算时间差（分钟）
 */
function timeDiffMinutes(date) {
  if (!date) return null;
  const diff = Date.now() - new Date(date).getTime();
  return Math.floor(diff / 60000);
}

/**
 * 格式化时间差
 */
function formatTimeDiff(date) {
  const minutes = timeDiffMinutes(date);
  if (minutes === null) return '-';
  if (minutes < 1) return '刚刚';
  if (minutes < 60) return `${minutes} 分钟前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} 小时前`;
  const days = Math.floor(hours / 24);
  return `${days} 天前`;
}

/**
 * 创建进度条
 */
function createProgressBar(percentage, width = 50) {
  // 限制百分比在 0-100 范围内
  const clamped = Math.max(0, Math.min(100, percentage));
  const filled = Math.round((clamped / 100) * width);
  const empty = width - filled;
  // 确保 filled 和 empty 都是非负数
  const safeFilled = Math.max(0, Math.min(width, filled));
  const safeEmpty = Math.max(0, width - safeFilled);
  return '█'.repeat(safeFilled) + '░'.repeat(safeEmpty);
}

/**
 * 格式化表格行
 */
function formatTableRow(cells, widths) {
  return cells.map((cell, i) => {
    const str = String(cell || '');
    const width = widths[i] || str.length;
    if (str.length > width) {
      return str.slice(0, width - 3) + '...';
    }
    return str.padEnd(width, ' ');
  }).join(' | ');
}

/**
 * 创建表格
 */
function createTable(headers, rows, colWidths = null) {
  if (!colWidths) {
    // 自动计算列宽
    const allRows = [headers, ...rows];
    const maxCols = Math.max(...allRows.map(r => r.length));
    colWidths = Array(maxCols).fill(0);
    allRows.forEach(row => {
      row.forEach((cell, i) => {
        const width = String(cell || '').length;
        if (width > colWidths[i]) colWidths[i] = width;
      });
    });
    // 添加 padding
    colWidths = colWidths.map(w => Math.min(w + 2, 30));
  }

  const separator = colWidths.map(w => '─'.repeat(w)).join('─┬─');
  
  let result = '';
  result += '|' + formatTableRow(headers, colWidths) + '|\n';
  result += '|' + separator + '|\n';
  rows.forEach(row => {
    result += '|' + formatTableRow(row, colWidths) + '|\n';
  });
  
  return result;
}

/**
 * 分页
 */
function paginate(items, page = 1, pageSize = 10) {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  return {
    items: items.slice(start, end),
    total: items.length,
    page,
    pageSize,
    totalPages: Math.ceil(items.length / pageSize)
  };
}

/**
 * 排序
 */
function sortByKey(items, key, order = 'asc') {
  return [...items].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    if (order === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });
}

/**
 * 过滤
 */
function filterBy(items, field, value) {
  return items.filter(item => item[field] === value);
}

/**
 * 查找
 */
function findFirst(items, predicate) {
  return items.find(predicate);
}

/**
 * 映射
 */
function mapItems(items, mapper) {
  return items.map(mapper);
}

/**
 * 分组
 */
function groupBy(items, key) {
  return items.reduce((acc, item) => {
    const k = item[key];
    if (!acc[k]) acc[k] = [];
    acc[k].push(item);
    return acc;
  }, {});
}

/**
 * 计数
 */
function countBy(items, key) {
  return items.reduce((acc, item) => {
    const k = item[key];
    acc[k] = (acc[k] || 0) + 1;
    return acc;
  }, {});
}

/**
 * 求和
 */
function sumBy(items, key) {
  return items.reduce((sum, item) => sum + (item[key] || 0), 0);
}

/**
 * 平均值
 */
function averageBy(items, key) {
  if (items.length === 0) return 0;
  return sumBy(items, key) / items.length;
}

/**
 * 最大值
 */
function maxBy(items, key) {
  if (items.length === 0) return null;
  return items.reduce((max, item) => {
    return item[key] > max[key] ? item : max;
  });
}

/**
 * 最小值
 */
function minBy(items, key) {
  if (items.length === 0) return null;
  return items.reduce((min, item) => {
    return item[key] < min[key] ? item : min;
  });
}

/**
 * 去重
 */
function uniqueBy(items, key) {
  const seen = new Set();
  return items.filter(item => {
    const k = item[key];
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}

/**
 * 限制数量
 */
function limit(items, n) {
  return items.slice(0, n);
}

/**
 * 延迟
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 重试
 */
async function retry(fn, times = 3, delay = 1000) {
  let lastError;
  for (let i = 0; i < times; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (i < times - 1) {
        await sleep(delay);
      }
    }
  }
  throw lastError;
}

/**
 * 防抖
 */
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * 节流
 */
function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * 生成唯一 ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * 验证邮箱
 */
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

/**
 * 验证 URL
 */
function isValidUrl(url) {
  try {
    const parsed = new URL(url);
    // 只允许 http 和 https 协议
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

/**
 * 截断字符串
 */
function truncate(str, length = 50, suffix = '...') {
  if (str.length <= length) return str;
  return str.slice(0, length - suffix.length) + suffix;
}

/**
 * 转义 HTML
 */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * 深拷贝
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * 合并对象
 */
function mergeObjects(...objects) {
  return Object.assign({}, ...objects);
}

/**
 * 获取对象键
 */
function getKeys(obj) {
  return Object.keys(obj);
}

/**
 * 获取对象值
 */
function getValues(obj) {
  return Object.values(obj);
}

/**
 * 获取对象条目
 */
function getEntries(obj) {
  return Object.entries(obj);
}

/**
 * 检查是否为空
 */
function isEmpty(value) {
  if (value === null || value === undefined) return true;
  if (value === '') return true;
  if (Array.isArray(value) && value.length === 0) return true;
  if (typeof value === 'object' && Object.keys(value).length === 0) return true;
  return false;
}

/**
 * 检查是否为数字
 */
function isNumber(value) {
  return !isNaN(parseFloat(value)) && isFinite(value);
}

/**
 * 检查是否为整数
 */
function isInteger(value) {
  return Number.isInteger(value);
}

/**
 * 检查是否为字符串
 */
function isString(value) {
  return typeof value === 'string';
}

/**
 * 检查是否为数组
 */
function isArray(value) {
  return Array.isArray(value);
}

/**
 * 检查是否为对象
 */
function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/**
 * 检查是否为函数
 */
function isFunction(value) {
  return typeof value === 'function';
}

/**
 * 检查是否为日期
 */
function isDate(value) {
  return value instanceof Date && !isNaN(value.getTime());
}

/**
 * 检查是否为布尔值
 */
function isBoolean(value) {
  return typeof value === 'boolean';
}

/**
 * 检查是否为 null
 */
function isNull(value) {
  return value === null;
}

/**
 * 检查是否为 undefined
 */
function isUndefined(value) {
  return value === undefined;
}

/**
 * 检查是否为空值
 */
function isNil(value) {
  return value === null || value === undefined;
}

/**
 * 检查是否为真值
 */
function isTruthy(value) {
  return !!value;
}

/**
 * 检查是否为假值
 */
function isFalsy(value) {
  return !value;
}

module.exports = {
  // 格式化
  formatStatus,
  formatPriority,
  formatTime,
  formatTimeDiff,
  createProgressBar,
  formatTableRow,
  createTable,
  
  // 数据处理
  paginate,
  sortByKey,
  filterBy,
  findFirst,
  mapItems,
  groupBy,
  countBy,
  sumBy,
  averageBy,
  maxBy,
  minBy,
  uniqueBy,
  limit,
  
  // 异步工具
  sleep,
  retry,
  debounce,
  throttle,
  
  // 工具函数
  generateId,
  isValidEmail,
  isValidUrl,
  truncate,
  escapeHtml,
  deepClone,
  mergeObjects,
  
  // 对象工具
  getKeys,
  getValues,
  getEntries,
  
  // 类型检查
  isEmpty,
  isNumber,
  isInteger,
  isString,
  isArray,
  isObject,
  isFunction,
  isDate,
  isBoolean,
  isNull,
  isUndefined,
  isNil,
  isTruthy,
  isFalsy
};
