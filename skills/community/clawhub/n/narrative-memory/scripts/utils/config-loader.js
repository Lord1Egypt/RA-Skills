/**
 * 配置管理模块
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const CONFIG_PATH = join(WORKSPACE, '.soul', 'narrative-config.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 触发阈值
  decisionThreshold: 0.7,
  valueJudgmentThreshold: 0.6,
  emotionalTurnThreshold: 0.65,
  milestoneThreshold: 0.75,
  firstExperienceThreshold: 0.5,
  reflectionThreshold: 0.6,
  
  // 积累层参数
  topicMentionThreshold: 3,
  emotionalPatternThreshold: 3,
  behaviorPatternThreshold: 3,
  valueTendencyThreshold: 2,
  
  // 重要性评分权重
  emotionalIntensityWeight: 0.3,
  decisionImpactWeight: 0.25,
  valueAlignmentWeight: 0.2,
  patternRepresentationWeight: 0.15,
  uniquenessWeight: 0.1,
  
  // 存储策略
  lowImportanceDecayDays: 7,
  mediumLowDecayDays: 30,
  mediumDecayDays: 90,
  mediumHighDecayDays: 180,
  highImportancePermanent: true,
  
  // 忽略层规则
  ignoreShortMessages: true,
  maxShortMessageLength: 3,
  ignoreSimpleConfirmations: true,
  ignoreSocialGreetings: true,
  ignoreFactQueries: true,
  ignoreSystemStatus: true,
  
  // 信号参数
  publishMilestoneSignals: true,
  publishPatternSignals: true,
  publishLifeThemeSignals: true,
  
  // 调试
  debugMode: false,
  logDetailedAnalysis: false,
  saveRawAssessments: true
};

/**
 * 深度合并对象
 * @param {object} target 目标对象
 * @param {object} source 源对象
 * @returns {object} 合并后的对象
 */
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
 * @param {string} key 配置键（支持点表示法，如'triggerThresholds.decision'）
 * @param {any} value 新值
 */
export function updateConfig(key, value) {
  const config = loadConfig();
  
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
  
  console.log(`配置更新: ${key} = ${JSON.stringify(value)}`);
  return config;
}

/**
 * 重置配置为默认值
 */
export function resetToDefaults() {
  saveConfig(DEFAULT_CONFIG);
  console.log('配置已重置为默认值');
  return { ...DEFAULT_CONFIG };
}

/**
 * 显示当前配置
 */
export function showConfig() {
  const config = loadConfig();
  console.log('当前配置:');
  console.log(JSON.stringify(config, null, 2));
  return config;
}

// CLI支持
if (import.meta.url === `file://${process.argv[1]}`) {
  const command = process.argv[2];
  const key = process.argv[3];
  const value = process.argv[4];
  
  switch (command) {
    case 'show':
      showConfig();
      break;
    case 'reset':
      resetToDefaults();
      break;
    case 'update':
      if (key && value !== undefined) {
        const parsedValue = value === 'true' ? true : value === 'false' ? false : !isNaN(value) ? Number(value) : value;
        updateConfig(key, parsedValue);
      } else {
        console.error('用法: node config-loader.js update <key> <value>');
      }
      break;
    default:
      console.log('可用命令: show, reset, update <key> <value>');
  }
}