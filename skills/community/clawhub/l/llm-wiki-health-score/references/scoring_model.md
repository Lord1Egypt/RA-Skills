# LLM Wiki 健康评分模型 v0.5

## 评分原则

采用一体化评分：

1. 结构化扫描只生成客观信号，不生成最终总分。
2. LLM 语义抽样必须覆盖全部 6 个维度。
3. 脚本校验语义 JSON 后，按维度融合结构化信号和语义评分，生成唯一最终分。

除根路径不可读或没有可解析文件外，不使用架构硬门槛。知识库不符合卡帕西式 LLM Wiki 时，`llm_wiki_architecture_fit` 给低分，并拉低总分。

## 状态

| `status` | 含义 |
|---|---|
| `unscorable` | 根路径不可读或没有可解析文件。 |
| `needs_semantic_sampling` | 已完成结构化信号扫描，等待语义抽样；不能报告最终分。 |
| `semantic_input_invalid` | 语义 JSON 不合规，最终评分未生成。 |
| `scored` | 已完成结构化信号和语义抽样融合。 |

## 产物位置

默认产物目录：

```text
<被评估知识库根目录>/.<工具名称>/llm-wiki-health/
```

默认工具名是 `workbuddy`，所以 WorkBuddy 调用时写入：

```text
<root>/.workbuddy/llm-wiki-health/
```

默认文件：

| 文件 | 用途 |
|---|---|
| `llm-wiki-health-report.md` | Markdown 报告。 |
| `llm-wiki-health-report.json` | JSON 报告，取决于 `--format json`。 |
| `semantic_scores.json` | LLM 语义抽样填写模板。 |

命令行规则：

- `--tool-name <name>` 控制默认隐藏目录名：`.<name>/llm-wiki-health/`。
- `--artifact-dir <path>` 完全覆盖默认目录。
- `--out <path>` 只覆盖报告文件位置。
- `--semantic-template-out <path>` 只覆盖语义模板位置。
- `--no-report-artifact` 只打印标准输出，不写报告产物。
- `--no-artifacts` 只打印标准输出，不写报告或语义模板。
- `--require-final` 要求必须生成最终评分；若仍是 `needs_semantic_sampling`，返回非 0 退出码。
- 首轮扫描默认写报告和语义模板。
- 使用 `--semantic-input` 合并最终分时，默认只写报告，不覆盖已填写的 `semantic_scores.json`。

退出码约定：

| 退出码 | 含义 |
|---:|---|
| `0` | 扫描成功；若未传 `--require-final`，等待语义抽样也算成功。 |
| `2` | `unscorable`，根路径不可读或没有可解析文件。 |
| `3` | `semantic_input_invalid`，语义评分输入不合规。 |
| `4` | 传入 `--require-final` 但尚未形成最终分。 |

## 维度与权重

权重是工程初始权重，不是论文验证过的通用权重。

| 维度 | 权重 | 设计意图 |
|---|---:|---|
| `llm_wiki_architecture_fit` | 20 | 先确认知识库是不是接近 LLM Wiki，而不是散乱文件夹。 |
| `source_traceability` | 20 | LLM Wiki 价值依赖可回溯来源，防止漂亮总结脱离证据。 |
| `schema_governance_quality` | 15 | Schema 层决定 agent 是否能稳定维护知识库。 |
| `knowledge_sedimentation_effectiveness` | 25 | wiki 层的长期沉淀是最高价值产物，因此最高权重。 |
| `retrieval_answerability` | 10 | 查询体验重要，但部分依赖外部搜索工具，权重较低。 |
| `maintenance_evolution` | 10 | 维护能力防止衰减，属于长期健康护栏。 |

## 融合公式

每个维度都有结构化信号分和语义抽样分。最终维度分：

```text
dimension_score = structural_score * structural_weight + semantic_score * semantic_weight
```

| 维度 | 结构化信号权重 | 语义抽样权重 |
|---|---:|---:|
| `llm_wiki_architecture_fit` | 0.45 | 0.55 |
| `source_traceability` | 0.45 | 0.55 |
| `schema_governance_quality` | 0.35 | 0.65 |
| `knowledge_sedimentation_effectiveness` | 0.25 | 0.75 |
| `retrieval_answerability` | 0.40 | 0.60 |
| `maintenance_evolution` | 0.45 | 0.55 |

语义权重更高，因为结构化信号只能证明“有文件、有链接、有 marker”，不能证明“结论忠实、规则无歧义、查询真的能回答”。Schema 和知识沉淀尤其依赖语义判断。

总分：

```text
final_score = sum(dimension_score * dimension_weight)
```

## 结构化扫描补充规则

- 评分脚本会跳过当前工具的默认产物目录，例如 `.workbuddy/llm-wiki-health/` 或 `.codex/llm-wiki-health/`，也会跳过 `--artifact-dir` 指定的目录。
- 来源支撑统计会先剥离 `CORE_*` 自动生成块；只有正文中的 raw/source/core note 链接才计入来源可追溯信号。
- `source_recoverability_score` 取代单一 `sidecar_score` 作为结构化来源可恢复性主指标；组件权重为 sidecar 30%、source manifest 15%、frontmatter `source_scope` 20%、正文 source citation 20%、机器索引 10%、外部索引数据库 5%。
- `sidecar_score` 保留在 metrics 中作为组件：sidecar 覆盖高会加分，但不再是卡帕西式 wiki 知识库的必要组成条件。
- Wiki 链接解析使用三态结果：`resolved`、`ambiguous`、`dangling`。同名文件不会被静默覆盖；歧义链接会进入检索与维护维度的链接健康扣分。
- 维护日志新鲜度按可解析日期与当前日期的距离计算，不绑定固定年份。

