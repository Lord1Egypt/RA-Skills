---
name: munger-decision
description: "Charlie Munger's mental model decision assistant. Analyzes your decision scenario, recommends the most relevant thinking models, and guides you through structured analysis. Free version includes 12 core models. Use when: making investment, product, strategy, or life decisions. NOT for: general Q&A or information lookup."
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "version": "1.2.0",
        "license": "MIT",
        "requires": { "bins": ["node"] },
      },
  }
---

# 芒格决策助手

将查理·芒格的核心思维模型转化为可执行的决策工具。

**当前版本：** 免费版（12 个核心模型）  
**完整版：** 83 个模型 + 83 个详细文档（即将推出）

---

## 🎯 核心功能

1. **场景识别：** 自动识别决策场景（投资、产品、人员、战略）
2. **模型推荐：** 根据场景推荐 3-5 个相关思维模型
3. **引导式分析：** 通过结构化问题引导用户思考
4. **决策报告：** 生成 Markdown 格式的分析报告

---

## 📦 免费版包含的 12 个核心模型

### 核心决策模型（8 个）
1. **第一性原理** - 回归事物本质
2. **机会成本** - 评估替代方案
3. **复利效应** - 长期价值积累
4. **能力圈** - 了解自己的边界
5. **逆向思维** - 反过来想，避免失败
6. **护城河** - 竞争优势分析
7. **安全边际** - 容错空间评估
8. **多元思维模型** - 跨学科交叉验证

### 心理学模型（4 个）
9. **确认偏误** - 避免选择性证据
10. **锚定效应** - 警惕第一印象
11. **损失厌恶** - 理性评估风险
12. **社会认同** - 独立思考，避免从众

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
└── munger-knowledge.js  # 12 个核心模型库
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

---

## 🎁 完整版（即将推出）

完整版将包含：

### 83 个思维模型
- **核心模型（10 个）：** 多元思维、机会成本、复利效应等
- **心理学模型（29 个）：** 确认偏误、锚定效应、损失厌恶等
- **经济学模型（15 个）：** 供需关系、边际效用、规模经济等
- **数学模型（12 个）：** 概率论、贝叶斯、幂律分布等
- **物理学模型（8 个）：** 临界质量、杠杆原理、惯性等
- **生物学模型（9 个）：** 进化论、适者生存、生态位等

### 83 个详细文档
- 每个模型配有独立 Markdown 文档
- 包含定义、案例、应用场景、常见误区
- 总计超过 50,000 字的深度内容

### 高级功能
- 智能评分算法（基于 LLM 分析）
- 历史记录持久化
- 自定义模型库
- 批量决策分析

**敬请期待！**

---

## 📄 许可证

MIT

---

**开发者：** edu-dev  
**版本：** v1.2.0-free  
**日期：** 2026-03-29
