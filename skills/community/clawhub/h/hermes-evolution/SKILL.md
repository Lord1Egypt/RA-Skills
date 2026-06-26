# Hermes Evolution - 爱马仕自动进化版

> **版本**: v1.0.0  
> **作者**: 森森  
> **适用**: OpenClaw 所有版本  
> **定位**: PM Router 智能增强层

---

## 🎯 简介

Hermes Evolution（爱马仕自动进化版）是森森在 OpenClaw 基础上构建的**智能增强层**，实现了主动服务、自动进化和用户理解三大核心能力。

### 核心特性

- **⚡ 高性能**: FTS 检索 0.03ms/次，任务查询 O(1)
- **🎯 主动智能**: Periodic Nudge 主动自检，不等指令
- **🔮 自动进化**: AutoSkillGenerator 自动创建 Skill
- **👤 用户理解**: Honcho 用户画像 + 需求预测
- **💾 稳定记忆**: Frozen Memory 分层管理
- **📊 完整闭环**: Self-Improving v2 规则权重学习

---

## 📦 包含模块

### 核心路由
| 模块 | 文件 | 功能 |
|------|------|------|
| PM Router | `sensen-pm-router.js` | 路由核心 + Agent Profile |
| Intent Router | `intent-router.js` | TF-IDF 置信度计算 |
| Agent Profiles | `agent-profiles.js` | Agent 角色定义 |

### 任务管理
| 模块 | 文件 | 功能 |
|------|------|------|
| Task Manager | `task-manager.js` | 任务状态机 |
| Task Store | `task-store.js` | 内存缓存 + 索引加速 |
| Task DAG | `task-dag.js` | DAG 依赖管理 |

### 学习进化
| 模块 | 文件 | 功能 |
|------|------|------|
| Self-Improving v2 | `sensen-self-improving-v2.js` | 规则权重 + 版本管理 |
| Frozen Memory | `frozen-memory.js` | 冻结记忆，下次生效 |
| Patch Store | `patch-store.js` | 增量更新 |

### 智能增强
| 模块 | 文件 | 功能 |
|------|------|------|
| FTS Indexer | `fts-indexer.js` | 全文检索，0.03ms/次 |
| Progressive Disclosure | `progressive-disclosure.js` | 渐进式加载，Token 控制 |
| Periodic Nudge | `periodic-nudge.js` | 主动自检引擎 |

### 用户理解
| 模块 | 文件 | 功能 |
|------|------|------|
| Honcho Profiler | `honcho-profiler.js` | 用户画像 + 需求预测 |
| AutoSkill Generator | `auto-skill-generator.js` | 自动创建 Skill |
| LLM Summarizer | `llm-summarizer.js` | 检索结果摘要 |

### 系统工具
| 模块 | 文件 | 功能 |
|------|------|------|
| Logger | `sensen-logger.js` | 结构化日志 |
| Collaborator | `sensen-collaborator.js` | 多 Agent 协作 |
| Collab Visualizer | `sensen-collab-visualizer.js` | 协作可视化 |
| Template Engine | `template-engine.js` | 模板渲染 |
| Scheduler | `sensen-scheduler.js` | 定时任务 |
| Feishu Notifier | `sensen-feishu-notifier.js` | 飞书通知 |
| Spawner | `sensen-spawner.js` | Agent Spawn |

---

## 🚀 快速开始

### 1. 安装

```bash
# 方式一：从 ClawhHub 安装
clawdhub install hermes-evolution

# 方式二：手动复制
# 将 modules/ 目录复制到 skills/sensen-pm-router/
```

### 2. 验证安装

```bash
node skills/sensen-pm-router/modules/test-task-store.js
node skills/sensen-pm-router/modules/test-intent-router.js
```

### 3. 基础使用

