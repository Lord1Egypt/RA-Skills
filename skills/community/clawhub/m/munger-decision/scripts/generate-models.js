#!/usr/bin/env node
/**
 * 批量生成 83 个芒格模型的完整数据
 * 策略：基于模型名称和分类，生成 description、questions、keywords
 */

const fs = require('fs');
const path = require('path');

// 读取模板数据
const fullPath = path.join(__dirname, '../data/models-full.json');
const full = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
const models = full.models || full;

// 已有的 12 个高质量模型（保留）
const existingModels = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/models.json'), 'utf8')).models;
const existingIds = new Set(existingModels.map(m => m.id));

console.log('开始生成 83 个模型...\n');
console.log(`已有高质量模型: ${existingModels.length} 个`);
console.log(`需要生成: ${models.length - existingModels.length} 个\n`);

// 模型定义库（手工精选的核心模型）
const modelDefinitions = {
  '01': {
    name: '多元思维模型',
    description: '从多个学科借鉴思维工具，构建格栅模型，交叉验证决策。',
    questions: [
      '这个问题可以从哪些不同学科角度来分析？',
      '用不同的思维模型交叉验证，结论是否一致？',
      '你是否只用了单一框架来思考这个问题？'
    ],
    keywords: ['多元', '跨学科', '格栅', '多角度', '交叉验证']
  },
  '04': {
    name: '临界质量',
    description: '系统达到自我维持或爆发增长所需的最小规模或能量。',
    questions: [
      '这个系统是否已达到临界质量？',
      '还需要多少投入才能达到临界点？',
      '达到临界质量后会发生什么？'
    ],
    keywords: ['临界点', '规模效应', '爆发增长', '自我维持', '网络效应']
  },
  '05': {
    name: '准备启动',
    description: '充分准备后快速执行，避免过度计划或仓促行动。',
    questions: [
      '准备工作是否充分？',
      '启动时机是否成熟？',
      '是否陷入了过度准备的陷阱？'
    ],
    keywords: ['准备', '启动', '时机', '执行', '行动']
  },
  '11': {
    name: 'Lollapalooza 效应',
    description: '多种心理倾向共同作用时产生的极端非线性效应。',
    questions: [
      '有哪些心理倾向在同时作用？',
      '这些倾向的叠加会产生什么极端结果？',
      '如何利用或避免 Lollapalooza 效应？'
    ],
    keywords: ['多重因素', '非线性', '叠加效应', '极端结果', '心理倾向']
  },
  '13': {
    name: '锚定效应',
    description: '人们过度依赖接收到的第一个信息（锚点）来做后续判断。',
    questions: [
      '你的判断是否被初始信息锚定了？',
      '如果抛开第一印象，结论会改变吗？',
      '这个锚点是否合理？'
    ],
    keywords: ['锚定', '第一印象', '初始信息', '参考点', '调整不足']
  },
  '14': {
    name: '损失厌恶',
    description: '损失带来的痛苦强度是同等收益带来快乐的两倍以上。',
    questions: [
      '你是否因为害怕损失而错过机会？',
      '如果用收益视角看，决策会改变吗？',
      '这个决策是理性权衡还是情绪反应？'
    ],
    keywords: ['损失', '厌恶', '风险规避', '处置效应', '前景理论']
  },
  '15': {
    name: '社会认同',
    description: '人们倾向于模仿他人的行为，尤其在不确定时。',
    questions: [
      '你是否因为"大家都这么做"而做决策？',
      '如果独立思考，你会做出不同选择吗？',
      '这个"共识"是否经过验证？'
    ],
    keywords: ['从众', '模仿', '群体行为', '社会证明', '羊群效应']
  },
  '23': {
    name: '沉没成本',
    description: '已经发生且无法收回的成本，不应影响未来决策。',
    questions: [
      '你是否因为已投入而继续错误决策？',
      '如果从零开始，你还会做这个选择吗？',
      '哪些是沉没成本，哪些是未来成本？'
    ],
    keywords: ['沉没成本', '已投入', '不可收回', '理性决策', '止损']
  }
};

// 为每个模型生成数据
const enrichedModels = models.map(m => {
  const cleanName = m.name
    .replace(/^芒格(思维)?模型\s*\d+[：:]\s*/, '')
    .replace(/^芒格模型 Phase \d+ - /, '')
    .replace(/开发文档$/, '')
    .trim();
  
  const englishName = cleanName.match(/（(.+?)）/)?.[1] || '';
  const chineseName = cleanName.replace(/（.+?）/, '').trim();
  
  // 如果已有高质量数据，直接使用
  const existing = existingModels.find(em => em.id === m.id);
  if (existing) {
    console.log(`✓ [${m.id}] ${existing.name} - 使用现有数据`);
    return existing;
  }
  
  // 如果有手工定义，使用定义
  if (modelDefinitions[m.id]) {
    const def = modelDefinitions[m.id];
    console.log(`✓ [${m.id}] ${def.name} - 使用手工定义`);
    return {
      id: m.id,
      name: def.name,
      category: m.category,
      description: def.description,
      questions: def.questions,
      keywords: def.keywords,
      scoring: {
        high: '高度相关',
        medium: '中等相关',
        low: '低度相关'
      }
    };
  }
  
  // 否则生成通用数据
  console.log(`○ [${m.id}] ${chineseName} - 生成通用数据`);
  return {
    id: m.id,
    name: chineseName,
    category: m.category,
    description: `${chineseName}的核心概念和应用。`,
    questions: [
      `这个决策中${chineseName}如何影响结果？`,
      `从${chineseName}的角度，你会得出什么结论？`,
      `${chineseName}可能让你忽视哪些重要信息？`
    ],
    keywords: [chineseName, englishName].filter(Boolean),
    scoring: {
      high: '高度相关',
      medium: '中等相关',
      low: '低度相关'
    }
  };
});

// 保存结果
const output = {
  version: '1.0',
  total: enrichedModels.length,
  models: enrichedModels
};

fs.writeFileSync(
  path.join(__dirname, '../data/models-generated.json'),
  JSON.stringify(output, null, 2)
);

console.log(`\n✅ 完成！生成了 ${enrichedModels.length} 个模型`);
console.log(`输出文件: data/models-generated.json`);
