#!/usr/bin/env node

/**
 * 叙事记忆主脚本
 * 实现三层过滤和六大触发信号检测
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { format, differenceInDays, parseISO, isWithinInterval } from 'date-fns';
import { loadConfig } from './utils/config-loader.js';

// 路径常量
const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = join(WORKSPACE, '.soul');
const NARRATIVE_PATH = join(SOUL_DIR, 'narratives.jsonl');
const ACCUMULATION_PATH = join(SOUL_DIR, 'accumulation-state.json');
const DAILY_CONTEXT_PATH = join(SOUL_DIR, 'daily_context.json');
const USER_VALUES_PATH = join(SOUL_DIR, 'user-values.json');

// 六大触发信号类型
const SIGNAL_TYPES = {
  DECISION: 'decision',
  VALUE_JUDGMENT: 'value_judgment',
  EMOTIONAL_TURN: 'emotional_turn',
  MILESTONE: 'milestone',
  FIRST_EXPERIENCE: 'first_experience',
  REFLECTION: 'reflection'
};

/**
 * 确保目录和文件存在
 */
function ensureFiles() {
  if (!existsSync(SOUL_DIR)) {
    mkdirSync(SOUL_DIR, { recursive: true });
  }
  
  if (!existsSync(ACCUMULATION_PATH)) {
    writeFileSync(ACCUMULATION_PATH, JSON.stringify({
      topic_mentions: {},
      emotional_patterns: {},
      behavior_patterns: {},
      value_tendencies: {},
      updated_at: new Date().toISOString()
    }, null, 2));
  }
}

/**
 * 加载用户价值数据
 */
function loadUserValues() {
  if (!existsSync(USER_VALUES_PATH)) {
    return { core_values: [], work_principles: [], life_priorities: [] };
  }
  
  try {
    return JSON.parse(readFileSync(USER_VALUES_PATH, 'utf-8'));
  } catch (error) {
    console.error('加载用户价值数据失败:', error.message);
    return { core_values: [], work_principles: [], life_priorities: [] };
  }
}

/**
 * 加载积累状态
 */
function loadAccumulationState() {
  if (!existsSync(ACCUMULATION_PATH)) {
    return {
      topic_mentions: {},
      emotional_patterns: {},
      behavior_patterns: {},
      value_tendencies: {}
    };
  }
  
  try {
    const state = JSON.parse(readFileSync(ACCUMULATION_PATH, 'utf-8'));
    return {
      topic_mentions: state.topic_mentions || {},
      emotional_patterns: state.emotional_patterns || {},
      behavior_patterns: state.behavior_patterns || {},
      value_tendencies: state.value_tendencies || {}
    };
  } catch (error) {
    console.error('加载积累状态失败:', error.message);
    return {
      topic_mentions: {},
      emotional_patterns: {},
      behavior_patterns: {},
      value_tendencies: {}
    };
  }
}

/**
 * 保存积累状态
 */
function saveAccumulationState(state) {
  const fullState = {
    ...state,
    updated_at: new Date().toISOString()
  };
  
  writeFileSync(ACCUMULATION_PATH, JSON.stringify(fullState, null, 2));
}

/**
 * Layer 1: 忽略层检测
 * 判断是否应该忽略该内容
 */
function shouldIgnore(text, config) {
  if (!text || typeof text !== 'string') return true;
  
  // 检查简单确认
  if (config.ignoreSimpleConfirmations) {
    const simpleConfirmations = ['好', '收到', '嗯', '明白', '了解', 'ok', 'OK', 'yes', '是的'];
    if (simpleConfirmations.includes(text.trim())) {
      return true;
    }
  }
  
  // 检查短消息
  if (config.ignoreShortMessages && text.length <= config.maxShortMessageLength) {
    return true;
  }
  
  // 检查日常寒暄
  if (config.ignoreSocialGreetings) {
    const greetings = ['你好', '早上好', '晚上好', '吃了吗', '今天天气不错', 'hi', 'hello'];
    if (greetings.some(g => text.includes(g))) {
      return true;
    }
  }
  
  return false;
}

/**
 * Layer 2: 积累层处理
 * 更新积累状态，返回是否触发叙事
 */
