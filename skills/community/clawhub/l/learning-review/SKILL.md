---
name: learning-review
description: >
  学用结合的回顾机制。包含五个回顾环节：学后复盘（每次学完）、周内化（每周一次）、应用检查（每两周一次）、压缩归档（每月一次）、知识落地（每周一次）。将学习成果转化为 Agent 实际工作能力，防止"学完就忘"。
  触发词："回顾", "复盘", "内化", "学习回顾", "learning review", "retrospective", "知识落地", "压缩归档"。
  Not for: 首次学习新知识（用 daily-learning）、非学习类的定期回顾。
---

# Learning Review — 学用结合回顾机制

学完不是终点，用上才是。本 skill 是 daily-learning 的配套闭环，确保学到的知识变成 Agent 的日常工作能力。

## 前置条件

依赖 daily-learning 的标准目录结构。如 `learning/reviews/` 不存在：

```bash
mkdir -p <workspace>/learning/reviews/{post-learning,weekly,application,archive,integration}
```

## 五种回顾模式

### 模式 A：学后复盘（Post-Learning Review）

**时机**：daily-learning Step 5 完成后立刻执行 | **耗时**：3-5 分钟

1. 读取刚才写的学习笔记
2. 生成复盘报告，保存到 `learning/reviews/post-learning/YYYY-MM-DD.md`

核心是回答三个问题：**直接能用什么？待内化什么？遗留什么问题？** "直接能用"必须具体到场景，不能写废话。

> 模板见 [references/templates.md](references/templates.md) → 模式 A

---

### 模式 B：周内化（Weekly Internalization）

**时机**：每周一次（建议周日），cron 触发 | **耗时**：10-15 分钟

1. 扫描本周 `learning/notes/` 所有笔记
2. 读取对应的 `learning/reviews/post-learning/` 复盘报告
3. 识别所有标记"待内化"的条目
4. 执行内化——更新 Agent 文件（AGENTS.md / TOOLS.md / SOUL.md / memory/ / MEMORY.md）
5. 写内化报告到 `learning/reviews/weekly/YYYY-Www.md`

**内化判断三问**：改变了我怎么做事？→ AGENTS.md | 给了新工具/方法？→ TOOLS.md | 改变了怎么想问题？→ SOUL.md。三个都"没有"则不到内化时机。

> 模板见 [references/templates.md](references/templates.md) → 模式 B（含内化动作对照表、各角色侧重点）

**关键原则**：内化不是复制粘贴，是用自己的话重写成行动指南。"我知道了" → "我改变了行为" 才算内化。

---

### 模式 C：应用检查（Application Check）

**时机**：每两周一次，cron 触发 | **耗时**：10-15 分钟

1. 读取最近 14 天的 `memory/*.md` 和 `learning/notes/*.md`
2. 交叉比对：学习笔记中的知识点有没有在日常工作中出现
3. **"提到就算应用"**：在对话/文档中提到学过的概念、用了学过的方法，都算
4. 写报告到 `learning/reviews/application/YYYY-MM-DD.md`

**关键原则**：对自己诚实，应用率是诊断工具不是 KPI。"未能应用"原因——"不适用"说明学偏了，"忘了"说明内化不够。

> 模板见 [references/templates.md](references/templates.md) → 模式 C

---

### 模式 D：压缩归档（Archive & Compress）

**时机**：每月一次，cron 触发 | **耗时**：10-15 分钟

1. 扫描 inline 文件（AGENTS.md, SOUL.md, MEMORY.md），检查是否超过 ~150 行
2. 识别可移出内容：不需每次对话看到的细节、已内化知识、过时上下文
3. 将移出内容写入 `references/<topic>.md`
4. 在 inline 文件中替换为摘要 + 指针（`详见 references/<topic>.md`）
5. 将不再需要的笔记从 `learning/notes/` 移至 `learning/archive/`

**判断标准**：连续 3 次回顾都没被用到的信息 → 移出 inline。

---

### 模式 E：知识落地（Knowledge Integration）

**时机**：每周一次，在模式 B 之后执行，或独立触发 | **耗时**：5-10 分钟

**目的**：确保学习不只停留在笔记层面，而是落地到行为准则或工作流程中。

1. 读取本周所有学习笔记和复盘报告
2. 对每条知识判断：能不能更新到 AGENTS.md（行为准则/认知）或某个 Skill（工作流程）里？

| 判断 | 行动 |
|------|------|
| 能落地到 AGENTS.md | 更新行为准则/认知/规则 |
| 能优化某个 Skill | 找到对应 Skill 文件，修改流程/步骤 |
| 暂时无法落地 | 标记"待验证"，下次回顾再检 |
| 纯知识储备 | 不强制落地，保持现状 |

3. 写知识落地报告到 `learning/reviews/integration/YYYY-MM-DD.md`

**关键原则**：不是每条知识都必须落地。但连续两周没有任何知识落地 → 学习方向或深度有问题。Skill 优化是最高价值的落地。

> 模板见 [references/templates.md](references/templates.md) → 模式 E

---

## 与 daily-learning 的集成

学后复盘（模式 A）应作为 daily-learning 的新 Step 5.5 自动触发。建议在 daily-learning 的 cron 描述中追加：

```
6. 执行学后复盘（learning-review skill 模式 A），保存到 learning/reviews/post-learning/
```

## Cron 配置

所有模式的 cron 模板见 [references/cron-templates.md](references/cron-templates.md)。

## 季度回顾（可选，不自动触发）

每季度末由人类或 learning-expert 发起：汇总 reviews/weekly/ 和 reviews/application/ 报告，统计季度学用转化率，识别持续"学了没用"的领域，输出下季度学习建议。暂不自动化。
