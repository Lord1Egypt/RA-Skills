---
name: llm-wiki-health-score
description: "当用户要求审计、评分、评估或监控 Obsidian/个人知识库是否符合卡帕西式 LLM Wiki 架构，或要求 WorkBuddy/Codex 对本地 Vault 生成知识库健康分、结构化信号和语义抽样最终评分时使用。关键词：LLM Wiki、Obsidian、个人知识库、健康分、语义抽样、WorkBuddy。"
metadata:
  version: "0.5.0"
---

# LLM Wiki 健康评分

## 概览

用于把本地个人知识库评价为卡帕西式 LLM Wiki。v0.5 不再把 `index.md`、`核心文件索引.md` 或架构不完整作为硬门槛；除根路径不可读或没有可解析文件外，都进入评分。架构符合度作为一个低分维度进入总分。

最终分数定义：

`LLM Wiki 健康分 v0.5 = 文献支撑维度 + 工程初始权重 + 结构化信号 + LLM 语义抽样 + 脚本合并最终分`

没有语义评分 JSON 时，不报告最终总分。

## 执行流程

默认产物目录：

```text
<被评估知识库根目录>/.<工具名称>/llm-wiki-health/
```

WorkBuddy 默认工具名是 `workbuddy`，因此默认产物目录是：

```text
<被评估知识库根目录>/.workbuddy/llm-wiki-health/
```

1. 运行扫描脚本，生成报告和语义评分模板。脚本会跳过当前工具的产物目录，避免把上一轮报告当作知识库内容再次扫描。

```powershell
python "D:\WorkBuddy_Data\.workbuddy\skills\llm-wiki-health-score\scripts\score_vault.py" --root "D:\Obsidian Vault" --format markdown --tool-name workbuddy
```

机器读取结构信号时使用 JSON：

```powershell
python "D:\WorkBuddy_Data\.workbuddy\skills\llm-wiki-health-score\scripts\score_vault.py" --root "D:\Obsidian Vault" --format json --tool-name workbuddy
```

首轮扫描默认写入：

- `<root>/.workbuddy/llm-wiki-health/llm-wiki-health-report.md` 或 `.json`。
- `<root>/.workbuddy/llm-wiki-health/semantic_scores.json`。

如需其他工具名，传 `--tool-name codex`，目录变为 `<root>/.codex/llm-wiki-health/`。如需完全指定目录，传 `--artifact-dir "<path>"`。

自动化或 CI 需要强制拿到最终分时，增加 `--require-final`。此时 `needs_semantic_sampling` 会返回非 0 退出码，避免上游误把半成品当作最终评分。

2. 检查 `status`。

| `status` | 处理方式 |
|---|---|
| `unscorable` | 停止。根路径不可读或没有可解析文件，无法评分。 |
| `needs_semantic_sampling` | 继续语义抽样。此时没有最终总分。 |
| `semantic_input_invalid` | 修正语义 JSON 后重跑。不要口头合并。 |
| `scored` | 已完成最终评分。 |

3. 读取评分依据和样本。

- 必读：`references/scoring_model.md`。
- 需要解释维度合理性或论文支撑时读取：`references/dimension_design_rationale.md`。
- 语义抽样必须使用固定探针问题：`references/probe_questions.md`。
- 按 `<root>/.<工具名称>/llm-wiki-health/semantic_scores.json` 的 `samples` 读取 schema、wiki、raw、index/log 等样本。
- 样本不足时，顺着样本中的 Wiki 链接、raw/source 链接和同目录规则补充证据。

4. 填写 `semantic_scores.json`。

每个维度都必须填写：

- `score`：`0-100`。
- `criteria`：每个细分项 `0-5`。
- `evidence`：至少 1 条，每条必须含 `file` 与 `note`。
- `samples`：样本级评分；知识沉淀和检索维度应尽量逐页/逐问给证据。
- `risks`：不确定、样本不足、证据冲突或陈旧风险。

脚本会校验维度 `score` 与 `criteria` 均值是否明显背离；背离过大时拒绝合并。结构化信号和语义抽样分差过大时不拒绝合并，但会写入复核提示。

