#!/usr/bin/env node

/**
 * Proactive Trigger 主执行脚本
 * 
 * 执行模式：
 * 1. --consume        : 消费并处理pending信号
 * 2. --test [topic]   : 测试指定话题的触发评分
 * 3. --calculate      : 计算当前综合触发评分
 * 4. --update-state   : 更新状态文件
 * 5. 无参数          : 执行完整触发检查流程
 */

import { parseArgs } from 'node:util';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { format, differenceInHours, differenceInMinutes, parseISO } from 'date-fns';

// 配置路径
const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = join(WORKSPACE, '.soul');
const SIGNALS_DIR = join(SOUL_DIR, 'signals');
const TRIGGER_STATE_PATH = join(SOUL_DIR, 'trigger-state.json');
const DAILY_CONTEXT_PATH = join(SOUL_DIR, 'daily_context.json');

// 默认配置
const DEFAULT_CONFIG = {
  maxDailyTriggers: 6,
  minTriggerIntervalHours: 2,
  timeWindows: {
    morning: { start: 7, end: 9, weight: 0.7 },
    workday: { start: 9, end: 18, weight: 1.0 },
    evening: { start: 18, end: 22, weight: 0.5 },
    night: { start: 22, end: 7, weight: 0.0 }
  },
  topicCoolingDays: 7,
  silenceIndexHalfLife: 24, // 小时
  minTriggerScore: 0.6
};

// 确保目录存在
function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// 加载状态
function loadState() {
  if (!existsSync(TRIGGER_STATE_PATH)) {
    return {
      lastTriggerTime: null,
      triggersToday: 0,
      triggeredTopics: {},
      userResponses: {},
      lastSignalProcessed: null,
      config: DEFAULT_CONFIG
    };
  }
  
  try {
    const state = JSON.parse(readFileSync(TRIGGER_STATE_PATH, 'utf-8'));
    // 确保有默认配置
    state.config = { ...DEFAULT_CONFIG, ...(state.config || {}) };
    return state;
  } catch (error) {
    console.error('加载状态文件失败:', error.message);
    return {
      lastTriggerTime: null,
      triggersToday: 0,
      triggeredTopics: {},
      userResponses: {},
      lastSignalProcessed: null,
      config: DEFAULT_CONFIG
    };
  }
}

// 保存状态
function saveState(state) {
  ensureDir(SOUL_DIR);
  writeFileSync(TRIGGER_STATE_PATH, JSON.stringify(state, null, 2));
}

// 获取当前时间窗口
function getCurrentTimeWindow() {
  const now = new Date();
  const hour = now.getHours();
  
  for (const [name, window] of Object.entries(DEFAULT_CONFIG.timeWindows)) {
    if (window.start <= window.end) {
      if (hour >= window.start && hour < window.end) return { name, weight: window.weight };
    } else {
      // 跨夜时段（如22:00-7:00）
      if (hour >= window.start || hour < window.end) return { name, weight: window.weight };
    }
  }
  
  return { name: 'unknown', weight: 0.5 };
}

// 计算沉默指数
function calculateSilenceIndex(state) {
  if (!state.lastTriggerTime) return 1.0;
  
  const lastTime = parseISO(state.lastTriggerTime);
  const now = new Date();
  const hoursSinceLast = differenceInHours(now, lastTime);
  
  // 指数衰减公式：e^(-t/T) 其中T为半衰期
  const halfLife = state.config.silenceIndexHalfLife;
  const index = Math.exp(-hoursSinceLast / halfLife);
  
  // 转换为等待指数：沉默越久，指数越高
  return 1.0 - index;
}

// 计算话题热度
function calculateTopicHeat(topic, state) {
  const now = new Date();
  const topicHistory = state.triggeredTopics[topic] || [];
  
  if (topicHistory.length === 0) return 0.3; // 基础热度
  
  // 最近提及次数
  const recentMentions = topicHistory.filter(time => {
    const mentionTime = parseISO(time);
    return differenceInHours(now, mentionTime) < 24;
  }).length;
  
  // 热度衰减：每次提及增加热度，随时间衰减
  let heat = 0.0;
  for (const mentionTime of topicHistory) {
    const hoursAgo = differenceInHours(now, parseISO(mentionTime));
    const decay = Math.exp(-hoursAgo / 24); // 24小时半衰期
    heat += 0.2 * decay;
  }
  
  // 限制范围
  return Math.min(heat + (recentMentions * 0.1), 1.0);
}

