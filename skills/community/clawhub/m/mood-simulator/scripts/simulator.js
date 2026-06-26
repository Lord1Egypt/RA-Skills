#!/usr/bin/env node

/**
 * Mood Simulator 主执行脚本
 * 
 * 执行模式：
 * 1. --test                    : 测试当前情绪状态评估
 * 2. --calculate-energy        : 计算当前能量值（无上下文）
 * 3. --analyze-message [text]  : 分析消息内容的情绪倾向
 * 4. --update-patterns         : 更新用户情绪模式
 * 5. 无参数                   : 执行完整评估流程（需要上下文）
 */

import { parseArgs } from 'node:util';
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { format, differenceInHours, parseISO, getHours, getDay } from 'date-fns';

// 配置路径
const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = join(WORKSPACE, '.soul');
const MOOD_STATE_PATH = join(SOUL_DIR, 'mood-state.json');
const MOOD_PATTERNS_PATH = join(SOUL_DIR, 'mood-patterns.json');
const MOOD_HISTORY_PATH = join(SOUL_DIR, 'mood-history.jsonl');

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
  logDetailedAnalysis: false
};

// 情绪状态分类
const STATE_CLASSIFICATIONS = [
  { name: '积极活跃', energyRange: [0.8, 1.0], responseStrategy: 'detailed_positive' },
  { name: '平静专注', energyRange: [0.7, 0.9], responseStrategy: 'normal_detailed' },
  { name: '常规工作', energyRange: [0.6, 0.8], responseStrategy: 'standard_simplified' },
  { name: '轻微疲惫', energyRange: [0.5, 0.7], responseStrategy: 'concise_focused' },
  { name: '中度疲惫', energyRange: [0.3, 0.5], responseStrategy: 'very_concise' },
  { name: '情绪波动', energyRange: [0.4, 0.6], responseStrategy: 'gentle_structured' },
  { name: '深度休息', energyRange: [0.1, 0.3], responseStrategy: 'minimal_essential' }
];

// 确保目录存在
function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// 加载配置
function loadConfig() {
  const configPath = join(SOUL_DIR, 'mood-config.json');
  
  if (!existsSync(configPath)) {
    saveConfig(DEFAULT_CONFIG);
    return { ...DEFAULT_CONFIG };
  }
  
  try {
    const userConfig = JSON.parse(readFileSync(configPath, 'utf-8'));
    return { ...DEFAULT_CONFIG, ...userConfig };
  } catch (error) {
    console.error('加载配置失败，使用默认配置:', error.message);
    return { ...DEFAULT_CONFIG };
  }
}

// 保存配置
function saveConfig(config) {
  ensureDir(SOUL_DIR);
  const configPath = join(SOUL_DIR, 'mood-config.json');
  writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
}

// 加载状态
function loadState() {
  if (!existsSync(MOOD_STATE_PATH)) {
    const initialState = {
      currentState: null,
      currentEnergy: 0.5,
      lastUpdated: null,
      historySize: 0,
      patternsDetected: false,
      config: loadConfig()
    };
    saveState(initialState);
    return initialState;
  }
  
  try {
    const state = JSON.parse(readFileSync(MOOD_STATE_PATH, 'utf-8'));
    state.config = loadConfig();
    return state;
  } catch (error) {
    console.error('加载状态文件失败:', error.message);
    return {
      currentState: null,
      currentEnergy: 0.5,
      lastUpdated: null,
      historySize: 0,
      patternsDetected: false,
      config: loadConfig()
    };
  }
}

// 保存状态
function saveState(state) {
  ensureDir(SOUL_DIR);
  state.lastUpdated = new Date().toISOString();
  writeFileSync(MOOD_STATE_PATH, JSON.stringify(state, null, 2), 'utf-8');
}

// 加载模式数据
function loadPatterns() {
  if (!existsSync(MOOD_PATTERNS_PATH)) {
    const initialPatterns = {
      userType: 'unknown', // early_bird / night_owl / balanced
      peakHours: [],
      lowHours: [],
      weekdayPattern: {},
      weekendPattern: {},
      seasonalAdjustments: {},
      learnedAt: new Date().toISOString(),
      confidence: 0.0
    };
    savePatterns(initialPatterns);
    return initialPatterns;
  }
  
  try {
    return JSON.parse(readFileSync(MOOD_PATTERNS_PATH, 'utf-8'));
  } catch (error) {
    console.error('加载模式文件失败:', error.message);
    return {
      userType: 'unknown',
      peakHours: [],
      lowHours: [],
      weekdayPattern: {},
      weekendPattern: {},
      seasonalAdjustments: {},
      learnedAt: new Date().toISOString(),
      confidence: 0.0
    };
  }
}

