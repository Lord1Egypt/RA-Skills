# 🦁 Hermes Evolution - 爱马仕自动进化版

> OpenClaw 的智能增强层，让 AI 助理从被动响应变为主动服务

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw/skill-hermes-evolution)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| ⚡ **高性能** | FTS 检索 0.03ms/次，任务查询 O(1) |
| 🎯 **主动智能** | Periodic Nudge 主动自检，提前发现问题 |
| 🔮 **自动进化** | AutoSkillGenerator 自动创建 Skill |
| 👤 **用户理解** | Honcho 用户画像 + 需求预测 |
| 💾 **稳定记忆** | Frozen Memory 分层管理 |
| 📊 **学习闭环** | Self-Improving v2 规则权重 |

---

## 🚀 快速开始

### 安装

```bash
# 方式一：ClawhHub 安装（推荐）
clawdhub install hermes-evolution

# 方式二：手动安装
# 将此仓库克隆到你的 skills 目录
git clone https://github.com/openclaw/skill-hermes-evolution.git skills/hermes-evolution
```

### 验证安装

```bash
# 运行核心测试
node hermes-evolution/modules/test-task-store.js
node hermes-evolution/modules/test-intent-router.js

# 如果看到 "✅ 测试完成" 即安装成功
```

### 基础使用

```javascript
// 引入模块
const TaskStore = require('./hermes-evolution/modules/task-store');
const IntentRouter = require('./hermes-evolution/modules/intent-router');

// 创建任务
const task = TaskStore.createTask({
  title: '发布小红书内容',
  assignedTo: 'Marketing',
  priority: 'P0'
});

// 智能路由
const result = IntentRouter.route('帮我写一篇关于职场成长的笔记');
console.log(result.agent); // 'Marketing'
console.log(result.confidence); // 0.85
```

---

## 📦 核心模块

### 路由系统
- `intent-router.js` - TF-IDF 置信度路由
- `sensen-pm-router.js` - PM 路由核心

### 任务管理
- `task-manager.js` - 任务状态机
- `task-store.js` - 内存缓存 + 索引
- `task-dag.js` - DAG 依赖管理

### 学习进化
- `self-improving-v2.js` - 规则权重学习
- `frozen-memory.js` - 冻结记忆
- `patch-store.js` - 增量更新

### 智能增强
- `fts-indexer.js` - 全文检索
- `progressive-disclosure.js` - Token 控制
- `periodic-nudge.js` - 主动自检
- `auto-skill-generator.js` - 自动创建 Skill
- `honcho-profiler.js` - 用户画像

---

## 🧪 测试

```bash
# 全部测试
npm test

# 分类测试
npm run test:core    # 核心模块
npm run test:ai      # AI 模块
```

---

## ⚙️ 配置

### Agent Profiles

```javascript
// modules/agent-profiles.js
const profiles = {
  Marketing: {
    keywords: ['小红书', '内容', '发布'],
    excludeWords: ['服务器', '代码'],
    description: '内容运营 Agent'
  },
  Strategy: {
    keywords: ['战略', '规划', '分析'],
    excludeWords: [],
    description: '战略规划 Agent'
  }
};
```

### Nudge 引擎

```javascript
const engine = createEngine({
  interval: 60 * 60 * 1000  // 1小时检查一次
});
engine.start();
```

---

## 📖 文档

- [完整文档](SKILL.md) - 详细 API 参考和架构设计
- [快速参考](docs/QUICK-REF.md) - 常用命令速查
- [部署清单](docs/DEPLOY-CHECKLIST.md) - 安装检查清单

---

## 🔄 与原生 OpenClaw 对比

| 维度 | 原生 OpenClaw | Hermes Evolution |
|------|--------------|------------------|
| 响应模式 | 被动等指令 | 主动服务 |
| 记忆系统 | 简单 JSON | Frozen Memory |
| 学习能力 | 无 | Self-Improving v2 |
| 检索性能 | O(n) 遍历 | FTS 0.03ms |
| 用户理解 | 无 | Honcho 画像 |
| 任务管理 | 无 | DAG + 状态机 |

---

## 🐛 问题反馈

如果你遇到问题：

1. 检查 [故障排查](SKILL.md#故障排查) 部分
2. 运行测试验证：`npm test`
3. 查看日志：`modules/.logs/`

---

## 📝 更新日志

### v1.0.0 (2026-04-11)
- ✅ 初始发布
- ✅ 23 个核心模块
- ✅ P0/P1/P2 完整功能

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👤 作者

**森森** - 苍苍子森的 AI 助理

*让 AI 助理从工具变成伙伴*

---

<p align="center">
  <strong>Hermes Evolution - 爱马仕自动进化版</strong><br>
  让 OpenClaw 更智能、更主动、更懂你
</p>
