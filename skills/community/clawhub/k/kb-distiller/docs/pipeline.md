# 六阶段蒸馏规程（详细版）

本文件是各阶段规程（`prompts/*.md`）的统领，定义阶段间的数据流、预算、容错与合并规则。

## 数据流总览

```
domains/<domain>.json
        │
        ▼
[阶段1 Elicit] ──► corpus/<domain>/<sub>/elicited/<topic>.md   （模型内生知识，主源）
[阶段2 Ingest] ──► corpus/<domain>/<sub>/docs/<slug>.md        （文档锚点，辅源）
        │
        ▼
[阶段3 Distill] 双源融合 ──► output/<skill_name>/kb/<sub>.md + 横切文件
        │
        ▼
[阶段4 Assemble] ──► output/<skill_name>/SKILL.md
        │
        ▼
[阶段5 Validate] scripts/validate_skill.py ──► 校验报告（失败 → 回阶段3/4修复）
        │
        ▼
[阶段6 Install] 输出安装指引（不自动安装）
```

## 阶段 1 — Elicit 模型知识萃取（核心）

目标：把执行模型的**内生领域知识**系统性"挤出"，尤其是文档里查不到的隐性经验。

- 按领域配置逐 subdomain、逐 `elicitation_topics` 主题执行五轮萃取（广度轮 → 深度轮 → 自我质询轮 → 边界轮 → 法则化轮），详见 [prompts/elicitation.md](../prompts/elicitation.md)。
- 每个主题的萃取结果存为 `corpus/<domain>/<sub>/elicited/<topic>.md`，frontmatter 记录 `topic`、`rounds_completed`、`elicited_at`。
- 萃取时**不要**边萃取边润色成教程——保留原始密度（要点列表、错误/正确代码对照、典型报错原文），润色与结构化是阶段 3 的事。
- 优先深挖：坑点 > AI 典型错误 > 最佳实践 > 概念复述。概念复述只需最小必要量（心智模型级别）。

## 阶段 2 — Ingest 文档锚点抓取（辅助）

目标：为时效性硬事实（版本号、API 签名、破坏性变更、最新特性）提供外部锚点，并对模型知识做交叉验证。

- 每个子领域受 `page_budget` 约束（**上限而非目标**），抓取顺序：种子根页 → 从抓回内容中发现的升级/迁移/发布日志/版本页 → 入门页 → API 索引页。
- 容错：单页失败跳过并记录；种子根页失败 → 该子领域降级为纯模型知识模式。
- 抓取结果聚合存为 `corpus/<domain>/<sub>/docs/_anchors.md`（含抓取日志表与关键事实小节；单页过长时可按页拆分 `docs/<slug>.md`），frontmatter 记录 `fetched_at`。
- 详见 [prompts/ingest.md](../prompts/ingest.md)。

## 阶段 3 — Distill 双源融合蒸馏

目标：把两路语料融合为结构化、可长期使用的知识文件。

- 每个 subdomain 产出 `output/<skill_name>/kb/<sub>.md`；另产出横切文件（跨框架坑点 `gotchas.md`、通用模式 `patterns.md`、AI 典型错误 `ai-mistakes.md`，按领域配置的 `cross_cutting_files` 决定）。
- 扩展子领域（配置 `spin_off_subdomains`，如 ui-ux 域的 wcag22-audit / aria-patterns / industry-themes / app-templates）同样产出 `kb/<name>.md`，但其语料寄居 `corpus_home` 所指路径、无独立 elicited/docs 目录，**不参与常规重蒸**（仅当寄居语料更新时手动重蒸，见增量模式）。
- 融合规则：
  1. 模型知识与文档**一致** → 保留，标注 `[官方文档](url)`。
  2. **冲突** → 以文档为准（尤其版本号/API 签名/破坏性变更），冲突点在文件尾「冲突消解记录」小节登记。
  3. **模型独有**（文档没有的隐性经验、AI 典型错误）→ 保留，标注 `[模型经验]` 并附适用说明。
  4. **文档独有** → 保留，标注来源 URL。
- kb 文件骨架与质量红线见 [prompts/distill.md](../prompts/distill.md) 与 [skill-schema.md](skill-schema.md)。

## 阶段 4 — Assemble 组装

- 生成 `output/<skill_name>/SKILL.md`：frontmatter（name 与目录同名、description 关键词前置公式）+ kb 索引表 + 问题类型→kb 文件决策树 + Top 坑点内联摘要 + 知识回流章节。
- 详见 [prompts/assemble.md](../prompts/assemble.md)。

## 阶段 5 — Validate 校验

- 首选运行 `python <skill根>/scripts/validate_skill.py <产物目录> --keywords <description_keywords逗号列表>`。
- 编号法则体系产物另跑编号审计：`python <skill根>/scripts/audit_refs_react.py <产物目录>`（react 域；ui-ux 域用 `audit_refs.py`）——前缀连续性/断链/孤儿/corpus 路径全 0 才算过。
- Python 不可用 → 按 [prompts/validate.md](../prompts/validate.md) 人工清单逐项核对。
- 事实抽查（每 2 个蒸馏轮次至少 1 次）：`python <skill根>/scripts/spot_check.py <产物目录>` URL 探活 + agent 抽 ≥10 条硬事实比对来源，规程见 [prompts/validate.md](../prompts/validate.md)「事实抽查」。
- 失败 → 修复 → 重跑，直至全绿。校验是 pre-filter：通过后仍需人工/agent 抽查来源标注与内容真实性。

## 阶段 6 — Install 安装指引

- 报告产物路径；给出 OpenCode / Claude Code 两个平台的安装路径（见仓库 INSTALL.md）。
- 提醒：复制后重启 Agent；目录名必须与 `name` 一致。
- **不自动复制到全局目录**——安装是用户决策。

## 增量模式（--refresh）

- 重跑阶段 1（萃取）与阶段 2（抓取），但**合并非覆盖**：
  - kb 条目按主题/坑点粒度合并，已存在且未变化的保留原条目与原标注。
  - 文档版本变化 → 更新「版本注意」小节并在变更记录登记。
  - 新坑点/新主题 → 追加；被证伪的条目 → 移除并记录原因。
- 与 refine（日常回流）的区别：refresh 是全量重蒸馏的增量合并，refine 是单条知识的即时回写。
- 扩展子领域（`spin_off_subdomains`）不参与常规重蒸；仅当 `corpus_home` 寄居语料更新时手动重蒸对应 kb（合并非覆盖规则同上）。

## 预算与红线汇总

| 项 | 限制 |
|---|---|
| 每子领域抓取页数 | ≤ `page_budget`（上限而非目标） |
| 单 kb 文件 | 非空、≤2000 行、含「来源索引」小节 |
| 产物总体积 | ≤2MB（2048KB，`validate_skill.py MAX_TOTAL_BYTES` 红线；早期 300KB 红线已上调） |
| URL | 只从抓回内容中发现深层链接，禁止猜测 |
| 硬事实标注 | 版本号/API 签名必须有文档佐证（纯模型模式下在来源索引显式声明未经验证） |