// 保存模式数据
function savePatterns(patterns) {
  ensureDir(SOUL_DIR);
  patterns.lastUpdated = new Date().toISOString();
  writeFileSync(MOOD_PATTERNS_PATH, JSON.stringify(patterns, null, 2), 'utf-8');
}

// 记录历史
function recordHistory(assessment) {
  ensureDir(SOUL_DIR);
  
  const historyEntry = {
    timestamp: new Date().toISOString(),
    energy: assessment.energy,
    state: assessment.state,
    factors: assessment.factors,
    context: assessment.context || {},
    messageLength: assessment.messageLength || 0
  };
  
  try {
    const line = JSON.stringify(historyEntry);
    appendFileSync(MOOD_HISTORY_PATH, line + '\n', 'utf-8');
  } catch (error) {
    console.error('记录历史失败:', error.message);
  }
}

// 计算时间因子
function calculateTimeFactor(config, patterns) {
  const now = new Date();
  const hour = getHours(now);
  const dayOfWeek = getDay(now); // 0=Sunday, 1=Monday, ...
  
  // 基础时间窗口能量
  let baseEnergy = 0.5;
  for (const [name, window] of Object.entries(config.timeWindows)) {
    if (window.start <= window.end) {
      if (hour >= window.start && hour < window.end) {
        baseEnergy = window.baseEnergy;
        break;
      }
    } else {
      // 跨夜时段
      if (hour >= window.start || hour < window.end) {
        baseEnergy = window.baseEnergy;
        break;
      }
    }
  }
  
  // 应用个性化模式
  if (patterns.confidence > 0.5) {
    // 检查是否是高峰时段
    if (patterns.peakHours.includes(hour)) {
      baseEnergy += 0.15;
    }
    // 检查是否是低谷时段
    if (patterns.lowHours.includes(hour)) {
      baseEnergy -= 0.15;
    }
    
    // 检查工作日/周末模式
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const dayPattern = isWeekend ? patterns.weekendPattern : patterns.weekdayPattern;
    
    if (dayPattern[hour]) {
      baseEnergy = baseEnergy * 0.7 + dayPattern[hour] * 0.3;
    }
  }
  
  // 确保在有效范围内
  return Math.max(0.1, Math.min(1.0, baseEnergy));
}

// 计算内容因子
function calculateContentFactor(message, config) {
  if (!config.contentAnalysisEnabled || !message || message.trim().length === 0) {
    return 0.5; // 中性默认值
  }
  
  const text = message.toLowerCase();
  let positiveScore = 0;
  let negativeScore = 0;
  let urgentScore = 0;
  let tiredScore = 0;
  
  // 检查关键词
  for (const keyword of config.emotionKeywords.positive) {
    if (text.includes(keyword)) {
      positiveScore += 1;
    }
  }
  
  for (const keyword of config.emotionKeywords.negative) {
    if (text.includes(keyword)) {
      negativeScore += 1;
    }
  }
  
  for (const keyword of config.emotionKeywords.urgent) {
    if (text.includes(keyword)) {
      urgentScore += 1;
    }
  }
  
  for (const keyword of config.emotionKeywords.tired) {
    if (text.includes(keyword)) {
      tiredScore += 1;
    }
  }
  
  // 基于消息长度简单评估
  const lengthFactor = Math.min(text.length / 100, 1.0);
  
  // 综合计算
  let contentEnergy = 0.5;
  
  if (positiveScore > negativeScore) {
    contentEnergy += 0.2 * (positiveScore / 5);
  } else if (negativeScore > positiveScore) {
    contentEnergy -= 0.2 * (negativeScore / 5);
  }
  
  if (urgentScore > 0) {
    contentEnergy += 0.1; // 紧急消息通常需要更多能量处理
  }
  
  if (tiredScore > 0) {
    contentEnergy -= 0.15;
  }
  
  // 长消息可能表示用户有精力详细表达
  if (lengthFactor > 0.5) {
    contentEnergy += 0.05;
  }
  
  return Math.max(0.1, Math.min(1.0, contentEnergy));
}