function processAccumulation(text, state, config) {
  const now = new Date();
  const today = format(now, 'yyyy-MM-dd');
  let shouldTrigger = false;
  
  // 话题提及积累
  const topics = extractTopics(text);
  for (const topic of topics) {
    if (!state.topic_mentions[topic]) {
      state.topic_mentions[topic] = {
        count: 1,
        first: today,
        last: today,
        contexts: [text.substring(0, 100)]
      };
    } else {
      state.topic_mentions[topic].count++;
      state.topic_mentions[topic].last = today;
      state.topic_mentions[topic].contexts.push(text.substring(0, 100));
      
      // 检查是否达到阈值
      if (state.topic_mentions[topic].count >= config.topicMentionThreshold) {
        console.log(`话题"${topic}"提及${state.topic_mentions[topic].count}次，可能触发叙事`);
        shouldTrigger = true;
      }
    }
  }
  
  // 情感模式积累
  const emotions = extractEmotions(text);
  for (const emotion of emotions) {
    const key = `${emotion.type}_${emotion.intensity}`;
    if (!state.emotional_patterns[key]) {
      state.emotional_patterns[key] = {
        count: 1,
        first: today,
        last: today,
        contexts: [text.substring(0, 100)]
      };
    } else {
      state.emotional_patterns[key].count++;
      state.emotional_patterns[key].last = today;
      state.emotional_patterns[key].contexts.push(text.substring(0, 100));
      
      if (state.emotional_patterns[key].count >= config.emotionalPatternThreshold) {
        console.log(`情感模式"${key}"出现${state.emotional_patterns[key].count}次，可能触发叙事`);
        shouldTrigger = true;
      }
    }
  }
  
  // 价值倾向积累
  const userValues = loadUserValues();
  for (const value of [...userValues.core_values, ...userValues.work_principles]) {
    if (text.includes(value.name) || text.includes(value.value)) {
      if (!state.value_tendencies[value.name]) {
        state.value_tendencies[value.name] = {
          count: 1,
          first: today,
          last: today,
          contexts: [text.substring(0, 100)]
        };
      } else {
        state.value_tendencies[value.name].count++;
        state.value_tendencies[value.name].last = today;
        state.value_tendencies[value.name].contexts.push(text.substring(0, 100));
        
        if (state.value_tendencies[value.name].count >= config.valueTendencyThreshold) {
          console.log(`价值倾向"${value.name}"提及${state.value_tendencies[value.name].count}次，可能触发叙事`);
          shouldTrigger = true;
        }
      }
    }
  }
  
  return { state, shouldTrigger };
}

/**
 * 提取话题（简化实现）
 */
function extractTopics(text) {
  // 简化实现：提取名词短语
  const commonTopics = [
    'AI', '创业', '产品', '技术', '家庭', '健康', '财务', '学习', '工作',
    '项目', '团队', '时间管理', '决策', '价值观', '目标', '计划'
  ];
  
  return commonTopics.filter(topic => text.includes(topic));
}

/**
 * 提取情感（简化实现）
 */
function extractEmotions(text) {
  const emotions = [];
  
  const emotionKeywords = {
    positive: ['开心', '高兴', '满意', '兴奋', '期待', '感激', '喜欢'],
    negative: ['担心', '焦虑', '压力', '疲惫', '失望', '生气', '困惑'],
    neutral: ['思考', '考虑', '计划', '决定', '反思', '总结']
  };
  
  for (const [type, keywords] of Object.entries(emotionKeywords)) {
    for (const keyword of keywords) {
      if (text.includes(keyword)) {
        emotions.push({
          type,
          keyword,
          intensity: 0.7 // 简化强度
        });
      }
    }
  }
  
  return emotions;
}

/**
 * Layer 3: 触发信号检测
 * 检测六大触发信号
 */