5. 让脚本合并最终分：

```powershell
python "D:\WorkBuddy_Data\.workbuddy\skills\llm-wiki-health-score\scripts\score_vault.py" --root "D:\Obsidian Vault" --format markdown --semantic-input "D:\Obsidian Vault\.workbuddy\llm-wiki-health\semantic_scores.json" --tool-name workbuddy
```

只有输出 `score_type = final_integrated_semantic_sampling` 时，才能称为最终评分。若传入 `--require-final`，未形成最终评分会返回非 0 退出码。

## 评分维度

| 维度 | 权重 | 评估对象 |
|---|---:|---|
| `llm_wiki_architecture_fit` | 20% | raw/wiki/schema 三层、ingest/query/lint 操作、关系维护和可演化组织方式。 |
| `source_traceability` | 20% | wiki 结论能否回到 raw/source/core note，证据链是否可恢复。 |
| `schema_governance_quality` | 15% | AGENTS/RULES 等规则是否完整、一致、无歧义、可验证、可追溯、可维护。 |
| `knowledge_sedimentation_effectiveness` | 25% | 最新 wiki 沉淀是否忠实、完整、连贯、可复用。 |
| `retrieval_answerability` | 10% | 能否快速定位上下文，并产出相关、忠实、可引用答案。 |
| `maintenance_evolution` | 10% | 日志、lint、过期检测、冲突处理和修复流程是否支撑持续演化。 |

权重是工程初始权重，不是论文验证过的通用权重。若用户要求严格校准，使用历史查询任务、答案正确率、来源引用正确率、复用率和用户满意度做再标定。

## 架构处理

- `raw/`、`wiki/`、`AGENTS.md`、`RULES.md` 是卡帕西式 LLM Wiki 的核心结构信号，但缺失时只降低 `llm_wiki_architecture_fit`，不直接返回 0。
- `index.md` 和 `核心文件索引.md` 是可选导航/检索信号，不是必需项。
- `log.md` 是维护证据，不是架构硬 gate。
- “Core Notes 或等价关系维护协议”不能由 LLM 自由判定。脚本只采纳可观察证据：`CORE_RELATIONSHIPS_V1`、`obsidian-core-notes`、关系块、backlink/graph 维护描述、lint/refresh/validate 命令等。LLM 只评价证据清晰度和可执行性。

## 输出规则

- 最终报告只给一个完整知识库评分。
- 不单独输出“结构化总分”；结构化信号只作为各维度依据。
- 每个维度必须解释：评估什么、得分、证据、语义抽样发现、扣分原因和改进建议。
- 不能只在回复中口头给语义分；必须写入 JSON，并让脚本合并。
- 正文来源统计会剥离 `CORE_*` 自动生成块，避免关系块里的 raw 链接让来源支撑虚高。
- `source_traceability.metrics.source_recoverability_score` 扩展原 `sidecar_score`：综合 sidecar、source manifest、正文 source citation、frontmatter `source_scope`、机器索引和外部索引数据库；`sidecar_score` 只作为组件保留。
- Wiki 链接解析会识别悬空链接和同名歧义链接；同名文件不会被静默覆盖。
- 评分产物默认写入被评估知识库根目录下的 `.<工具名称>/llm-wiki-health/`，不写到 skill 目录。
- 如果目标根目录是 `D:\Obsidian Vault`，写入产物后遵守本地 `AGENTS.md` / `RULES.md`，按需要运行 Core Notes 公开命令行流程；若只用 `--no-artifacts` 做只读扫描，则不需要。

## 资源

- `scripts/score_vault.py`：确定性扫描、语义模板生成、语义 JSON 校验、最终分合并。
- `scripts/test_score_vault.py`：评分契约单元测试。
- `references/scoring_model.md`：维度、权重、语义评分细则和合并公式。
- `references/dimension_design_rationale.md`：维度设计合理性、论文/理论映射、误判控制。
- `references/probe_questions.md`：固定探针问题集，用于保持语义抽样可复核、可比较。