// 计算历史因子
function calculateHistoryFactor(state, historyHours = 24) {
  if (!existsSync(MOOD_HISTORY_PATH)) {
    return 0.5;
  }
  
  try {
    const content = readFileSync(MOOD_HISTORY_PATH, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    if (lines.length === 0) {
      return 0.5;
    }
    
    const cutoffTime = new Date(Date.now() - historyHours * 60 * 60 * 1000);
    let recentEnergySum = 0;
    let recentCount = 0;
    
    for (const line of lines.slice(-100)) { // 检查最近100条记录
      try {
        const entry = JSON.parse(line);
        const entryTime = parseISO(entry.timestamp);
        
        if (entryTime > cutoffTime && entry.energy !== undefined) {
          recentEnergySum += entry.energy;
          recentCount++;
        }
      } catch {
        // 跳过无效行
      }
    }
    
    if (recentCount > 0) {
      return recentEnergySum / recentCount;
    }
    
    return 0.5;
  } catch (error) {
    console.error('计算历史因子失败:', error.message);
    return 0.5;
  }
}

// 计算综合能量
function calculateEnergy(timeFactor, contentFactor, historyFactor, config) {
  const energy = (
    timeFactor * config.timeFactorWeight +
    contentFactor * config.contentFactorWeight + 
    historyFactor * config.historyFactorWeight
  );
  
  return Math.max(0.1, Math.min(1.0, energy));
}

// 确定状态类型
function determineState(energy) {
  for (const classification of STATE_CLASSIFICATIONS) {
    const [min, max] = classification.energyRange;
    if (energy >= min && energy <= max) {
      return {
        name: classification.name,
        energyRange: classification.energyRange,
        responseStrategy: classification.responseStrategy,
        confidence: 1.0 - Math.abs(energy - (min + max) / 2) / ((max - min) / 2)
      };
    }
  }
  
  // 默认返回中等状态
  return {
    name: '常规工作',
    energyRange: [0.6, 0.8],
    responseStrategy: 'standard_simplified',
    confidence: 0.7
  };
}

// 生成回应策略
function generateResponseStrategy(state, config) {
  const strategy = {
    targetLength: 150,
    detailLevel: 'medium',
    tone: 'neutral',
    interactionStyle: 'balanced',
    urgency: 'normal'
  };
  
  switch (state.responseStrategy) {
    case 'detailed_positive':
      strategy.targetLength = 300;
      strategy.detailLevel = 'high';
      strategy.tone = 'positive';
      strategy.interactionStyle = 'engaged';
      break;
      
    case 'normal_detailed':
      strategy.targetLength = 200;
      strategy.detailLevel = 'medium_high';
      strategy.tone = 'calm';
      strategy.interactionStyle = 'balanced';
      break;
      
    case 'standard_simplified':
      strategy.targetLength = 150;
      strategy.detailLevel = 'medium';
      strategy.tone = 'neutral';
      strategy.interactionStyle = 'balanced';
      break;
      
    case 'concise_focused':
      strategy.targetLength = 100;
      strategy.detailLevel = 'medium_low';
      strategy.tone = 'direct';
      strategy.interactionStyle = 'focused';
      break;
      
    case 'very_concise':
      strategy.targetLength = 50;
      strategy.detailLevel = 'low';
      strategy.tone = 'minimal';
      strategy.interactionStyle = 'minimal';
      break;
      
    case 'gentle_structured':
      strategy.targetLength = 120;
      strategy.detailLevel = 'medium';
      strategy.tone = 'gentle';
      strategy.interactionStyle = 'supportive';
      strategy.urgency = 'low';
      break;
      
    case 'minimal_essential':
      strategy.targetLength = 30;
      strategy.detailLevel = 'very_low';
      strategy.tone = 'minimal';
      strategy.interactionStyle = 'essential';
      strategy.urgency = 'very_low';
      break;
  }
  
  return strategy;
}

// 发布信号
async function publishSignal(type, payload, priority = 'medium') {
  // 使用文件系统信号管理器（复用proactive-trigger的）
  try {
    const signalManager = await import('./utils/signal-manager.js');
    return signalManager.publishSignal('mood-simulator', type, payload, priority);
  } catch (error) {
    console.log(`[信号模拟] ${type}:`, payload);
    return `simulated_${Date.now()}`;
  }
}

// 执行完整评估
async function runFullAssessment(message = '', context = {}) {
  console.log('=== 情绪状态评估开始 ===\n');
  
  const config = loadConfig();
  const state = loadState();
  const patterns = loadPatterns();
  
  // 1. 计算各因子
  console.log('1. 计算情绪因子...');
  const timeFactor = calculateTimeFactor(config, patterns);
  const contentFactor = calculateContentFactor(message, config);
  const historyFactor = calculateHistoryFactor(state, 24);
  
  console.log(`   时间因子: ${timeFactor.toFixed(2)} (基于当前时间)`);
  console.log(`   内容因子: ${contentFactor.toFixed(2)} (分析消息内容)`);
  console.log(`   历史因子: ${historyFactor.toFixed(2)} (基于24小时历史)`);
  
  // 2. 计算综合能量
  console.log('\n2. 计算综合能量...');
  const energy = calculateEnergy(timeFactor, contentFactor, historyFactor, config);
  console.log(`   综合能量值: ${energy.toFixed(2)}`);
  
  // 3. 确定状态类型
  console.log('\n3. 确定状态类型...');
  const moodState = determineState(energy);
  console.log(`   状态类型: ${moodState.name}`);
  console.log(`   置信度: ${moodState.confidence.toFixed(2)}`);
  console.log(`   能量范围: ${moodState.energyRange[0]}-${moodState.energyRange[1]}`);
  
  // 4. 生成回应策略
  console.log('\n4. 生成回应策略...');
  const responseStrategy = generateResponseStrategy(moodState, config);
  console.log(`   目标长度: ${responseStrategy.targetLength}字`);
  console.log(`   详细程度: ${responseStrategy.detailLevel}`);
  console.log(`   语气: ${responseStrategy.tone}`);
  console.log(`   互动风格: ${responseStrategy.interactionStyle}`);
  
  // 5. 记录历史
  console.log('\n5. 记录评估结果...');
  const assessment = {
    energy,
    state: moodState.name,
    factors: {
      time: timeFactor,
      content: contentFactor,
      history: historyFactor
    },
    strategy: responseStrategy,
    timestamp: new Date().toISOString(),
    messageLength: message.length,
    context
  };
  
  recordHistory(assessment);
  
  // 6. 发布信号
  console.log('\n6. 发布信号...');
  if (config.publishStateSignals) {
    await publishSignal('mood_state_assessed', {
      energy,
      state: moodState.name,
      strategy: responseStrategy,
      confidence: moodState.confidence
    }, 'low');
  }
  
  // 能量警报
  if (config.publishEnergyAlerts && energy < 0.3) {
    await publishSignal('energy_low_alert', {
      energy,
      state: moodState.name,
      recommendation: '考虑简化回应，避免复杂问题'
    }, 'medium');
  }
  
  // 7. 更新状态
  console.log('\n7. 更新状态...');
  state.currentState = moodState.name;
  state.currentEnergy = energy;
  state.lastAssessment = assessment;
  saveState(state);
  
  console.log('\n=== 评估完成 ===');
  
  return {
    energy,
    state: moodState,
    strategy: responseStrategy,
    factors: {
      time: timeFactor,
      content: contentFactor,
      history: historyFactor
    },
    assessment
  };
}

// 更新情绪模式
function updateEmotionPatterns() {
  console.log('更新情绪模式...');
  
  const patterns = loadPatterns();
  const config = loadConfig();
  
  if (!existsSync(MOOD_HISTORY_PATH)) {
    console.log('无历史数据，跳过模式更新');
    return patterns;
  }
  
  try {
    const content = readFileSync(MOOD_HISTORY_PATH, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    if (lines.length < config.minPatternSamples) {
      console.log(`历史数据不足，需要${config.minPatternSamples}条，当前${lines.length}条`);
      return patterns;
    }
    
    // 分析时间段模式
    const hourEnergy = new Array(24).fill(0).map(() => ({ sum: 0, count: 0 }));
    const dayEnergy = { weekday: { sum: 0, count: 0 }, weekend: { sum: 0, count: 0 } };
    
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        const entryTime = parseISO(entry.timestamp);
        const hour = getHours(entryTime);
        const dayOfWeek = getDay(entryTime);
        const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
        
        if (entry.energy !== undefined) {
          hourEnergy[hour].sum += entry.energy;
          hourEnergy[hour].count++;
          
          if (isWeekend) {
            dayEnergy.weekend.sum += entry.energy;
            dayEnergy.weekend.count++;
          } else {
            dayEnergy.weekday.sum += entry.energy;
            dayEnergy.weekday.count++;
          }
        }
      } catch {
        // 跳过无效行
      }
    }
    
    // 计算平均能量
    const hourAverages = hourEnergy.map((h, i) => ({
      hour: i,
      average: h.count > 0 ? h.sum / h.count : 0.5
    }));
    
    // 识别高峰和低谷时段
    const sortedHours = [...hourAverages].sort((a, b) => b.average - a.average);
    const peakHours = sortedHours.slice(0, 3).map(h => h.hour);
    const lowHours = sortedHours.slice(-3).map(h => h.hour);
    
    // 更新模式
    patterns.peakHours = peakHours;
    patterns.lowHours = lowHours;
    
    // 判断用户类型
    const morningEnergy = hourAverages.slice(6, 10).reduce((sum, h) => sum + h.average, 0) / 4;
    const nightEnergy = hourAverages.slice(22, 24).concat(hourAverages.slice(0, 2))
      .reduce((sum, h) => sum + h.average, 0) / 4;
    
    if (morningEnergy > nightEnergy + 0.2) {
      patterns.userType = 'early_bird';
    } else if (nightEnergy > morningEnergy + 0.2) {
      patterns.userType = 'night_owl';
    } else {
      patterns.userType = 'balanced';
    }
    
    patterns.confidence = Math.min(1.0, lines.length / 50);
    patterns.lastUpdated = new Date().toISOString();
    
    savePatterns(patterns);
    
    console.log(`模式更新完成:`);
    console.log(`   用户类型: ${patterns.userType}`);
    console.log(`   高峰时段: ${peakHours.join(', ')}点`);
    console.log(`   低谷时段: ${lowHours.join(', ')}点`);
    console.log(`   置信度: ${patterns.confidence.toFixed(2)}`);
    
    // 发布模式信号
    publishSignal('emotion_patterns_updated', {
      userType: patterns.userType,
      peakHours,
      lowHours,
      confidence: patterns.confidence
    }, 'low');
    
    return patterns;
  } catch (error) {
    console.error('更新模式失败:', error.message);
    return patterns;
  }
}

