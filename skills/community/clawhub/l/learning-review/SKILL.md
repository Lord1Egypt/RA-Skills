---
name: learning-review
description: >
  学用结合的回顾机制。包含三个回顾环节：学后复盘（每次学完）、周内化（每周一次）、应用检查（每两周一次）。
  将学习成果转化为 Agent 的实际工作能力，防止"学完就忘"。
  触发词："回顾", "复盘", "内化", "学习回顾", "learning review", "retrospective"。
---

# Learning Review — 学用结合回顾机制

学完不是终点，用上才是。本 skill 是 daily-learning 的配套闭环，确保学到的知识变成 Agent 的日常工作能力。

## 前置条件

本 skill 依赖 daily-learning 的标准目录结构：

```
<workspace>/learning/
├── LEARNING.md          # 学习进度
├── notes/               # 每日学习笔记
└── reviews/             # 回顾报告（本 skill 创建）
    ├── post-learning/   # 学后复盘
    ├── weekly/          # 周内化报告
    └── application/     # 应用检查
```

## 三种回顾模式

### 模式 A：学后复盘（Post-Learning Review）

**时机**：daily-learning Step 5（双写 Wiki）完成后，立刻执行
**耗时**：3-5 分钟

**流程**：

1. 读取刚才写的学习笔记
2. 生成复盘报告，保存到 `<workspace>/learning/reviews/post-learning/YYYY-MM-DD.md`

**复盘模板**：

```markdown
# 学后复盘 - YYYY-MM-DD

## 学习主题
<topic>

## 一句话总结
<费曼法：用最通俗的话概括核心>

## 和我工作的关系
- 直接能用：<列出可以马上应用的点，具体到"在什么场景下做什么">
- 未来有用：<需要积累或特定条件才用得上的>
- 无关：<学完发现跟自己领域不大的，简要说明为什么>

## 待内化项
- [ ] → AGENTS.md：<需要更新的具体内容>
- [ ] → TOOLS.md：<需要更新的具体内容>
- [ ] → SOUL.md：<需要更新的具体内容>
- [ ] → MEMORY.md：<需要记录的重要洞察>

## 遗留问题
<学完还搞不懂的，或需要进一步探索的>
```

**规则**：
- 没有就写"暂无"，不硬凑
- "直接能用"必须具体，不能写"可以提升工作效率"这种废话
- 不推群，安静执行

---

### 模式 B：周内化（Weekly Internalization）

**时机**：每周一次（建议周日），通过 cron 触发
**耗时**：10-15 分钟

**流程**：

1. 扫描本周 `learning/notes/` 下所有笔记
2. 读取对应的 `learning/reviews/post-learning/` 复盘报告
3. 识别所有标记了"待内化"的条目
4. 执行内化——更新 Agent 自身文件
5. 写内化报告

**内化动作**：

| 学到的内容类型 | 内化到 | 怎么改 |
|---------------|--------|--------|
| 工作流程改进 | AGENTS.md | 添加/修改对应流程步骤 |
| 工具使用经验 | TOOLS.md | 添加工具配置、技巧 |
| 认知/态度/方法论 | SOUL.md | 调整原则、风格描述 |
| 重要事件/决策 | memory/YYYY-MM-DD.md | 记录当天的 memory |
| 通用知识洞察 | MEMORY.md | 添加到长期记忆 |

**周内化报告模板**，保存到 `<workspace>/learning/reviews/weekly/YYYY-Www.md`（如 `2026-W20.md`）：

```markdown
# 周内化报告 - YYYY 第 Www 周 (MM-DD ~ MM-DD)

## 本周学习概览
- 共学习 <N> 个主题
- 主题列表：<topic1>, <topic2>, ...

## 已内化
| 内容 | 内化到 | 改了什么 |
|------|--------|---------|
| <topic> | AGENTS.md | <具体改动> |
| <topic> | TOOLS.md | <具体改动> |

## 未内化（及原因）
- <topic>：<为什么还没内化，比如"需要更多实践验证">

## 本周最有价值的收获
<一条，最多两条，用费曼法写>

## 下周关注
<基于本周学习，下周应该重点什么>
```

**关键原则**：
- 内化不是复制粘贴，是**用自己的话重写成行动指南**
- "我知道了" → "我改变了行为" 才算内化
- 不推群（除非发现重要洞察值得分享）

---

### 模式 C：应用检查（Application Check）

**时机**：每两周一次，通过 cron 触发
**耗时**：10-15 分钟

**流程**：

1. 读取最近 14 天的 memory 文件（`memory/*.md`）
2. 读取最近 14 天的学习笔记（`learning/notes/*.md`）
3. 交叉比对：学习笔记中的知识点，有没有在日常工作中出现
4. **"提到就算应用"**：在对话/文档中提到学过的概念、用了学过的方法，都算

**应用检查报告模板**，保存到 `<workspace>/learning/reviews/application/YYYY-MM-DD.md`：

```markdown
# 应用检查 - YYYY-MM-DD

## 回顾周期：MM-DD ~ MM-DD

## 学习了什么
- <topic1> (MM-DD)
- <topic2> (MM-DD)

## ✅ 已应用
- **<topic>** → 在 <场景> 中使用了，效果：<具体描述>

## ❌ 未能应用
- **<topic>** → 原因：<没遇到场景/忘了/不适用>

## 🔄 需要修正
- **<topic>** → 实践发现笔记中 <哪里不对>，应改为 <正确的理解>

## 应用率
<已应用数> / <学习总数> = XX%

## 行动项
- [ ] <基于检查结果的具体行动>
```

**关键原则**：
- 对自己诚实，"没用上"不丢人
- 应用率不是 KPI，是诊断工具。低说明学习方向或方式需要调整
- 关注"未能应用"的原因——如果是"不适用"，说明学偏了；如果是"忘了"，说明内化不够

---

## Cron 配置模板

### 周内化 cron

```
执行周内化任务。

遵循 learning-review skill 模式 B（周内化）：
1. 扫描本周 learning/notes/ 下的所有笔记
2. 读取对应的 learning/reviews/post-learning/ 复盘报告
3. 识别待内化项，执行内化（更新 AGENTS.md、TOOLS.md、SOUL.md、memory/）
4. 写内化报告到 learning/reviews/weekly/YYYY-Www.md

安静执行，不推群。
```

### 应用检查 cron

```
执行应用检查任务。

遵循 learning-review skill 模式 C（应用检查）：
1. 读取最近 14 天的 memory 文件
2. 读取最近 14 天的学习笔记
3. 交叉比对：哪些学过的知识在日常工作中被应用了
4. 写应用检查报告到 learning/reviews/application/YYYY-MM-DD.md

安静执行，不推群。
```

---

## 与 daily-learning 的集成

学后复盘（模式 A）应作为 daily-learning 的新 Step 5.5，在学习流程中自动触发。

建议修改 daily-learning 的 cron 描述，在 Step 5 后追加：

```
6. 执行学后复盘（learning-review skill 模式 A），保存到 learning/reviews/post-learning/
```

---

## 季度回顾（可选，不自动触发）

每季度末，可由人类或 learning-expert 发起：

1. 汇总本周所有 reviews/weekly/ 和 reviews/application/ 报告
2. 统计季度学用转化率
3. 识别持续"学了没用"的领域
4. 输出下季度学习建议

这个环节暂不自动化，需要人工判断。