// 读取待处理信号
function getPendingSignals() {
  const pendingFile = join(SIGNALS_DIR, 'pending.jsonl');
  if (!existsSync(pendingFile)) return [];
  
  try {
    const content = readFileSync(pendingFile, 'utf-8');
    const lines = content.split('\n').filter(Boolean);
    return lines.map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    }).filter(signal => signal && signal.type && signal.status === 'pending');
  } catch (error) {
    console.error('读取信号文件失败:', error.message);
    return [];
  }
}

// 处理信号
function processSignal(signal, state) {
  console.log(`处理信号: [${signal.source}] ${signal.type}`);
  
  let shouldTrigger = false;
  let triggerType = null;
  let message = null;
  
  switch (signal.type) {
    case 'breakthrough':
      shouldTrigger = true;
      triggerType = '庆祝';
      message = `看到你完成了“${signal.payload.topic || '某件事'}”，为你点赞！🎉`;
      break;
      
    case 'frustration':
      shouldTrigger = true;
      triggerType = '支持';
      message = `听起来遇到点困难，需要帮忙梳理一下“${signal.payload.topic || '这个问题'}”吗？`;
      break;
      
    case 'decision':
      shouldTrigger = Math.random() > 0.5; // 50%概率触发，避免打扰
      triggerType = '跟进';
      message = `关于你刚才的决策“${signal.payload.topic || '这个选择'}”，有什么后续需要支持的吗？`;
      break;
      
    case 'context_update':
      if (signal.payload.topTopics) {
        shouldTrigger = true;
        triggerType = '话题跟进';
        const topics = signal.payload.topTopics.slice(0, 2).join('、');
        message = `最近你常聊到“${topics}”，想深入聊聊哪个方面？`;
      }
      break;
      
    default:
      // 其他信号类型不触发
      break;
  }
  
  return { shouldTrigger, triggerType, message };
}

// 安全检查
function performSafetyChecks(state, triggerType) {
  const now = new Date();
  const timeWindow = getCurrentTimeWindow();
  
  // 1. 时间窗口检查
  if (timeWindow.weight === 0) {
    console.log('安全检查失败: 当前时段禁止触发');
    return false;
  }
  
  // 2. 每日次数限制
  if (state.triggersToday >= state.config.maxDailyTriggers) {
    console.log(`安全检查失败: 今日已触发${state.triggersToday}次，达到上限`);
    return false;
  }
  
  // 3. 最小间隔检查
  if (state.lastTriggerTime) {
    const lastTime = parseISO(state.lastTriggerTime);
    const hoursSinceLast = differenceInHours(now, lastTime);
    if (hoursSinceLast < state.config.minTriggerIntervalHours) {
      console.log(`安全检查失败: 距上次触发仅${hoursSinceLast.toFixed(1)}小时`);
      return false;
    }
  }
  
  // 4. 时间窗口权重
  if (Math.random() > timeWindow.weight) {
    console.log(`安全检查失败: 时间窗口权重${timeWindow.weight}，随机过滤`);
    return false;
  }
  
  return true;
}

// 计算综合触发评分
function calculateTriggerScore(state, signal = null) {
  const silenceIndex = calculateSilenceIndex(state);
  const timeWindow = getCurrentTimeWindow();
  
  let topicHeat = 0.5;
  let urgency = 0.3;
  let contextRelevance = 0.5;
  
  if (signal) {
    // 基于信号计算
    topicHeat = signal.payload.topic ? calculateTopicHeat(signal.payload.topic, state) : 0.5;
    urgency = signal.priority === 'high' ? 0.8 : signal.priority === 'medium' ? 0.5 : 0.3;
    contextRelevance = 0.7; // 信号通常有上下文
  }
  
  // 综合评分公式
  const score = silenceIndex * topicHeat * urgency * contextRelevance * timeWindow.weight;
  
  console.log(`触发评分计算:`);
  console.log(`  沉默指数: ${silenceIndex.toFixed(2)}`);
  console.log(`  话题热度: ${topicHeat.toFixed(2)}`);
  console.log(`  紧急程度: ${urgency.toFixed(2)}`);
  console.log(`  上下文相关: ${contextRelevance.toFixed(2)}`);
  console.log(`  时间权重: ${timeWindow.weight.toFixed(2)}`);
  console.log(`  综合评分: ${score.toFixed(2)}`);
  
  return score;
}

