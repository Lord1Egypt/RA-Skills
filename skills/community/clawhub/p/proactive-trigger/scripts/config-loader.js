/**
 * 配置管理模块
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const CONFIG_PATH = join(WORKSPACE, '.soul', 'trigger-config.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 触发限制
  maxDailyTriggers: 6,
  minTriggerIntervalHours: 2,
  
  // 时间窗口配置
  timeWindows: {
    morning: { start: 7, end: 9, weight: 0.7, allowedTypes: ['daily_summary', 'health_reminder'] },
    workday: { start: 9, end: 18, weight: 1.0, allowedTypes: ['all'] },
    evening: { start: 18, end: 22, weight: 0.5, allowedTypes: ['care', 'follow_up'] },
    night: { start: 22, end: 7, weight: 0.0, allowedTypes: [] }
  },
  
  // 话题管理
  topicCoolingDays: 7,
  minTopicHeat: 0.3,
  
  // 沉默指数
  silenceIndexHalfLife: 24, // 小时
  minSilenceIndex: 0.3,
  
  // 评分阈值
  minTriggerScore: 0.6,
  highPriorityThreshold: 0.8,
  
  // 信号处理
  processSignalsOnStartup: true,
  signalProcessingInterval: 300000, // 5分钟（毫秒）
  
  // 消息生成
  includeEmoji: true,
  maxMessageLength: 200,
  requireOpenEndedQuestion: true,
  
  // 学习参数
  learningEnabled: true,
  responseTrackingDays: 30,
  
  // 调试
  debugMode: false,
  logToFile: true
};

/**
 * 加载配置
 * @returns {object} 配置对象
 */
export function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    saveConfig(DEFAULT_CONFIG);
    return { ...DEFAULT_CONFIG };
  }
  
  try {
    const userConfig = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
    // 深度合并，确保新字段有默认值
    return deepMerge(DEFAULT_CONFIG, userConfig);
  } catch (error) {
    console.error('加载配置失败，使用默认配置:', error.message);
    return { ...DEFAULT_CONFIG };
  }
}

/**
 * 保存配置
 * @param {object} config 配置对象
 */
export function saveConfig(config) {
  const dir = join(WORKSPACE, '.soul');
  if (!existsSync(dir)) {
    require('fs').mkdirSync(dir, { recursive: true });
  }
  
  try {
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
    console.log('配置已保存:', CONFIG_PATH);
  } catch (error) {
    console.error('保存配置失败:', error.message);
  }
}

/**
 * 更新配置字段
 * @param {string} key 配置键（支持点表示法，如'timeWindows.morning.weight'）
 * @param {any} value 新值
 */
export function updateConfig(key, value) {
  const config = loadConfig();
  
  // 使用点表示法设置嵌套属性
  const keys = key.split('.');
  let current = config;
  
  for (let i = 0; i < keys.length - 1; i++) {
    if (!current[keys[i]] || typeof current[keys[i]] !== 'object') {
      current[keys[i]] = {};
    }
    current = current[keys[i]];
  }
  
  current[keys[keys.length - 1]] = value;
  saveConfig(config);
  
  console.log(`配置已更新: ${key} = ${JSON.stringify(value)}`);
}

/**
 * 获取当前时间窗口
 * @returns {object} 时间窗口信息
 */
export function getCurrentTimeWindow() {
  const config = loadConfig();
  const now = new Date();
  const hour = now.getHours();
  
  for (const [name, window] of Object.entries(config.timeWindows)) {
    if (window.start <= window.end) {
      if (hour >= window.start && hour < window.end) {
        return { 
          name, 
          weight: window.weight, 
          allowedTypes: window.allowedTypes,
          start: window.start,
          end: window.end
        };
      }
    } else {
      // 跨夜时段（如22:00-7:00）
      if (hour >= window.start || hour < window.end) {
        return { 
          name, 
          weight: window.weight, 
          allowedTypes: window.allowedTypes,
          start: window.start,
          end: window.end
        };
      }
    }
  }
  
  return { 
    name: 'unknown', 
    weight: 0.5, 
    allowedTypes: [],
    start: 0,
    end: 24
  };
}

/**
 * 检查触发类型是否在当前时间窗口允许
 * @param {string} triggerType 触发类型
 * @returns {boolean} 是否允许
 */
export function isTriggerTypeAllowed(triggerType) {
  const timeWindow = getCurrentTimeWindow();
  
  if (timeWindow.allowedTypes.includes('all')) {
    return true;
  }
  
  // 映射通用类型到具体类型
  const typeMapping = {
    'daily_summary': ['daily_summary', 'morning_briefing'],
    'health_reminder': ['health_reminder', 'break_reminder'],
    'care': ['care', 'evening_checkin'],
    'follow_up': ['follow_up', 'topic_followup'],
    'celebration': ['celebration', 'breakthrough'],
    'support': ['support', 'frustration']
  };
  
  // 检查具体类型
  if (timeWindow.allowedTypes.includes(triggerType)) {
    return true;
  }
  
  // 检查映射的类型
  for (const [category, types] of Object.entries(typeMapping)) {
    if (timeWindow.allowedTypes.includes(category) && types.includes(triggerType)) {
      return true;
    }
  }
  
  return false;
}

/**
 * 获取配置值
 * @param {string} key 配置键
 * @param {any} defaultValue 默认值
 * @returns {any} 配置值
 */
export function getConfigValue(key, defaultValue = undefined) {
  const config = loadConfig();
  const keys = key.split('.');
  let current = config;
  
  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      return defaultValue;
    }
  }
  
  return current !== undefined ? current : defaultValue;
}

/**
 * 重置为默认配置
 */
export function resetToDefaults() {
  saveConfig(DEFAULT_CONFIG);
  console.log('配置已重置为默认值');
}

/**
 * 显示当前配置
 */
export function showConfig() {
  const config = loadConfig();
  console.log('当前配置:');
  console.log(JSON.stringify(config, null, 2));
}

// 深度合并函数
function deepMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
}

export default {
  loadConfig,
  saveConfig,
  updateConfig,
  getCurrentTimeWindow,
  isTriggerTypeAllowed,
  getConfigValue,
  resetToDefaults,
  showConfig,
  DEFAULT_CONFIG
};