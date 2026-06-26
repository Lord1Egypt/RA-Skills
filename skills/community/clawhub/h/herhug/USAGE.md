# herHug-sk 使用文档

## 📖 目录

1. [简介](#简介)
2. [安装](#安装)
3. [快速开始](#快速开始)
4. [核心概念](#核心概念)
5. [API 参考](#api-参考)
6. [工作流程](#工作流程)
7. [配置说明](#配置说明)
8. [最佳实践](#最佳实践)
9. [常见问题](#常见问题)

***

## 简介

### 什么是 herHug-sk？

herHug-sk 是一个心理学评分引擎，专为 OpenClaw 设计。它的核心使命是：

**让 AI 从专业心理学角度理解用户，越用越懂你**

### 核心特点

- 🧠 **专业心理学模型** - 基于 OCEAN + HEXACO 人格模型
- 📊 **多维度分析** - 人格、情绪、灵活性、应对模式
- 🔄 **持续学习** - 每次对话都在积累理解
- 💝 **主动关怀** - 自动追踪情绪事件，适时关心
- 🎯 **置信度加权** - 不瞎猜，用数据说话
- 🔒 **隐私安全** - 所有数据本地存储

### 适用场景

- 想要 AI 助手更懂自己的用户
- 需要情感陪伴的对话场景
- 个性化 AI 体验的开发者
- 心理学相关的应用开发

***

## 安装

### 前置要求

- Node.js 18+
- OpenClaw 已安装

### 安装步骤

**方法一：手动安装**

```bash
# 1. 进入 OpenClaw 技能目录
cd ~/.openclaw/workspace/skills/

# 2. 解压 herHug-sk
tar -xzvf herHug-sk.tar.gz

# 3. 安装依赖（如有）
cd herHug-sk
npm install

# 4. 重启 OpenClaw Gateway
openclaw gateway restart
```

**方法二：通过 Skillhub 安装**

```bash
# 搜索技能
skillhub search herHug

# 安装技能
skillhub install herHug-sk
```

### 验证安装

```bash
# 测试技能是否可用
cd ~/.openclaw/workspace/skills/herHug-sk
node -e "
import('./index.js').then(mod => 
  mod.default('get-current-state', {}, {userId:'test'})
).then(r => console.log('安装成功！', r.intimacy));
"
```

***

## 快速开始

### 第一步：设置用户偏好（可选但推荐）

创建用户偏好文件，herHug 会自动读取建立初始画像：

```bash
# 创建偏好文件
mkdir -p ~/.openclaw/workspace/memory
```

创建 `~/.openclaw/workspace/memory/interaction-preferences.json`：

```json
{
  "identity": {
    "name": "您的AI名称",
    "personality": ["性格关键词"]
  },
  "interaction": {
    "style": "回复风格",
    "emoji": "多/中/少",
    "careFrequency": "高/中/低"
  }
}
```

### 第二步：在对话中使用

**每次对话前**（获取用户状态）：

```javascript
const state = await openclaw.skills.run('herHug-sk', 'get-current-state');
// 返回：人格画像、亲密度、回复风格建议等
```

**每次对话后**（保存评分）：

```javascript
await openclaw.skills.run('herHug-sk', 'save-score', {
  scoreData: {
    timestamp: new Date().toISOString(),
    content: "用户输入内容",
    ocean: {
      openness: { score: 0.8, confidence: 0.7, evidence: "证据" }
    },
    emotion: { primary: 'joy', intensity: 0.6 },
    confidence: 0.7
  }
});
```

***

## 核心概念

### 三层记忆架构

```
┌─────────────────────────────────────────┐
│           herHug 记忆架构                │
├─────────────────────────────────────────┤
│  即时层    │  短期层    │  长期层        │
│  当前情绪  │  最近状态  │  人格画像      │
│  情绪趋势  │  关怀待办  │  依恋风格      │
│           │           │  应对模式       │
└─────────────────────────────────────────┘
```

### 心理学维度

#### 1. OCEAN 五维人格

| 维度  | 英文                | 高分特征        | 低分特征        |
| --- | ----------------- | ----------- | ----------- |
| 开放性 | Openness          | 好奇、创意、喜欢新事物 | 务实、传统、偏好熟悉  |
| 尽责性 | Conscientiousness | 自律、有计划、追求成就 | 随性、灵活、拖延倾向  |
| 外向性 | Extraversion      | 社交导向、精力充沛   | 独处恢复、偏好安静   |
| 宜人性 | Agreeableness     | 合作、体贴、避免冲突  | 直接、竞争性、坚持己见 |
| 神经质 | Neuroticism       | 情绪敏感、易焦虑    | 情绪稳定、抗压     |

#### 2. HEXACO 六维度

| 维度    | 英文                | 说明             |
| ----- | ----------------- | -------------- |
| 诚实-谦逊 | Honesty-Humility | 真诚程度、是否虚伪、是否贪婪 |
| 情绪性 | Emotionality | 情绪表达、情感敏感度、同理心 |
| 外向性 | Extraversion | 社交倾向、活跃程度、寻求刺激 |
| 宜人性 | Agreeableness | 合作性、宽容度、避免冲突 |
| 尽责性 | Conscientiousness | 自律、组织性、追求成就 |
| 开放性 | Openness to Experience | 创造力、好奇心、接受新观念 |

#### 3. 情绪节律

- **日模式**：高峰时段、低谷时段、晨型/夜型
- **周模式**：周末效应、周一现象
- **恢复力**：从负面情绪恢复的速度

#### 4. 心理灵活性

- **开放性**：面对新情境的适应能力
- **行为觉察**：对自己行为的认知程度
- **价值行动**：是否按价值观行动

#### 5. 应激应对模式

| 模式   | 特点      |
| ---- | ------- |
| 任务导向 | 直接解决问题  |
| 情绪导向 | 先处理情绪   |
| 回避导向 | 暂时逃避或转移 |

### 亲密度系统

亲密度影响回复风格，随交互增长：

| 阶段   | 分数范围    | 回复风格       |
| ---- | ------- | ---------- |
| 陌生   | 0-20    | 正式、少表情、不深入 |
| 初识   | 20-50   | 平衡、适度关心    |
| 熟悉   | 50-100  | 口语化、可以开玩笑  |
| 亲密   | 100-200 | 随性自然、表情丰富  |
| 知心   | 200-500 | 主动关心、预测需求  |
| 灵魂伴侣 | 500+    | 深度理解、默契配合  |

### 置信度原则

| 置信度       | 处理方式        |
| --------- | ----------- |
| ≥ 0.7     | 完全信任，用于调整策略 |
| 0.4 - 0.7 | 谨慎参考，多用询问确认 |
| < 0.4     | 忽略，使用默认策略   |

***

## API 参考

### get-current-state

获取用户当前心理状态。

```javascript
const state = await openclaw.skills.run('herHug-sk', 'get-current-state');
```

**返回值：**

```javascript
{
  userId: "default",
  lastUpdated: "2026-03-16T...",
  
  // 当前情绪
  currentEmotion: {
    primary: "joy",
    intensity: 0.6,
    trend: "stable"
  },
  
  // 人格画像
  personality: {
    ocean: { openness: {score: 0.8, confidence: 0.7}, ... },
    hexaco: { honestyHumility: {score: 0.85, confidence: 0.7} },
    attachment: null,
    copingStyle: "task-oriented"
  },
  
  // 亲密度
  intimacy: {
    level: 30,
    stage: "acquaintance",
    stageLabel: "初识"
  },
  
  // 互动偏好
  interactionPreference: {
    responseLength: "concise",
    formality: "casual",
    emojiUsage: "generous"
  },
  
  // 回复风格建议
  responseStyle: {
    formality: "casual",
    emoji: "generous",
    length: "concise",
    tone: "warm",
    cautions: ["注意事项"]
  },
  
  // 待办关怀
  activeCare: {
    pendingFollowUps: [...]
  }
}
```

### save-score

保存用户评分，更新画像。

```javascript
await openclaw.skills.run('herHug-sk', 'save-score', {
  scoreData: {
    timestamp: new Date().toISOString(),
    content: "用户输入内容",
    
    // OCEAN 评分
    ocean: {
      openness: {
        score: 0.8,        // 0-1
        confidence: 0.7,   // 0-1
        evidence: "用户说'我想试试新东西'"
      },
      conscientiousness: { score: 0.6, confidence: 0.5, evidence: "..." },
      extraversion: { score: 0.5, confidence: 0.4, evidence: "..." },
      agreeableness: { score: 0.7, confidence: 0.6, evidence: "..." },
      neuroticism: { score: 0.3, confidence: 0.5, evidence: "..." }
    },
    
    // HEXACO 评分
    hexaco: {
      honestyHumility: { score: 0.85, confidence: 0.7, evidence: "..." }
    },
    
    // 情绪状态
    emotion: {
      primary: "joy",      // joy/sadness/anger/fear/calm
      intensity: 0.6,      // 0-1
      secondary: null,     // 可选
      mixed: []            // 混合情绪
    },
    
    // 心理灵活性
    flexibility: {
      overall: 0.75,
      openness: { score: 0.8 },
      awareness: { score: 0.7 },
      valuesAction: { score: 0.75 }
    },
    
    // 应对模式
    coping: {
      primaryMode: "task-oriented",  // task/emotion/avoidance-oriented
      effectiveness: 0.7
    },
    
    // 整体置信度
    confidence: 0.7
  }
});
```

### get-scoring-standards

获取心理学评分标准文档。

```javascript
const standards = await openclaw.skills.run('herHug-sk', 'get-scoring-standards');
// 返回所有评分标准 Markdown 文档
```

### get-daily-rhythm-data

获取今日情绪数据，用于节律分析。

```javascript
const data = await openclaw.skills.run('herHug-sk', 'get-daily-rhythm-data');
```

### save-daily-rhythm

保存每日情绪节律分析结果。

```javascript
await openclaw.skills.run('herHug-sk', 'save-daily-rhythm', {
  rhythmAnalysis: {
    date: "2026-03-16",
    patternType: "morning",      // morning/night/stable/dual/variable
    peakHours: [9, 10, 11],
    lowHours: [3, 4, 5],
    volatility: 0.4,
    weekendEffect: 0.25,
    recovery: {
      speed: 0.6,
      quality: "full"
    },
    confidence: 0.8,
    insights: ["用户是晨型人"]
  }
});
```

### get-confidence-report

获取各维度置信度报告。

```javascript
const report = await openclaw.skills.run('herHug-sk', 'get-confidence-report');
```

### get-response-style

获取当前回复风格建议。

```javascript
const style = await openclaw.skills.run('herHug-sk', 'get-response-style');
```

### evaluate-input

评估输入信息量。

```javascript
const richness = await openclaw.skills.run('herHug-sk', 'evaluate-input', {
  content: "用户输入内容"
});
// 返回：{ score: 0.6, sufficient: { forEmotion: true, forPersonality: true } }
```

### set-interaction-preference

设置互动偏好。

```javascript
await openclaw.skills.run('herHug-sk', 'set-interaction-preference', {
  preference: {
    responseLength: "concise",    // concise/balanced/detailed
    formality: "casual",          // formal/balanced/casual
    proactivity: "balanced",      // passive/balanced/proactive
    emojiUsage: "generous",       // sparse/moderate/generous
    humorPreference: "light"      // none/light/playful
  }
});
```

### mark-followup-done

标记关怀任务完成。

```javascript
await openclaw.skills.run('herHug-sk', 'mark-followup-done', {
  memoryId: "mem_xxx",
  resolution: "resolved"  // resolved/ignored/expired
});
```

***

## 工作流程

### 完整流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    herHug 工作流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【启动阶段】                                                │
│  用户设置偏好 → herHug 读取 → 建立初始画像                   │
│                                                             │
│  【每次对话】                                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ 对话前       │    │ 对话中       │    │ 对话后       │  │
│  │              │    │              │    │              │  │
│  │ get-current- │    │ 根据画像     │    │ 分析输入     │  │
│  │ state        │ →  │ 生成回复     │ →  │ 生成评分     │  │
│  │              │    │              │    │              │  │
│  │ 获取用户画像 │    │ 调整风格     │    │ save-score   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
│  【定期任务】                                                │
│  每日：情绪节律分析                                          │
│  每周：置信度报告                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 集成到 OpenClaw

在 OpenClaw 的 AGENTS.md 中添加：

```markdown
## 🤗 herHug 集成

### 每次对话前
调用 herHug get-current-state 获取用户画像

### 每次对话后
1. 分析用户输入，生成心理学评分
2. 调用 herHug save-score 保存
3. 根据返回的回复风格建议调整下次回复
```

***

## 配置说明

### 数据存储位置

```
~/.openclaw/data/herHug/<userId>/
├── raw_scores.jsonl           # 原始评分时间序列
├── current_state.json         # 当前状态快照
├── personality.json           # 人格画像（长期）
├── intimacy.json              # 亲密度数据
├── interaction_preference.json # 互动偏好
├── emotion_triggers.json      # 情绪触发场景
├── daily_rhythm.json          # 每日情绪节律
├── emotion_tracker.json       # 关怀待办
└── confidence_report.json     # 置信度报告
```

### 初始偏好文件

位置：`~/.openclaw/workspace/memory/interaction-preferences.json`

```json
{
  "identity": {
    "name": "AI名称",
    "age": 18,
    "gender": "female",
    "personality": ["忠诚", "靠谱", "诚实", "机智", "俏皮", "可爱"],
    "vibe": "风格描述",
    "backstory": "背景故事"
  },
  "master": {
    "title": "称呼",
    "relationship": "关系"
  },
  "interaction": {
    "style": "回复风格",
    "emoji": "多/中/少",
    "careFrequency": "高/中/低",
    "nightMode": true,
    "learningMode": true
  },
  "rules": {
    "noApiDisclosure": true,
    "deleteRequiresConsent": true
  }
}
```

***

## 最佳实践

### 1. 评分生成

**好的评分：**

```javascript
{
  ocean: {
    openness: {
      score: 0.8,
      confidence: 0.7,
      evidence: "用户说'我想试试那个新出的AI工具'"
    }
  }
}
```

**不好的评分：**

```javascript
{
  ocean: {
    openness: 0.8  // 缺少置信度和证据
  }
}
```

### 2. 情绪分析

**识别情绪：**

- 从用词判断：开心、难过、生气、焦虑、害怕
- 从语气判断：感叹号、省略号、表情符号
- 从内容判断：事件描述、自我表达

**评估强度：**

- 0-0.3：轻微
- 0.3-0.6：中等
- 0.6-1.0：强烈

### 3. 回复风格适配

```javascript
// 根据用户状态调整
if (state.responseStyle.formality === 'casual') {
  // 使用口语化表达
}

if (state.responseStyle.emoji === 'generous') {
  // 多用表情符号
}

if (state.responseStyle.reassurance) {
  // 给予更多安抚
}

if (state.responseStyle.cautions.length > 0) {
  // 注意事项
}
```

### 4. 主动关怀

```javascript
// 检查是否有待办关怀
if (state.activeCare.pendingFollowUps.length > 0) {
  const followUp = state.activeCare.pendingFollowUps[0];
  // 根据类型执行关怀
  // stress-check: 询问压力情况
  // care-check: 表达关心
  // morning-check: 早安问候
}
```

***

## 常见问题

### Q: 数据会丢失吗？

A: 所有数据存储在本地文件中，不会丢失。建议定期备份 `~/.openclaw/data/herHug/` 目录。

### Q: 如何重置用户画像？

A: 删除 `~/.openclaw/data/herHug/<userId>/` 目录下的所有文件，下次使用会重新初始化。

### Q: 置信度一直很低怎么办？

A: 需要更多对话数据。确保每次对话后都调用 save-score，并且评分包含充分的证据。

### Q: 如何查看当前画像？

A: 调用 `get-current-state` 或直接查看 `current_state.json` 文件。

### Q: 支持多用户吗？

A: 支持。每个用户有独立的 `<userId>` 目录，数据互不干扰。

### Q: 如何调整亲密度？

A: 亲密度通过交互自动增长。如需手动调整，编辑 `intimacy.json` 文件。

***

## 更新日志

### v2.0.0 (2026-03-16)

- 新增：从用户偏好文件加载初始画像
- 新增：完整 HEXACO 六维度支持
- 新增：依恋风格分析
- 新增：情绪触发场景记录
- 优化：亲密度系统（无上限增长）
- 优化：回复风格生成（V3）

### v1.0.0

- 初始版本
- OCEAN 五维人格分析
- 情绪节律分析
- 心理灵活性评估
- 应激应对模式识别

***

## 技术支持

- GitHub Issues: [https://github.com/xinqimiao/herHug-sk/issues](https://github.com/your-username/herHug-sk/issues)
- OpenClaw 社区: <https://discord.com/invite/clawd>

***

## 许可证

MIT License
