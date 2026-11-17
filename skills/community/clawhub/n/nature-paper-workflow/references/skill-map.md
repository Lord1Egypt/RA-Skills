# 全部 40 个子 skill 速查表

> 配套主 skill: [SKILL.md](../SKILL.md)
> v2.0.0 更新：新增 5 个 econ-* 子技能 + 跨学科共享基础设施段落

## 总览

| 类别 | 数量 | 来源 | 分支 |
|---|---|---|---|
| STEM 子技能 | 35 | Yuan1z/nature-skills + Boom5426/Nature-Paper-Skills | STEM 分支 |
| Econ 子技能 | 5 | juliaError/econ-TopJournal-writing-Skill（CC BY-NC 4.0） | Econ 分支 |
| 跨学科共享 | 5 | 上两组中跨学科通用的 | 两个分支 |
| 主路由器 | 1 | 本仓库 | - |
| **合计** | **40**（不含共享重复计数） | | |

## STEM 分支子技能（35 个）

### 输入侧（读论文 + 调研）

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-reader | 0a | 读论文、中英对照 | PDF/DOI/arXiv → 中英对照 reader |
| nature-academic-search | 0b | 找文献、PubMed | PubMed/Scopus 检索（含 MCP server） |
| nature-literature-pipeline | 0b | 文献流水线 | 批量检索 → 筛选 → 整理 |
| nature-paper-card | 0b | 论文卡片 | 论文卡片化整理 |
| nature-downloader | 0b | 论文下载 | PDF 下载 |
| academic-researcher | 0b | 综述、文献综述 | 文献综述与方法学支持 |
| results-analysis | 0b | 结论推导 | 实验输出转论文级结论 |

### 项目初始化

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| paper-bootstrap | 1a | 项目初始化、bootstrap | 项目目录初始化、状态文件 |
| nature-portfolio-playbook | 1b | 期刊选择、venue | Nature 系列定位与政策预检 |

### 起草与结构

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-writing | 2a | 写摘要、写引言、投稿包 | 章节起草 + 投稿包 |
| manuscript-optimizer | 2b | 结构修复、漂移 | claim/evidence/术语漂移修复 |
| results-section-revision | 2c | Results 修订 | Results 小节叙述结构修复 |

### 图与证据

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| figure-planner | 3a | 图规划、一图一主张 | 一图一主张、panel 角色 |
| nature-figure | 3b | 出图、科研绘图 | 投稿级科研绘图 + AI 示意图 |
| figure-style | 3c | 图检查、figure style | 出版级图形正确性 |

### 统计与数据

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| stats-reporting-audit | 4a | 统计审计、p值、n值 | n值/重复性/多重比较审计 |
| nature-statistics | 4b | 统计分析 | 统计计算 |
| nature-data | 4b | 数据处理 | 数据处理 |

### 引用与数据声明

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-ref-verifier | 5a | 引用核验 | 引用准确性、造假检测 |
| citation-verifier | 5a | BibTeX 卫生 | BibTeX 格式 + 严重度分级 |
| reference-audit-guide | 5a | 引用核验原则 | 引用核验原则参考 |
| nature-citation | 5b | 加引用、CNS 引用 | 自动补 CNS 严格引用 |
| data-availability | 5c | 数据声明、FAIR | 数据可用性声明 |

### 润色与预检

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-polishing | 6a | 润色、LaTeX 排版 | 段落级润色 + LaTeX |
| scientific-prose-style | 6a | 句子精修、em-dash | 句子级精修 |
| submission-audit | 6b | 投稿预检 | 全维度预检 |

### 审稿与返修

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-reviewer | 7a | 审稿模拟、预审 | 3 份 reviewer reports |
| nature-response | 7b | 返修、rebuttal | 逐点回复、标红修改 |

