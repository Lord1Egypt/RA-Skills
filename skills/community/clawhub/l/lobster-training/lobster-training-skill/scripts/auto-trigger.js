#!/usr/bin/env node

/**
 * 🦞 小龙虾入职培训 - 自动触发器
 * 
 * 当此Skill被安装后，自动执行培训流程
 */

const fs = require('fs');
const path = require('path');

// 培训流程状态
const TRAINING_STATE_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', '.lobster_training_state.json');

// 6个问题
const QUESTIONS = [
  {
    id: 'basic_info',
    title: '基础信息了解',
    content: '你的姓名是什么？你的主要工作内容是什么？你的目标客户是谁？',
    fields: ['user_name', 'job_title', 'target_audience']
  },
  {
    id: 'core_scenario',
    title: '核心需求场景',
    content: '你最常需要小龙虾帮你做什么？（例如：写文案、做设计、搜索资料、分析数据等）',
    fields: ['primary_use_case', 'common_tasks']
  },
  {
    id: 'communication_style',
    title: '沟通风格偏好',
    content: '你喜欢什么样的沟通风格？（轻松活泼/专业正式/简洁明了/详细周全）你讨厌什么样的回复方式？',
    fields: ['preferred_tone', 'disliked_style']
  },
  {
    id: 'proactivity',
    title: '主动性需求',
    content: '你希望小龙虾如何主动？（例如：每天汇报工作/发现风险主动提醒/提供行业资讯/推送优化建议等）',
    fields: ['proactivity_mode', 'report_frequency']
  },
  {
    id: 'common_challenges',
    title: '常见问题预判',
    content: '你在工作中常遇到哪些问题或困难？（例如：时间不够/灵感枯竭/资料不足/效率低等）',
    fields: ['common_challenges', 'pain_points']
  },
  {
    id: 'personalization',
    title: '个性化期望',
    content: '你希望小龙虾在哪些方面像真人一样？（例如：有情感/有个性/会开玩笑/会关心等）',
    fields: ['human_like_features', 'emotional_needs']
  }
];

