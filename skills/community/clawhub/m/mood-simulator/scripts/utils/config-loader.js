/**
 * 配置管理模块
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const CONFIG_PATH = join(WORKSPACE, '.soul', 'mood-config.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 评估参数
  timeFactorWeight: 0.4,
  contentFactorWeight: 0.3,
  historyFactorWeight: 0.3,
  minConfidenceThreshold: 0.6,
  
  // 时间参数
  timeWindows: {
    morning: { start: 6, end: 9, baseEnergy: 0.7 },
    work_morning: { start: 9, end: 12, baseEnergy: 0.8 },
    lunch: { start: 12, end: 14, baseEnergy: 0.5 },
    work_afternoon: { start: 14, end: 18, baseEnergy: 0.7 },
    evening: { start: 18, end: 22, baseEnergy: 0.6 },
    night: { start: 22, end: 6, baseEnergy: 0.3 }
  },
  
  // 内容分析
  contentAnalysisEnabled: true,
  emotionKeywords: {
    positive: ['好', '开心', '完成', '成功', '顺利', '谢谢', '感谢'],
    negative: ['累', '困', '烦', '压力', '问题', '困难', '不懂'],
    urgent: ['急', '马上', '立刻', '尽快', '紧急'],
    tired: ['累', '困', '疲惫', '想睡', '没精神']
  },
  
  // 历史模式
  historyDaysToConsider: 7,
  patternLearningRate: 0.1,
  minPatternSamples: 5,
  
  // 信号参数
  publishStateSignals: true,
  publishPatternSignals: true,
  publishEnergyAlerts: true,
  
  // 调试
  debugMode: false,
  logDetailedAnalysis: false,
  saveRawAssessments: true
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
    mkdirSync(dir, { recursive: true });
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
 * @param {string} key 配置键（支持点表示法，如'timeWindows.morning.baseEnergy'）
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
          baseEnergy: window.baseEnergy,
          start: window.start,
          end: window.end
        };
      }
    } else {
      // 跨夜时段（如22:00-6:00）
      if (hour >= window.start || hour < window.end) {
        return {
          name,
          baseEnergy: window.baseEnergy,
          start: window.start,
          end: window.end
        };
      }
    }
  }
  
  return {
    name: 'unknown',
    baseEnergy: 0.5,
    start: 0,
    end: 24
  };
}

/**
 * 获取情绪关键词
 * @param {string} category 关键词类别
 * @returns {Array} 关键词列表
 */
export function getEmotionKeywords(category = null) {
  const config = loadConfig();
  
  if (category && config.emotionKeywords[category]) {
    return config.emotionKeywords[category];
  }
  
  return config.emotionKeywords;
}

/**
 * 验证配置有效性
 * @returns {Array} 问题列表
 */
export function validateConfig() {
  const config = loadConfig();
  const issues = [];
  
  // 验证权重总和
  const weightSum = config.timeFactorWeight + config.contentFactorWeight + config.historyFactorWeight;
  if (Math.abs(weightSum - 1.0) > 0.01) {
    issues.push(`权重总和应为1.0，当前: ${weightSum.toFixed(2)}`);
  }
  
  // 验证时间窗口
  for (const [name, window] of Object.entries(config.timeWindows)) {
    if (window.baseEnergy < 0 || window.baseEnergy > 1) {
      issues.push(`时间窗口 ${name}.baseEnergy 应在 0-1 之间，当前: ${window.baseEnergy}`);
    }
    
    if (window.start < 0 || window.start >= 24) {
      issues.push(`时间窗口 ${name}.start 应在 0-23 之间，当前: ${window.start}`);
    }
    
    if (window.end < 0 || window.end > 24) {
      issues.push(`时间窗口 ${name}.end 应在 0-24 之间，当前: ${window.end}`);
    }
  }
  
  return issues;
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

/**
 * 获取配置摘要
 */
export function getConfigSummary() {
  const config = loadConfig();
  const issues = validateConfig();
  
  return {
    weights: {
      time: config.timeFactorWeight,
      content: config.contentFactorWeight,
      history: config.historyFactorWeight,
      total: config.timeFactorWeight + config.contentFactorWeight + config.historyFactorWeight
    },
    features: {
      contentAnalysis: config.contentAnalysisEnabled,
      signalPublishing: config.publishStateSignals,
      patternLearning: config.patternLearningRate > 0
    },
    timeWindows: Object.keys(config.timeWindows).length,
    emotionKeywords: Object.entries(config.emotionKeywords).reduce((sum, [cat, words]) => sum + words.length, 0),
    issues: issues.length > 0 ? issues : ['无']
  };
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
  getConfigValue,
  getCurrentTimeWindow,
  getEmotionKeywords,
  validateConfig,
  resetToDefaults,
  showConfig,
  getConfigSummary,
  DEFAULT_CONFIG
};