function detectSignals(text, config) {
  const signals = [];
  const textLower = text.toLowerCase();
  
  // 1. 关键决策检测
  const decisionKeywords = ['我决定', '选择了', '放弃了', '确定了', '最终选择', '决定要'];
  if (decisionKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.DECISION,
      confidence: 0.8,
      keywords: decisionKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  // 2. 价值判断检测
  const valueKeywords = ['我认为', '更重要', '不符合我的原则', '价值观上', '对我而言', '意义在于'];
  if (valueKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.VALUE_JUDGMENT,
      confidence: 0.7,
      keywords: valueKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  // 3. 情感转折检测
  const emotionalKeywords = ['从...到', '感觉...现在', '曾经...如今', '转变', '改变想法'];
  if (emotionalKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.EMOTIONAL_TURN,
      confidence: 0.6,
      keywords: emotionalKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  // 4. 里程碑检测
  const milestoneKeywords = ['终于完成了', '达到了', '突破性进展', '里程碑', '第一次成功'];
  if (milestoneKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.MILESTONE,
      confidence: 0.9,
      keywords: milestoneKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  // 5. 第一次体验检测
  const firstKeywords = ['第一次尝试', '从未', '全新体验', '初次', '头一回'];
  if (firstKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.FIRST_EXPERIENCE,
      confidence: 0.7,
      keywords: firstKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  // 6. 反思与后悔检测
  const reflectionKeywords = ['不应该', '如果重来', '从中学到', '后悔当时', '教训是'];
  if (reflectionKeywords.some(kw => textLower.includes(kw))) {
    signals.push({
      type: SIGNAL_TYPES.REFLECTION,
      confidence: 0.75,
      keywords: reflectionKeywords.filter(kw => textLower.includes(kw))
    });
  }
  
  return signals;
}

/**
 * 计算重要性评分
 */
function calculateImportanceScore(signal, text, config) {
  let score = 0;
  
  // 情感强度（简化实现）
  const emotions = extractEmotions(text);
  const emotionalIntensity = emotions.length > 0 ? 0.8 : 0.3;
  score += emotionalIntensity * config.emotionalIntensityWeight;
  
  // 决策影响（基于信号类型）
  const decisionImpact = signal.type === SIGNAL_TYPES.DECISION ? 0.9 : 0.5;
  score += decisionImpact * config.decisionImpactWeight;
  
  // 价值体现（检查是否涉及核心价值）
  const userValues = loadUserValues();
  const allValues = [...userValues.core_values, ...userValues.work_principles, ...userValues.life_priorities];
  const valueAlignment = allValues.some(v => text.includes(v.name)) ? 0.8 : 0.3;
  score += valueAlignment * config.valueAlignmentWeight;
  
  // 模式代表性（检查是否重复出现）
  const accumulationState = loadAccumulationState();
  const topics = extractTopics(text);
  const patternRepresentation = topics.some(t => accumulationState.topic_mentions[t]?.count > 1) ? 0.7 : 0.3;
  score += patternRepresentation * config.patternRepresentationWeight;
  
  // 独特性（简化实现）
  const uniqueness = signal.type === SIGNAL_TYPES.FIRST_EXPERIENCE ? 0.9 : 0.5;
  score += uniqueness * config.uniquenessWeight;
  
  return Math.min(Math.max(score, 0), 1);
}

/**
 * 创建叙事记录
 */
function createNarrative(signal, text, importanceScore, config) {
  const now = new Date();
  const narrativeId = `narrative_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  const narrative = {
    id: narrativeId,
    timestamp: now.toISOString(),
    type: signal.type,
    title: generateTitle(signal, text),
    
    scene: {
      time_context: format(now, 'yyyy-MM-dd HH:mm'),
      emotional_context: extractEmotions(text).map(e => e.type).join(', ') || 'neutral'
    },
    
    content: {
      core_statement: extractCoreStatement(text),
      detailed_description: text.substring(0, 500),
      source_text: text
    },
    
    analysis: {
      importance_score: importanceScore,
      confidence: signal.confidence,
      detected_keywords: signal.keywords,
      signal_strength: signal.confidence
    },
    
    metadata: {
      version: "1.0",
      created_by: "narrative-memory",
      last_accessed: now.toISOString(),
      access_count: 0,
      reinforcement_score: 0.5
    }
  };
  
  return narrative;
}

/**
 * 生成标题
 */
function generateTitle(signal, text) {
  const prefix = {
    [SIGNAL_TYPES.DECISION]: '决策',
    [SIGNAL_TYPES.VALUE_JUDGMENT]: '价值判断',
    [SIGNAL_TYPES.EMOTIONAL_TURN]: '情感转折',
    [SIGNAL_TYPES.MILESTONE]: '里程碑',
    [SIGNAL_TYPES.FIRST_EXPERIENCE]: '首次体验',
    [SIGNAL_TYPES.REFLECTION]: '反思'
  }[signal.type] || '事件';
  
  const snippet = text.substring(0, 30).replace(/\n/g, ' ').trim();
  return `${prefix}: ${snippet}...`;
}

/**
 * 提取核心陈述
 */
function extractCoreStatement(text) {
  // 简化实现：提取第一句话或关键短语
  const sentences = text.split(/[.!?。！？]/);
  return sentences[0] || text.substring(0, 50);
}

/**
 * 保存叙事记录
 */
function saveNarrative(narrative) {
  ensureFiles();
  
  const line = JSON.stringify(narrative) + '\n';
  appendFileSync(NARRATIVE_PATH, line, 'utf-8');
  
  console.log(`叙事记录已保存: ${narrative.id}`);
  console.log(`标题: ${narrative.title}`);
  console.log(`重要性: ${narrative.analysis.importance_score.toFixed(2)}`);
}

/**
 * 处理文本
 */
export function processText(text, config) {
  console.log('处理文本:', text.substring(0, 100) + '...');
  
  // Layer 1: 检查是否忽略
  if (shouldIgnore(text, config)) {
    console.log('Layer 1: 忽略此内容');
    return { ignored: true };
  }
  
  // Layer 2: 积累层处理
  const accumulationState = loadAccumulationState();
  const { state: updatedState, shouldTrigger } = processAccumulation(text, accumulationState, config);
  saveAccumulationState(updatedState);
  
  // Layer 3: 触发信号检测
  const signals = detectSignals(text, config);
  
  if (signals.length === 0 && !shouldTrigger) {
    console.log('Layer 2/3: 未检测到触发信号，仅积累');
    return { ignored: false, signals: [], accumulated: true };
  }
  
  // 处理检测到的信号
  const narratives = [];
  for (const signal of signals) {
    const importanceScore = calculateImportanceScore(signal, text, config);
    
    // 检查是否超过阈值
    const threshold = config[`${signal.type}Threshold`] || 0.5;
    if (importanceScore >= threshold) {
      const narrative = createNarrative(signal, text, importanceScore, config);
      saveNarrative(narrative);
      narratives.push(narrative);
    }
  }
  
  // 处理积累触发
  if (shouldTrigger && narratives.length === 0) {
    // 创建基于积累的叙事
    const topics = extractTopics(text);
    const narrative = {
      id: `pattern_${Date.now()}`,
      timestamp: new Date().toISOString(),
      type: 'pattern',
      title: `模式识别: ${topics.join(', ')}`,
      content: {
        core_statement: `检测到重复出现的模式: ${Object.keys(updatedState.topic_mentions).filter(t => updatedState.topic_mentions[t].count >= config.topicMentionThreshold).join(', ')}`,
        detailed_description: text.substring(0, 500)
      },
      analysis: {
        importance_score: 0.6,
        confidence: 0.7,
        pattern_type: 'topic_repetition'
      }
    };
    
    saveNarrative(narrative);
    narratives.push(narrative);
  }
  
  return {
    ignored: false,
    signals: signals.map(s => s.type),
    narratives: narratives.map(n => ({ id: n.id, title: n.title, importance: n.analysis.importance_score }))
  };
}

/**
 * 分析每日上下文
 */
function analyzeDailyContext() {
  if (!existsSync(DAILY_CONTEXT_PATH)) {
    console.log('每日上下文文件不存在');
    return;
  }
  
  try {
    const dailyContext = JSON.parse(readFileSync(DAILY_CONTEXT_PATH, 'utf-8'));
    console.log('=== 每日上下文分析 ===');
    console.log(`日期: ${dailyContext.date}`);
    console.log(`总结: ${dailyContext.summary}`);
    console.log(`用户情绪: ${dailyContext.user_mood}`);
    
    if (dailyContext.key_events && dailyContext.key_events.length > 0) {
      console.log('\n关键事件:');
      dailyContext.key_events.forEach((event, i) => {
        console.log(`  ${i + 1}. ${event}`);
      });
    }
    
    if (dailyContext.proactive_observations && dailyContext.proactive_observations.length > 0) {
      console.log('\n主动观察:');
      dailyContext.proactive_observations.forEach((obs, i) => {
        console.log(`  ${i + 1}. ${obs}`);
      });
    }
  } catch (error) {
    console.error('分析每日上下文失败:', error.message);
  }
}

/**
 * 显示时间线
 */
function showTimeline(limit = 10) {
  if (!existsSync(NARRATIVE_PATH)) {
    console.log('暂无叙事记录');
    return [];
  }
  
  try {
    const lines = readFileSync(NARRATIVE_PATH, 'utf-8').trim().split('\n');
    const narratives = lines.map(line => JSON.parse(line));
    
    // 按时间倒序排序
    narratives.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    console.log('=== 叙事时间线 ===');
    narratives.slice(0, limit).forEach((narrative, i) => {
      console.log(`\n${i + 1}. ${narrative.title}`);
      console.log(`   时间: ${narrative.timestamp}`);
      console.log(`   类型: ${narrative.type}`);
      console.log(`   重要性: ${narrative.analysis.importance_score.toFixed(2)}`);
      if (narrative.content.core_statement) {
        console.log(`   核心: ${narrative.content.core_statement}`);
      }
    });
    
    return narratives.slice(0, limit);
  } catch (error) {
    console.error('显示时间线失败:', error.message);
    return [];
  }
}

/**
 * 模式分析
 */
function analyzePatterns() {
  const state = loadAccumulationState();
  
  console.log('=== 模式分析 ===');
  
  console.log('\n话题提及统计:');
  Object.entries(state.topic_mentions)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 10)
    .forEach(([topic, data]) => {
      console.log(`  ${topic}: ${data.count}次 (${data.first} ~ ${data.last})`);
    });
  
  console.log('\n情感模式统计:');
  Object.entries(state.emotional_patterns)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 5)
    .forEach(([pattern, data]) => {
      console.log(`  ${pattern}: ${data.count}次`);
    });
  
  console.log('\n价值倾向统计:');
  Object.entries(state.value_tendencies)
    .sort((a, b) => b[1].count - a[1].count)
    .forEach(([value, data]) => {
      console.log(`  ${value}: ${data.count}次`);
    });
}

/**
 * 主函数
 */
async function main() {
  const config = loadConfig();
  ensureFiles();
  
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case '--process-text':
      if (args[1]) {
        const result = processText(args[1], config);
        console.log('处理结果:', JSON.stringify(result, null, 2));
      } else {
        console.error('请提供要处理的文本');
      }
      break;
      
    case '--analyze-daily':
      analyzeDailyContext();
      break;
      
    case '--timeline':
      const limit = args[1] ? parseInt(args[1]) : 10;
      showTimeline(limit);
      break;
      
    case '--patterns':
      analyzePatterns();
      break;
      
    case '--test':
      console.log('运行测试...');
      // 测试忽略层
      const testTexts = [
        '好',
        '今天天气不错',
        '我决定放弃这个项目',
        '我认为家庭比工作更重要',
        '从焦虑到平静，我经历了很多'
      ];
      
      for (const text of testTexts) {
        console.log(`\n测试文本: "${text}"`);
        const result = processText(text, config);
        console.log('结果:', result.ignored ? '忽略' : '处理');
        if (result.signals && result.signals.length > 0) {
          console.log('检测到信号:', result.signals);
        }
      }
      break;
      
    case '--process-signal':
      if (args[1]) {
        try {
      // 修复：支持JSON字符串和普通字符串
      let signal;
      try {
        signal = JSON.parse(args[1]);
      } catch (e) {
        // 如果不是JSON，当作普通字符串处理
        signal = {
          type: args[1],
          payload: { text: `接收到信号: ${args[1]}` },
          timestamp: new Date().toISOString()
        };
        console.log(`将字符串信号"${args[1]}"转换为标准格式`);
      }
          console.log(`处理信号: ${signal.type} [${signal.id}]`);
          
          // 根据信号类型处理
          if (signal.payload && signal.payload.text) {
            const result = processText(signal.payload.text, config);
            console.log('信号处理结果:', JSON.stringify(result, null, 2));
            
            // 发布叙事记录信号
            if (result.narratives && result.narratives.length > 0) {
              console.log(`创建了${result.narratives.length}个叙事记录`);
              // 这里可以调用publishSignal来发布milestone_recorded等信号
            }
          } else {
            console.log('信号无文本内容，跳过');
          }
        } catch (error) {
          console.error('解析信号失败:', error.message);
        }
      } else {
        console.error('请提供信号JSON');
      }
      break;
      
    default:
      console.log('叙事记忆系统 v0.3.0');
      console.log('用法:');
      console.log('  --process-text <text>   处理文本并检测触发信号');
      console.log('  --analyze-daily         分析每日上下文');
      console.log('  --timeline [limit]      显示叙事时间线');
      console.log('  --patterns              分析模式统计');
      console.log('  --test                  运行测试');
      console.log('  --process-signal <json> 处理信号');
      break;
  }
}

// 运行主函数
main().catch(error => {
  console.error('脚本执行失败:', error);
  process.exit(1);
});