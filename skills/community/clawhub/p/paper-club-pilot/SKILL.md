---
slug: paper-club-pilot
name: paper-club-pilot
displayName: 【学术会议】学术组会引擎
version: 2.0.1
description: "Use when preparing for, running, or wrapping up a research group meeting / lab seminar / reading club — e.g. says '帮我们准备组会'、'推荐本周必读'、'生成研讨材料包'、'记录组会讨论'、'会后代组会沉淀'、'paper club prep'. Triggers before a Tencent Meeting group session (recommend readings + discussion kit), during it (capture discussion via smart notes), and after it (distill into the academic knowledge base). The highest-frequency academic meeting scenario."
agent_created: true
---

# 【学术会议】学术组会引擎 · Paper Club Pilot

组会是研究生的最高频会议。本技能覆盖组会全生命周期：会前按课题组方向从文献库推荐本周必读 + 生成研讨材料包（摘要/关键贡献/可复现性/讨论问题）；会中调用腾讯会议智能纪要做讨论记录；会后把结论沉淀进学术知识库。让每次组会都「有准备、有记录、有积累」。

Covers the full group-meeting lifecycle: pre-meeting reading curation + discussion kit, in-meeting capture via Tencent Meeting smart notes, post-meeting distillation into the knowledge base.

---

## 零、进化燃料 · 安装即开

> **📋 安装须知**：本技能安装后默认开启「进化燃料」——每次使用后自动记录方法层标签（只记方法名，绝不记你们组会聊了什么、你是谁），留在你本机用于持续优化本技能。如不需此服务，随时说「别记了」即可关闭。

---

## 何时使用 / When to use

- 会前：用户说「帮准备组会」「推荐本周必读」「生成研讨材料包」。
- 会中：用户说「记录组会讨论」「抓重点」「标记决策」。
- 会后：用户说「会后代沉淀」「把结论存进知识库」「整理行动项」。
- **不触发**：单篇文献把关（用 cjg-paper-fact-checker）、想法新颖性判断（用 novelty-validator）、答辩演练（用 defense-rehearsal）。

---

## 核心原则 / Core principle

**三阶段闭环，缺一不可。** 只做会前或只做会后，组会价值都打折。本技能把「准备→记录→沉淀」串成一条线。

**复用文献底座。** 会前推荐与材料包来自 global-biblio-base（12亿文献）；会后沉淀进 academic-knowledge-base。两个都是已有能力，本技能是它们的「组会编排层」。

**已真机验证（2026-07-18）**：会前推荐管线经真实 SmartLib 网关检索命中真实论文（方向「大语言模型+推理」共 2283 篇可推荐，配额真实计次），检索底座壁垒成立；会中捕获依赖用户授权腾讯会议数据、会后沉淀为编排逻辑，二者非独立外部依赖。

**课题组画像驱动。** 推荐质量取决于是否知道该组的方向。首次用会让用户填「课题组方向/近期关键词/必读清单」，存为轻量画像，后续复用。

---

## 主链路 / The pipeline

```
[课题组画像: 方向/关键词/必读]
        │
   ┌────┴─────┬──────────┐
   ▼          ▼          ▼
① 会前准备   ② 会中记录   ③ 会后沉淀
推荐必读     腾讯会议     蒸馏结论
+ 材料包     智能纪要     → 知识库
```

### ① 会前准备 (Prep) — 复用 global-biblio-base
- 按课题组画像，检索本周最相关的新文献 / 必读经典，给 3–5 篇「本周必读」候选。
- 对选定论文生成**研讨材料包**（每篇）：一句话摘要、关键贡献、可复现性初判、3 个讨论问题。
- 输出可直接贴进会议邀请/群公告。

### ② 会中记录 (Capture) — 腾讯会议智能纪要
- 调用腾讯会议技能拉取智能纪要 / 转写，提取：决策点、争议点、待办（行动项）、未决问题。
- 若用户实时说「记一下这个」，追加到当前纪要。

### ③ 会后沉淀 (Distill) — 复用 academic-knowledge-base
- 把会中结论、行动项、未决问题蒸馏成结构化条目，存入学术知识库。
- 更新课题组画像（新方向、新关键词）。
- 输出「组会小结」给 user 确认后归档。

---

## 腾讯会议接入 / Tencent Meeting integration

- **智能纪要 / 转写**：会中讨论记录的唯一输入源。
- **预定会议**：会前可辅助生成会议主题/议程并预定。
- **参会人信息**：标注谁负责哪个行动项，沉淀时可追溯。

调用前确认用户已授权该场会议数据访问。

---

## 非职责边界 / NON-mandate

- **不做** 单篇文献真实性把关 —— 用 cjg-paper-fact-checker。
- **不做** 想法新颖性判断 —— 用 novelty-validator。
- **不做** 答辩演练 —— 用 defense-rehearsal。
- **不替组会做决定** —— 只组织信息，决策在课题组。

---

## 外部标杆（全球）

> 标杆范围 = 全世界（所有技能/工具/论文/知识），不是某平台。paper-club-pilot 目标是 **Global-Best**，不是比赛第一。
> 一句话差异化：**唯一覆盖「组会全生命周期」（会前推荐必读 + 会中纪要捕获 + 会后知识沉淀）且锚定课题组画像的技能**。竞品几乎都只做单点：Elicit / Consensus 做文献问答、ResearchRabbit / Connected Papers 做文献图谱发现、ChatPDF / Scispace 做单篇 PDF 精读、Paperpal 做写作润色。壁垒：复用 global-biblio-base（12 亿文献池）+ 腾讯会议智能纪要 + academic-knowledge-base，本技能是它们的「组会编排层」。已知短板：会中纪要依赖用户授权会议数据、知识库蒸馏为辅助级。

---

> ⚙️ 本技能由「技能锻造炉」锻造
>
> 想让你的技能也越用越牛？用「技能锻造炉」创建并开启进化（在 SkillHub 搜索技能 slug「cjg-skill-forge」，认准这个唯一标识）。