```javascript
// 在你的代码中引入
const TaskStore = require('./modules/task-store');
const IntentRouter = require('./modules/intent-router');
const SelfImproving = require('./modules/sensen-self-improving-v2');

// 创建任务
const task = TaskStore.createTask({
  title: '测试任务',
  assignedTo: 'Marketing',
  priority: 'P0'
});

// 路由
const result = IntentRouter.route('发布小红书内容');
console.log(result.agent); // 'Marketing'

// 记录纠正
SelfImproving.logCorrection({
  type: 'format',
  originalText: '太长了',
  correction: '输出简洁'
});
```

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                        OpenClaw Gateway                         │
├─────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐   │
│   │  Router    │───▶│  Sessions  │───▶│  Skills         │   │
│   └─────────────┘    └─────────────┘    └─────────────────┘   │
│         │                                       │              │
│         ▼                                       ▼              │
│   ┌─────────────────────────────────────────────────────┐     │
│   │              爱马仕增强层 Hermes Evolution            │     │
│   │  PM Router → Task Store → Self-Improving → Frozen   │     │
│   │  Intent Router → FTS Index → Progressive Disclosure│     │
│   │  Periodic Nudge → Honcho Profiler → AutoSkill     │     │
│   └─────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 配置

### Agent Profiles

编辑 `agent-profiles.js` 自定义 Agent 角色：

```javascript
const profiles = {
  Marketing: {
    keywords: ['小红书', '内容', '发布', '抖音', '知乎'],
    excludeWords: ['服务器', '代码', 'bug'],
    description: '负责内容运营和发布'
  },
  // ...
};
```

### 定时任务

编辑 `sensen-scheduler.js` 配置定时任务：

```javascript
const schedules = [
  { time: '09:00', name: '小红书热门', task: 'summarize_topics' },
  { time: '12:00', name: '觉醒日记', task: 'diary' },
  // ...
];
```

---

## 📖 API 参考

### TaskStore

```javascript
// 创建任务
TaskStore.createTask({ title, assignedTo, priority });

// 查询
TaskStore.queryByStatus('inbox');
TaskStore.queryByAssignee('Marketing');

// 统计
TaskStore.getStats();

// 看板
TaskStore.printKanban();
```

### IntentRouter

```javascript
// 路由
IntentRouter.route('发布小红书');

// 添加关键词
IntentRouter.addKeyword('AgentName', ['keyword1', 'keyword2']);
```

### SelfImproving

```javascript
// 记录纠正
SelfImproving.logCorrection({ type, originalText, correction });

// 获取规则
SelfImproving.getActiveRules();

// 匹配
SelfImproving.matchRule('太长了缩短');
```

### PeriodicNudge

```javascript
// 创建引擎
const engine = createEngine({ interval: 60 * 60 * 1000 });

// 启动
engine.start();

// 获取状态
engine.getSummary();
```

### HonchoProfiler

```javascript
// 获取画像
const profile = profiler.getProfile('user_001');

// 预测需求
profile.predictNeeds();

// 获取推荐
profile.getRecommendations();
```

---

## 🧪 测试

```bash
# 运行所有测试
node modules/test-task-store.js
node modules/test-intent-router.js
node modules/test-self-improving-v2.js
node modules/test-fts-indexer.js
node modules/test-honcho-profiler.js
node modules/test-periodic-nudge.js
node modules/test-auto-skill-generator.js
node modules/test-logger.js
node modules/test-dag.js
node modules/test-template.js
node modules/test-collaborator.js
node modules/test-collab-visualizer.js
```

---

## 🔧 故障排查

### 常见问题

**Q: TaskStore 查询返回空**
```javascript
// 检查索引
console.log(TaskStore.getStats());
// 重建索引
TaskStore.rebuildIndex();
```

**Q: IntentRouter 路由错误**
```javascript
// 检查关键词
console.log(IntentRouter.getKeywords());
// 添加缺失的关键词
IntentRouter.addKeyword('Agent', ['keyword']);
```

**Q: Self-Improving 不生效**
```javascript
// 检查规则文件
const fs = require('fs');
console.log(fs.readdirSync('./rules'));
```

---

## 📝 更新日志

### v1.0.0 (2026-04-11)
- 初始发布
- 23 个核心模块
- P0/P1/P2 完整功能

---

## 📄 许可证

MIT License

---

## 👤 作者

**森森** - 苍苍子森的 AI 助理

---

*最后更新: 2026-04-11*