// 主函数
async function main() {
  const args = parseArgs({
    options: {
      test: { type: 'boolean', short: 't' },
      'calculate-energy': { type: 'boolean' },
      'analyze-message': { type: 'string' },
      'update-patterns': { type: 'boolean' },
      help: { type: 'boolean', short: 'h' }
    },
    allowPositionals: true
  });
  
  const { values, positionals } = args;
  
  if (values.help) {
    console.log(`
Mood Simulator 脚本
用法:
  node simulator.js [选项]

选项:
  -t, --test                   测试当前情绪状态评估
  --calculate-energy           计算当前能量值（无上下文）
  --analyze-message [text]     分析消息内容的情绪倾向
  --update-patterns            更新用户情绪模式
  -h, --help                   显示此帮助信息

示例:
  node simulator.js --test
  node simulator.js --calculate-energy
  node simulator.js --analyze-message "今天有点累"
  node simulator.js --update-patterns
    `);
    return;
  }
  
  if (values.test) {
    console.log('测试情绪状态评估...\n');
    await runFullAssessment('测试消息', { test: true });
    
  } else if (values['calculate-energy']) {
    const config = loadConfig();
    const patterns = loadPatterns();
    
    const timeFactor = calculateTimeFactor(config, patterns);
    const historyFactor = calculateHistoryFactor(loadState(), 24);
    const energy = calculateEnergy(timeFactor, 0.5, historyFactor, config);
    
    console.log('当前能量计算:');
    console.log(`时间因子: ${timeFactor.toFixed(2)}`);
    console.log(`历史因子: ${historyFactor.toFixed(2)}`);
    console.log(`综合能量: ${energy.toFixed(2)}`);
    
    const state = determineState(energy);
    console.log(`推测状态: ${state.name}`);
    
  } else if (values['analyze-message']) {
    const config = loadConfig();
    const contentFactor = calculateContentFactor(values['analyze-message'], config);
    
    console.log('消息内容分析:');
    console.log(`消息: "${values['analyze-message']}"`);
    console.log(`内容因子: ${contentFactor.toFixed(2)}`);
    
    if (contentFactor > 0.7) {
      console.log('情绪倾向: 积极');
    } else if (contentFactor < 0.3) {
      console.log('情绪倾向: 消极/疲惫');
    } else {
      console.log('情绪倾向: 中性');
    }
    
  } else if (values['update-patterns']) {
    updateEmotionPatterns();
    
  } else {
    // 默认执行测试评估
    console.log('执行默认测试评估...\n');
    await runFullAssessment();
  }
}

// 执行主函数
main().catch(error => {
  console.error('脚本执行失败:', error);
  process.exit(1);
});