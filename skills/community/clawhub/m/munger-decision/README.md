# 芒格决策助手 Skill

将查理·芒格的 60+ 思维模型转化为可执行的决策工具。

---

## 🎯 核心功能

1. **场景识别：** 自动识别决策场景（投资、产品、人员、战略）
2. **模型推荐：** 根据场景推荐 3-5 个相关思维模型
3. **引导式分析：** 通过结构化问题引导用户思考
4. **决策报告：** 生成 Markdown 格式的分析报告

---

## 📦 安装

```bash
cd /root/.openclaw/workspace/agents/edu-team/dev/munger-decision
npm install
```

---

## 🚀 使用方法

### 命令行

```bash
# 开始决策分析
/munger analyze 是否应该投资中宠股份

# 查看所有模型
/munger models

# 查看历史记录
/munger history
```

### 代码调用

```typescript
import { assistant } from './src/index';

// 开始分析
const response = await assistant.startAnalysis('session-123', '是否应该投资中宠股份');
console.log(response);

// 处理回答
const next = await assistant.handleAnswer('session-123', '7分，我对行业有一定了解');
console.log(next);
```

---

## 🏗️ 架构设计

### 模块划分

```
src/
├── index.ts          # 主入口
├── detector.ts       # 场景识别器
├── recommender.ts    # 模型推荐引擎
├── dialogue.ts       # 对话管理器
├── reporter.ts       # 报告生成器
└── types.ts          # 类型定义

data/
├── scenarios.json    # 场景库
└── models.json       # 模型库
```

### 核心流程

```
用户输入
    ↓
场景识别（detector）
    ↓
模型推荐（recommender）
    ↓
多轮对话（dialogue）
    ↓
报告生成（reporter）
```

---

## 🧪 测试

```bash
npm test
```

---

## 📊 数据结构

### 场景定义

```json
{
  "id": "investment",
  "name": "投资决策",
  "keywords": ["投资", "股票", "买入"],
  "patterns": ["是否.*投资"],
  "models": ["06", "10", "09", "07", "44"]
}
```

### 模型定义

```json
{
  "id": "06",
  "name": "能力圈",
  "category": "core",
  "description": "只在自己理解的领域做决策",
  "questions": [
    "你对这个领域的了解程度？（1-10分）",
    "你能清晰解释核心逻辑吗？"
  ],
  "scoring": {
    "8-10": "高（可以决策）",
    "5-7": "中等（需深入研究）"
  }
}
```

---

## 🎓 芒格模型应用

### 第一性原理

**核心问题：** 用户真正需要什么？
- 不是"学习芒格模型"
- 而是"做出更好的决策"

**设计推导：**
1. 最小化学习成本 → 自动场景识别
2. 结构化思考 → 引导式问题
3. 可执行建议 → 决策报告

### 逆向思维

**什么会导致失败？**
1. 场景识别不准 → 关键词 + 正则 + LLM 兜底
2. 问题太学术 → 白话文 + 实际案例
3. 报告太长 → 控制在 1 页内

### 能力圈

**我们擅长：**
- ✅ Node.js + TypeScript
- ✅ 状态机设计
- ✅ Markdown 生成

**我们不擅长：**
- ⚠️ 复杂 NLP → 简单规则 + LLM 兜底
- ⚠️ 前端 UI → MVP 纯命令行

---

## 📝 开发日志

### v1.0.0 (2026-03-25)

**已完成：**
- ✅ 场景识别器（关键词 + 正则匹配）
- ✅ 模型推荐引擎（基于场景映射）
- ✅ 对话管理器（状态机 + 会话管理）
- ✅ 报告生成器（Markdown 格式）
- ✅ 核心数据（4 场景 + 12 模型）

**待优化：**
- [ ] LLM 场景识别（提升准确率）
- [ ] 智能评分算法（基于答案内容）
- [ ] 历史记录持久化
- [ ] 更多模型（扩展到 60 个）

---

## 🤝 贡献指南

### 添加新场景

编辑 `data/scenarios.json`：

```json
{
  "id": "new-scenario",
  "name": "新场景",
  "keywords": ["关键词1", "关键词2"],
  "patterns": ["正则.*表达式"],
  "models": ["01", "06", "07"]
}
```

### 添加新模型

编辑 `data/models.json`：

```json
{
  "id": "99",
  "name": "新模型",
  "category": "category",
  "description": "模型描述",
  "questions": ["问题1", "问题2"],
  "scoring": {
    "good": "评分说明"
  }
}
```

---

## 📄 许可证

MIT

---

**开发者：** edu-dev  
**版本：** v1.0.0  
**日期：** 2026-03-25