// 生成触发消息
function generateTriggerMessage(triggerType, baseMessage, state) {
  const now = new Date();
  const timeOfDay = now.getHours() < 12 ? '早上' : now.getHours() < 18 ? '下午' : '晚上';
  
  // 添加个性化前缀
  const prefixes = [
    `[${timeOfDay}好]`,
    `[趁你休息间隙]`,
    `[想起来提醒一下]`,
    `[根据之前聊的]`
  ];
  
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
  
  // 确保是开放式问题
  let message = `${prefix} ${baseMessage}`;
  if (!message.includes('？') && !message.includes('?')) {
    message += ' 你觉得呢？';
  }
  
  return message;
}

// 更新状态（触发后）
function updateStateAfterTrigger(state, topic, userResponse = null) {
  const now = new Date();
  const today = format(now, 'yyyy-MM-dd');
  
  // 更新触发记录
  state.lastTriggerTime = now.toISOString();
  state.triggersToday += 1;
  
  // 记录话题触发
  if (topic) {
    if (!state.triggeredTopics[topic]) {
      state.triggeredTopics[topic] = [];
    }
    state.triggeredTopics[topic].push(now.toISOString());
    
    // 保持最近30条记录
    if (state.triggeredTopics[topic].length > 30) {
      state.triggeredTopics[topic] = state.triggeredTopics[topic].slice(-30);
    }
  }
  
  // 记录用户响应（如果提供）
  if (userResponse) {
    const responseKey = topic || 'general';
    if (!state.userResponses[responseKey]) {
      state.userResponses[responseKey] = [];
    }
    state.userResponses[responseKey].push({
      time: now.toISOString(),
      response: userResponse,
      topic
    });
  }
  
  // 如果是新的一天，重置今日计数
  const lastTriggerDate = state.lastTriggerTime ? format(parseISO(state.lastTriggerTime), 'yyyy-MM-dd') : null;
  if (lastTriggerDate !== today) {
    state.triggersToday = 1; // 当前触发是今天的第一次
  }
  
  return state;
}

// 主处理函数：消费并处理信号
async function consumeAndProcessSignals() {
  console.log('开始消费信号...');
  
  const state = loadState();
  const signals = getPendingSignals();
  
  if (signals.length === 0) {
    console.log('没有待处理信号');
    return { processed: 0, triggered: 0 };
  }
  
  let processedCount = 0;
  let triggeredCount = 0;
  
  for (const signal of signals) {
    // 安全检查
    if (!performSafetyChecks(state, signal.type)) {
      console.log(`跳过信号 ${signal.id}: 安全检查失败`);
      continue;
    }
    
    // 计算触发评分
    const score = calculateTriggerScore(state, signal);
    if (score < state.config.minTriggerScore) {
      console.log(`跳过信号 ${signal.id}: 评分${score.toFixed(2)}低于阈值${state.config.minTriggerScore}`);
      continue;
    }
    
    // 处理信号
    const { shouldTrigger, triggerType, message: baseMessage } = processSignal(signal, state);
    
    if (shouldTrigger && baseMessage) {
      // 生成最终消息
      const finalMessage = generateTriggerMessage(triggerType, baseMessage, state);
      
      console.log(`\n=== 触发消息 ===`);
      console.log(`类型: ${triggerType}`);
      console.log(`信号: ${signal.type} (${signal.source})`);
      console.log(`消息: ${finalMessage}`);
      console.log(`================\n`);
      
      // 更新状态
      const topic = signal.payload.topic || signal.type;
      updateStateAfterTrigger(state, topic);
      triggeredCount++;
      
      // 实际发送消息（这里只是模拟，实际需要调用OpenClaw API）
      // await sendMessage(finalMessage);
    }
    
    // 标记信号为已处理（实际需要调用signal_resolve工具）
    // await resolveSignal(signal.id, shouldTrigger ? 'done' : 'ignored');
    
    processedCount++;
    state.lastSignalProcessed = signal.id;
  }
  
  saveState(state);
  console.log(`处理完成: 处理${processedCount}个信号，触发${triggeredCount}次`);
  
  return { processed: processedCount, triggered: triggeredCount };
}

