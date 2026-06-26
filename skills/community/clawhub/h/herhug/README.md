# 🤗 herHug-sk - 心理学评分引擎

## 让AI从专业角度理解用户，越用越懂你

herHug-sk 是一个为 OpenClaw 设计的心理学评分引擎。它不做生成，只做两件事：

1. **提供专业的心理学评分标准**
2. **记录用户的评分数据，构建连续画像**

大模型基于这些标准和数据，生成真正懂你的回复。

<br />

## ✨**详细的操作手册可以查看USAGE.m**d

## ✨ 特性

- 🧠 **OCEAN+HEXACO人格模型** - 稳定的性格骨架
- 📊 **情绪节律分析** - 日模式、周模式、恢复力
- 🌊 **心理灵活性** - 动态适应能力
- ⚡ **应激应对模式** - 压力下的真实反应
- 🎯 **置信度加权** - 每个维度都有可信度评估
- 💝 **主动关怀** - 自动记住需要跟进的情绪事件
- 🔄 **初始画像加载** - 从用户偏好文件建立初始画像

## 🚀 安装

```bash
# 进入 OpenClaw 技能目录
cd ~/.openclaw/workspace/skills/

# 克隆仓库
git clone https://github.com/xinqimiao/herHug-sk.git

cd herHug-sk
npm install
openclaw gateway restart
```

## 📁 文件结构

```
herHug-sk/
├── SKILL.md           # 技能说明文档
├── index.js           # 核心引擎代码
├── package.json       # Node.js 依赖
├── plugin.json        # OpenClaw 插件配置
├── README.md          # 本文件
├── prompts/           # 提示词模板
│   └── scoring-prompt.md
└── standards/         # 心理学评分标准
    ├── 01_ocean_hexaco.md
    ├── 02_emotional_rhythm.md
    ├── 03_psychological_flexibility.md
    ├── 04_stress_coping.md
    └── 05_confidence_scoring.md
```

## 📊 核心功能

### 1. 获取评分标准

```javascript
const standards = await openclaw.skills.run('herHug-sk', 'get-scoring-standards');
```

### 2. 保存用户评分

```javascript
await openclaw.skills.run('herHug-sk', 'save-score', {
  scoreData: {
    timestamp: new Date().toISOString(),
    content: userInput,
    ocean: { 
      openness: { score: 0.8, confidence: 0.7, evidence: "..." },
      conscientiousness: { score: 0.6, confidence: 0.5, evidence: "..." },
      // ...
    },
    emotion: { primary: 'joy', intensity: 0.7 },
    flexibility: { overall: 0.75 },
    coping: { primaryMode: 'task-oriented' },
    confidence: 0.7
  }
});
```

### 3. 获取当前状态

```javascript
const state = await openclaw.skills.run('herHug-sk', 'get-current-state');
// 返回：人格画像、亲密度、互动偏好、回复风格建议等
```

### 4. 每日情绪节律分析

```javascript
const rawData = await openclaw.skills.run('herHug-sk', 'get-daily-rhythm-data');
await openclaw.skills.run('herHug-sk', 'save-daily-rhythm', {
  rhythmAnalysis: analysisResult
});
```

## 🧠 心理学维度

| 维度           | 文件                                | 说明            |
| ------------ | --------------------------------- | ------------- |
| OCEAN+HEXACO | 01\_ocean\_hexaco.md              | 人格骨架          |
| 情绪节律         | 02\_emotional\_rhythm.md          | 时间模式（日/周/恢复力） |
| 心理灵活性        | 03\_psychological\_flexibility.md | 适应能力          |
| 应激应对         | 04\_stress\_coping.md             | 压力反应          |
| 置信度          | 05\_confidence\_scoring.md        | 可信程度          |

## ⚠️ 置信度原则

| 置信度       | 处理方式          |
| --------- | ------------- |
| ≥ 0.7     | 完全信任，用于调整回复风格 |
| 0.4 - 0.7 | 谨慎参考，多用询问确认   |
| < 0.4     | 忽略，用默认策略      |

## 🔄 完整工作流程

```
启动阶段：
  用户设置身份偏好 → herHug 读取偏好文件 → 建立初始用户画像

每次对话前：
  调用 get-current-state → 返回完整用户画像 → AI 根据画像生成回复

每次对话后：
  AI 分析用户输入 → 生成心理学评分 → 调用 save-score → 更新用户画像

定期任务：
  每日：情绪节律分析
  每周：置信度报告生成
```

## 📁 数据存储

所有用户数据保存在 `~/.openclaw/data/herHug/<userId>/` 目录下：

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

## 🎁 初始画像功能

herHug-sk 启动时会自动读取用户的偏好文件建立初始画像：

- `~/.openclaw/workspace/IDENTITY.md` - 身份定义
- `~/.openclaw/workspace/USER.md` - 用户信息
- `~/.openclaw/workspace/memory/interaction-preferences.json` - 互动偏好

从这些文件推断：

- OCEAN 人格特质
- HEXACO 诚实-谦逊维度
- 互动偏好设置
- 初始亲密度

## 📄 License

MIT License