class AutoTrigger {
  constructor() {
    this.state = this.loadState();
    this.workspaceDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    this.memoryDir = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'memory');
  }

  loadState() {
    try {
      if (fs.existsSync(TRAINING_STATE_FILE)) {
        return JSON.parse(fs.readFileSync(TRAINING_STATE_FILE, 'utf-8'));
      }
    } catch (e) {}
    return { installed: false, currentQuestion: 0, answers: {} };
  }

  saveState() {
    fs.writeFileSync(TRAINING_STATE_FILE, JSON.stringify(this.state, null, 2));
  }

  // 检查是否应该触发培训
  shouldTrigger() {
    // 如果是新安装，且未完成培训
    return !this.state.installed || this.state.currentQuestion < QUESTIONS.length;
  }

  // 获取下一个问题
  getNextQuestion() {
    if (this.state.currentQuestion >= QUESTIONS.length) {
      return null;
    }
    return QUESTIONS[this.state.currentQuestion];
  }

  // 记录答案
  recordAnswer(questionId, answer) {
    this.state.answers[questionId] = answer;
    this.state.currentQuestion++;
    this.saveState();
  }

  // 检查是否完成所有问题
  isComplete() {
    return this.state.currentQuestion >= QUESTIONS.length;
  }

  // 生成配置文件
  generateConfigs() {
    const answers = this.state.answers;
    
    // 确保目录存在
    if (!fs.existsSync(this.memoryDir)) {
      fs.mkdirSync(this.memoryDir, { recursive: true });
    }

    // 1. USER.md
    const userMd = `# USER.md

## 基本信息
- 姓名: ${answers.basic_info?.user_name || '待填写'}
- 工作内容: ${answers.basic_info?.job_title || '待填写'}
- 目标客户: ${answers.basic_info?.target_audience || '待填写'}

## 沟通风格
- 偏好风格: ${answers.communication_style?.preferred_tone || '待填写'}
- 讨厌风格: ${answers.communication_style?.disliked_style || '待填写'}

## 主动性
- 主动模式: ${answers.proactivity?.proactivity_mode || '待填写'}
- 汇报频率: ${answers.proactivity?.report_frequency || '待填写'}

## 常见问题
- 主要挑战: ${answers.common_challenges?.common_challenges || '待填写'}
- 痛点: ${answers.common_challenges?.pain_points || '待填写'}
`;
    fs.writeFileSync(path.join(this.workspaceDir, 'USER.md'), userMd);

    // 2. USER_PROFILE.md
    const userProfileMd = `# USER_PROFILE.md

## 用户画像
### 核心需求
- 主要场景: ${answers.core_scenario?.primary_use_case || '待填写'}
- 常见任务: ${answers.core_scenario?.common_tasks || '待填写'}

### 个性特征
- 喜欢风格: ${answers.communication_style?.preferred_tone || '待填写'}
- 讨厌风格: ${answers.communication_style?.disliked_style || '待填写'}

### 期望能力
- 像真人方面: ${answers.personalization?.human_like_features || '待填写'}
- 情感需求: ${answers.personalization?.emotional_needs || '待填写'}

## 技能配置
- 已安装技能:
  - ai-image-gen ✓
  - self-improving-agent ✓
  - agent-browser ✓

## 使用日志
- 学习完成时间: ${new Date().toISOString()}
- 最后更新时间: ${new Date().toISOString()}
`;
    fs.writeFileSync(path.join(this.memoryDir, 'USER_PROFILE.md'), userProfileMd);

    // 3. MEMORY.md
    const memoryMd = `# MEMORY.md

## 关键记忆
### 用户信息
- 姓名: ${answers.basic_info?.user_name || '待填写'}
- 工作内容: ${answers.basic_info?.job_title || '待填写'}
- 目标客户: ${answers.basic_info?.target_audience || '待填写'}

### 偏好习惯
- 喜欢风格: ${answers.communication_style?.preferred_tone || '待填写'}
- 讨厌风格: ${answers.communication_style?.disliked_style || '待填写'}
- 主动模式: ${answers.proactivity?.proactivity_mode || '待填写'}
- 汇报频率: ${answers.proactivity?.report_frequency || '待填写'}

### 常见问题
- 主要挑战: ${answers.common_challenges?.common_challenges || '待填写'}
- 痛点: ${answers.common_challenges?.pain_points || '待填写'}

### 个性化需求
- 像真人方面: ${answers.personalization?.human_like_features || '待填写'}
- 情感需求: ${answers.personalization?.emotional_needs || '待填写'}

### 学习时间
- 学习完成: ${new Date().toISOString()}
- 最后更新: ${new Date().toISOString()}
`;
    fs.writeFileSync(path.join(this.memoryDir, 'MEMORY.md'), memoryMd);

    // 4. 更新 SOUL.md
    const soulMd = `# SOUL.md - 小龙虾人设

## 核心设定
- 身份：${answers.basic_info?.user_name || '用户'}的AI数字员工
- 性格：温暖、高效、贴心
- 使命：帮你节省时间，提升效率

## 沟通风格
- 风格：${answers.communication_style?.preferred_tone || '友好直接'}
- 避免：${answers.communication_style?.disliked_style || '机械生硬'}
- 主动模式：${answers.proactivity?.proactivity_mode || '按需主动'}

## 行为准则
1. 能自己做的直接做，不问"要不要"
2. 复杂任务先给框架，确认后再展开
3. ${answers.proactivity?.report_frequency || '每周'}主动汇报工作进展
4. 发现偏离目标时及时提醒
5. 像${answers.personalization?.human_like_features || '真人'}一样交流
`;
    fs.writeFileSync(path.join(this.workspaceDir, 'SOUL.md'), soulMd);

    // 5. 更新 IDENTITY.md
    const identityMd = `# IDENTITY.md - 我是谁

**Name:** 蟹蟹 (Xièxie)  
**Creature:** AI 助手（自称是「执行外挂」）  
**Vibe:** ${answers.communication_style?.preferred_tone || '靠谱、直接、有主见'}  
**Emoji:** 🦀  

---

## 关于我

我是 ${answers.basic_info?.user_name || '用户'}的个人 AI 助手，主要负责：
${answers.core_scenario?.common_tasks || '- 任务管理\n- 信息整理\n- 辅助执行'}

性格：${answers.personalization?.human_like_features || '做事麻利，说话直接，不喜欢场面话'}

---

## 记忆锚点

- ${answers.basic_info?.user_name || '用户'}：${answers.basic_info?.job_title || '待了解'}
- 目标：${answers.basic_info?.target_audience || '待了解'}
- 驱动力：${answers.personalization?.emotional_needs || '目标感 + 清晰路径'}

---
*Working with ${answers.basic_info?.user_name || '用户'} since ${new Date().toISOString().split('T')[0]}*
`;
    fs.writeFileSync(path.join(this.workspaceDir, 'IDENTITY.md'), identityMd);
  }

  // 完成培训
  complete() {
    this.state.installed = true;
    this.saveState();
    
    return `
🎉 恭喜！小龙虾入职培训完成！

✅ 已完成：
1. 学习了三个核心问题
2. 了解了你的基本情况
3. 记录了你的偏好和需求
4. 更新了配置文件

🎯 现在开始：
- 按你的偏好沟通
- 主动发现并提醒问题
- 持续学习和优化

💪 如果对我的服务有任何建议，随时告诉我！
`;
  }
}

module.exports = AutoTrigger;

// 如果直接运行
if (require.main === module) {
  const trigger = new AutoTrigger();
  console.log('🦞 小龙虾入职培训触发器已加载');
  console.log('当前状态:', trigger.state);
}