// 测试函数
function testTriggerCalculation(topic = 'test') {
  console.log(`测试话题触发评分: "${topic}"`);
  
  const state = loadState();
  const score = calculateTriggerScore(state);
  
  console.log(`\n测试结果:`);
  console.log(`当前时间窗口: ${getCurrentTimeWindow().name}`);
  console.log(`沉默指数: ${calculateSilenceIndex(state).toFixed(2)}`);
  console.log(`话题"${topic}"热度: ${calculateTopicHeat(topic, state).toFixed(2)}`);
  console.log(`综合评分: ${score.toFixed(2)}`);
  console.log(`是否达到阈值(${state.config.minTriggerScore}): ${score >= state.config.minTriggerScore ? '是' : '否'}`);
  
  return score;
}

// 主函数
async function main() {
  const args = parseArgs({
    options: {
      consume: { type: 'boolean', short: 'c' },
      test: { type: 'string', short: 't' },
      calculate: { type: 'boolean' },
      'update-state': { type: 'boolean' },
      help: { type: 'boolean', short: 'h' },
      'process-signal': { type: 'string' }
    },
    allowPositionals: true
  });
  
  const { values, positionals } = args;
  
  if (values.help) {
    console.log(`
Proactive Trigger 脚本
用法:
  node trigger.js [选项]

选项:
  -c, --consume          消费并处理pending信号
  -t, --test [topic]     测试指定话题的触发评分
  --calculate            计算当前综合触发评分
  --update-state         更新状态文件
  --process-signal       处理单个信号（JSON格式）
  -h, --help             显示此帮助信息

示例:
  node trigger.js --consume
  node trigger.js --test "健康提醒"
  node trigger.js --calculate
  node trigger.js --process-signal '{"type":"mood_state_assessed",...}'
    `);
    return;
  }
  
  if (values.consume) {
    await consumeAndProcessSignals();
  } else if (values.test) {
    testTriggerCalculation(values.test);
  } else if (values.calculate) {
    const state = loadState();
    const score = calculateTriggerScore(state);
    console.log(`当前综合触发评分: ${score.toFixed(2)}`);
  } else if (values['update-state']) {
    const state = loadState();
    saveState(state);
    console.log('状态文件已更新');
  } else if (values['process-signal']) {
    try {
      const signal = JSON.parse(values['process-signal']);
      console.log(`处理信号: ${signal.type} [${signal.id}]`);
      
      // 处理信号逻辑
      const state = loadState();
      
      // 根据信号类型处理
      if (signal.type === 'mood_state_assessed') {
        console.log(`情绪状态: ${signal.payload.state}, 能量: ${signal.payload.energy}`);
        // 记录情绪状态用于触发决策
        // 这里可以添加更多逻辑
      }
      
      // 检查是否应该触发主动干预
      const triggerScore = calculateTriggerScore(state);
      console.log(`当前触发评分: ${triggerScore.toFixed(2)}`);
      
      if (triggerScore >= state.config.minTriggerScore) {
        console.log('⚠️ 触发评分达到阈值，可能需要主动干预');
      }
      
      // 保存状态
      saveState(state);
    } catch (error) {
      console.error('处理信号失败:', error.message);
    }
    return;
  } else {
    // 默认执行完整检查
    console.log('执行完整触发检查...');
    const state = loadState();
    
    // 1. 检查是否有待处理信号
    const signals = getPendingSignals();
    if (signals.length > 0) {
      console.log(`发现${signals.length}个待处理信号，开始消费...`);
      await consumeAndProcessSignals();
    } else {
      console.log('无待处理信号，跳过触发检查');
    }
    
    // 2. 显示当前状态
    console.log('\n当前状态:');
    console.log(`今日触发次数: ${state.triggersToday}/${state.config.maxDailyTriggers}`);
    console.log(`上次触发时间: ${state.lastTriggerTime || '从未'}`);
    console.log(`已记录话题数: ${Object.keys(state.triggeredTopics).length}`);
  }
}

// 执行主函数
main().catch(error => {
  console.error('脚本执行失败:', error);
  process.exit(1);
});