## 语义抽样评分细则

### `llm_wiki_architecture_fit`

| 细项 | 5 分含义 |
|---|---|
| `raw_wiki_schema_layering` | raw/source、wiki/synthesis、schema/rules 分层清晰，职责边界稳定。 |
| `ingest_query_lint_operations` | 有可执行或可复述的 ingest、query、lint/validate、logging 流程。 |
| `agent_operationalization` | 未来 agent 能根据 schema 判断读取、写入、维护和验证步骤。 |
| `modularity_and_adaptability` | 结构允许局部替换工具或索引方式，不绑定单个文件名。 |

### `source_traceability`

| 细项 | 5 分含义 |
|---|---|
| `provenance_coverage` | 关键 wiki 结论覆盖主要 raw/source/core note 来源。 |
| `claim_source_alignment` | 抽样结论能被来源支持，没有明显无来源断言。 |
| `citation_granularity` | 引用粒度足够具体，能定位到文件、段落、会议、版本或证据。 |
| `source_recoverability` | sidecar、manifest、正文 source citation、frontmatter `source_scope`、机器索引或外部索引数据库足以让 agent 找回原始材料。 |

### `schema_governance_quality`

| 细项 | 5 分含义 |
|---|---|
| `completeness` | 规则覆盖范围、分层、取信、ingest、query、验证、日志和例外。 |
| `consistency` | `AGENTS.md`、`RULES.md` 和下级规则之间不互相冲突。 |
| `unambiguity` | 未来 agent 不需要猜测即可执行。 |
| `verifiability` | 规则能映射到可观察文件、命令、检查项或验收标准。 |
| `traceability` | 规则说明结论、来源、生成旁注和日志如何追溯。 |
| `maintainability` | 规则能演化，避免重复、陈旧和人工重建。 |

### `knowledge_sedimentation_effectiveness`

| 细项 | 5 分含义 |
|---|---|
| `groundedness` | 重要结论有 source/raw/core note 支撑。 |
| `completeness` | 覆盖当前主题目的所需的关键事实、口径和限制。 |
| `relevance_actionability` | 能支撑未来决策、回答、实现或复用。 |
| `coherence_readability` | 结构、术语、叙述清晰。 |
| `source_integration` | 不是简单摘抄，而是跨来源综合。 |
| `freshness_conflict_handling` | 能识别近期变化、陈旧结论和来源冲突。 |

### `retrieval_answerability`

| 细项 | 5 分含义 |
|---|---|
| `navigation_findability` | 从入口、索引、链接、标签或搜索能快速定位相关材料。 |
| `question_context_precision` | 查询样例返回的上下文聚焦，不被大量无关文件稀释。 |
| `answer_faithfulness` | 抽样回答忠实于检索到的上下文。 |
| `answer_relevance` | 抽样回答直接回应问题，并给出可用结论。 |

### `maintenance_evolution`

| 细项 | 5 分含义 |
|---|---|
| `logging_freshness` | 维护日志记录近期动作、范围、结果和风险。 |
| `staleness_detection` | 有发现过期结论、坏链、漂移或缺失旁注的机制。 |
| `conflict_handling` | 来源冲突会被标记、分级、追溯，而不是静默合并。 |
| `repair_workflow` | 有可执行的 refresh/reconcile/validate/lint 或等价修复流程。 |

## 语义 JSON 契约

所有维度必须存在：

```json
{
  "schema_version": "semantic-scores-v0.2",
  "dimensions": {
    "llm_wiki_architecture_fit": {
      "score": 0,
      "criteria": {
        "raw_wiki_schema_layering": 0,
        "ingest_query_lint_operations": 0,
        "agent_operationalization": 0,
        "modularity_and_adaptability": 0
      },
      "evidence": [
        {"file": "AGENTS.md", "note": "paraphrased evidence"}
      ],
      "risks": []
    }
  }
}
```

约束：

- `score` 必须是 `0-100`。
- 每个 criterion 必须是 `0-5`。
- 每个维度至少 1 条 evidence。
- evidence 必须是对象，包含 `file` 和 `note`。
- 没有 evidence 的维度不得给高分。
- 不允许 LLM 只凭“看起来像协议”判定等价关系维护协议；必须有文件证据。
- 维度 `score` 必须与 `criteria` 均值大体一致；差距超过阈值时脚本拒绝合并。
- 结构化信号分与语义抽样分严重背离时，脚本会输出复核提示。

## 固定探针问题

语义抽样必须读取 `references/probe_questions.md`。该文件给出每个维度的标准探针问题，用于提高不同轮次评分的可比较性。知识沉淀和检索维度至少回答 4 个探针问题，其余维度至少回答 2 个。每个回答都需要文件证据；找不到证据时记录风险，不用常识补齐。

## 分数区间

| 分数区间 | 解释 |
|---:|---|
| `0-39` | 很低。通常不是 LLM Wiki，或几乎没有可追溯沉淀。 |
| `40-59` | 低。局部有资料，但分层、来源、查询或维护缺口明显。 |
| `60-74` | 初步可用。结构存在，知识沉淀和可追溯性仍不稳定。 |
| `75-84` | 较健康。可支持日常使用，但仍有明显短板。 |
| `85-94` | 良好。结构、追溯、查询、维护多数稳定。 |
| `95-100` | 优秀。结构成熟，语义抽样和查询验证也稳定。 |

## 报告要求

最终报告必须包含：

- 总分和分数区间。
- 每个维度得分、权重、评估对象。
- 结构化证据和语义抽样证据。
- 扣分原因。
- 2-5 条优先改进建议。

不要报告单独的结构化总分。结构化信号只作为维度依据出现。
