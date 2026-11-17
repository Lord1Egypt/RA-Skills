# 子 skill 调用协议

> 配套主 skill: [SKILL.md](../SKILL.md)
> v2.0.0 新增：Econ 分支子技能调用协议 + 跨学科共享子技能调用协议

## 调用流程

### 1. 读取子 skill SKILL.md

```
读取 ~/.claude/skills/<sub-skill>/SKILL.md
```

### 2. 按子 skill 路由协议执行

让子 skill 的 SKILL.md 主导执行。**不要从 router 凭记忆执行**。

### 3. 双层架构处理

如果子 skill 也是 static/dynamic 双层架构（如 nature-reader / nature-writing / nature-polishing / econ-write），继续读取：

1. 子 skill 的 `manifest.yaml` 检测任务类型
2. 按 axis 加载 `static/` 下的对应片段
3. **不要一次性读全部片段**——按需加载节省 token

## 双层架构子 skill

### STEM 分支双层架构

| Skill | 加载策略 |
|---|---|
| nature-reader | 按 source_format (pdf-text/scanned-pdf/html/doi-arxiv/pasted-text) |
| nature-writing | 按 task/paper_type/section/language/journal |
| nature-polishing | 按 paper_type/section/language/journal |
| nature-figure | 按 backend (Python/R) 或 OpenRouter AI 路线 |
| nature-paper2ppt | 按 paper_type (discovery/methods) |
| nature-citation | 按操作模式 |
| nature-response | 按任务类型 |

### Econ 分支双层架构（v2.0.0 新增）

| Skill | 加载策略 |
|---|---|
| econ-write | 按 task（abstract/intro/lit/theory/empirical/tables/robustness/LaTeX） + paper_type + journal |
| cn-top-econ-writing | 按 mode（ER/MW/CIE/EQ 4 模式） + section + 门槛审计类型 |
| econ-table-figure-design | 按 table_type（main/robustness/heterogeneity/mechanism） + figure_type（event-study/trend/map/distribution） |
| econ-writing-workflow | 按 task_category（11 类任务分类） + reference_fragment（argument-logic/full-paper-drafting/literature-grounding/manuscript-voice/regression-results/english-diction/chinese-diction/journal-styles） |
| econ-writing-workflow-multiagent | 按 section_agent（intro/lit/theory/empirical/conclusion） + paper_state 协议 |

## 调用示例

### 示例 1: 读论文（STEM Phase 0a）

```
User: 我有一篇 PDF 想读
Router: 📍 学科分支：STEM
        📍 当前阶段：Phase 0a - 读论文
        🎯 路由到：nature-reader
[读取 ~/.claude/skills/nature-reader/SKILL.md]
[按 source_format=pdf-text 加载 static/ 片段]
[执行 reader 流程]
Router: ✅ 完成
        👉 下一步：Phase 0b 文献调研，或 Phase 1a 项目初始化
```

### 示例 2: 起草（STEM Phase 2a）

```
User: 帮我写引言
Router: 📍 学科分支：STEM
        📍 当前阶段：Phase 2a - 章节起草
        🎯 路由到：nature-writing
[读取 ~/.claude/skills/nature-writing/SKILL.md]
[按 task=drafting, section=introduction 加载 static/ 片段]
[执行写作流程]
Router: ✅ 完成
        👉 下一步：Phase 2b 结构优化，或 Phase 3a 图规划
```

### 示例 3: 经济学论文起草（Econ E-1，v2.0.0 新增）

```
User: 我有一篇 DiD 论文要写
Router: 📍 学科分支：Econ
        📍 当前阶段：E-1 - 全文起草
        🎯 路由到：econ-write（英文）/ cn-top-econ-writing（中文）
[询问投稿语言：英文 AER 系列 / 中文《经济研究》系列]
[按 task=drafting, paper_type=empirical, method=DiD 加载 static/ 片段]
[执行经济学写作流程：主结果 → 识别策略 → 数据 → 引言 → 文献 → 稳健 → 机制 → 结论]
Router: ✅ 完成
        👉 下一步：E-2 表图设计，或 E-3 论证逻辑审计
```

### 示例 4: 跨学科共享子技能（引用核验，v2.0.0 新增）

```
User: 帮我核验引用
Router: 📍 跨学科共享：引用核验
        🎯 路由到：nature-ref-verifier（共享）
[读取 ~/.claude/skills/nature-ref-verifier/SKILL.md]
[执行引用核验流程，与学科无关]
Router: ✅ 完成
        👉 下一步：如需 BibTeX 格式核验，追加 citation-verifier
```

### 示例 5: 经济学审稿模拟（Econ E-5a，v2.0.0 新增）

```
User: 模拟审稿我的经济学论文
Router: 📍 学科分支：Econ
        📍 当前阶段：E-5a - 审稿模拟
        🎯 路由到：nature-reviewer（共享，按经济学视角调整）
[读取 ~/.claude/skills/nature-reviewer/SKILL.md]
[按经济学视角调整审稿维度：Identification Quality / Data Quality / Robustness Coverage / Mechanism Credibility / Contribution Significance / Policy Implication]
[执行审稿模拟，生成 3 份 reviewer reports]
Router: ✅ 完成
        👉 下一步：E-5b 返修回复
```

## v2.0.0 调用协议新增规则

### Pre-Phase 学科识别必走
每次调用前先做 Pre-Phase 学科识别，将任务分流到 STEM 或 Econ 分支。详细规则见 [discipline-routing.md](discipline-routing.md)。

### 跨学科共享子技能
共享子技能（`paper-bootstrap` / `nature-ref-verifier` / `citation-verifier` / `submission-audit` / `nature-reviewer` / `nature-response`）两个分支都可调用，无需切换分支。

### Econ 分支可用性校验
进入 Econ 分支前，检查 `~/.claude/skills/econ-write/SKILL.md` 是否存在。不存在时提示用户安装 econ-* 扩展包。

### 分支切换
用户中途转向不同学科任务时，重新走 Pre-Phase 学科识别，不混合两个分支的工作流。