### 衍生场景

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| nature-paper2ppt | D1 | 转 PPT、组会汇报 | 论文 → 中文组会 PPT |
| nature-paper-to-patent | D2 | 转专利、国知局 | 论文 → 专利 |
| nature-proposal-writer | D3 | 写基金、申请书 | 基金申请书 |
| nature-experiment-log | D4 | 实验记录 | 实验记录管理 |
| conference-paper-writing | D5 | 会议论文、NeurIPS | NeurIPS/ICML/ICLR 流程 |

## Econ 分支子技能（5 个，v2.0.0 新增）

| Skill | 阶段 | 触发关键词 | 核心能力 |
|---|---|---|---|
| econ-writing-workflow | E-0 / E-3 | 经济学论文、输入审计、论证审计 | 11 类任务分类 + argument-logic / regression-results / manuscript-voice references |
| econ-write | E-1 / E-4 | 起草、写引言、AER 体例 | 英文经济学论文写作，融合 50+ 经济学家指南（Cochrane / McCloskey / Shapiro / Bellemare / Goldin / Glaeser / Kremer） |
| cn-top-econ-writing | E-1 / E-4 | 起草、经济研究体例 | 中文顶刊写作，4 模式（ER/MW/CIE/EQ）+ 4 门槛审计 |
| econ-table-figure-design | E-2 | 表图设计、三线表、回归表、事件研究图 | 经济学表图：三线表 + 主回归/稳健性/异质性/机制表 + 事件研究/趋势/地图/分布图 |
| econ-writing-workflow-multiagent | E-0~E-5（升级） | 复杂项目、多章节协同 | 多代理协调，paper_state 协议 + section agents |

## 跨学科共享基础设施（v2.0.0 新增）

以下子技能跨学科通用，两个分支都可调用：

| 功能 | 共享子技能 | 说明 |
|---|---|---|
| 项目初始化 | `paper-bootstrap` | 目录结构 + 状态文件，跨学科适用 |
| 引用核验 | `nature-ref-verifier` + `citation-verifier` + `reference-audit-guide` | 引用准确性 + BibTeX 格式，跨学科适用 |
| 投稿预检 | `submission-audit` | 通用投稿预检清单 |
| 审稿模拟 | `nature-reviewer` | 按学科视角调整审稿维度 |
| 返修回复 | `nature-response` | 逐点回复 + cover letter + 标红修改 |

## 共享支持包

| Skill | 用途 |
|---|---|
| nature-shared | 被其他 skill 引用的共享参考资料（不直接调用） |

## 路由层（共存）

| Skill | 用途 |
|---|---|
| paper-workflow | Boom5426 原版顶层路由（与 nature-paper-workflow 共存） |

---

## 互补协同使用规则

### 引用核验协同（Phase 5a / E-3 共享）

```
Step 1: nature-ref-verifier  → 检查引用内容准确性
Step 2: citation-verifier    → 检查 BibTeX 格式卫生
Step 3: reference-audit-guide → 引用核验原则参考
```

### 润色协同（Phase 6a）

```
Step 1: nature-polishing         → 段落级润色 + LaTeX 排版
Step 2: scientific-prose-style   → 句子级精修
```

### 场景路由

- **期刊投稿**：nature-writing + nature-polishing
- **会议论文**：conference-paper-writing + scientific-prose-style
- **中文组会**：nature-paper2ppt
- **经济学英文顶刊**：econ-write + econ-table-figure-design + submission-audit
- **经济学中文顶刊**：cn-top-econ-writing + econ-table-figure-design + submission-audit
- **经济学复杂项目**：econ-writing-workflow-multiagent（多代理协调）

## Econ 扩展包许可证声明

econ-* 5 个子技能来自 `juliaError/econ-TopJournal-writing-Skill` 仓库，采用 **CC BY-NC 4.0** 许可（非商用）。
本 router（`nature-paper-workflow`）仅做路由，不复制 econ-* 内容。
用户需从原仓库独立安装：https://github.com/juliaError/econ-TopJournal-writing-Skill

`econ-write` 上游依赖 `hanlulong/econ-writing-skill`（MIT），但 `juliaError` 仓库改造部分为 CC BY-NC 4.0。
