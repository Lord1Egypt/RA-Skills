## Description:

运营-产品协同加速套件，用于将运营需求翻译为产品语言、生成效果归因框架、计算优先级、生成验收标准、对齐数据口径并生成协同文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, product, and growth teams use this Chinese-language skill to translate requirements, align metrics, reason about attribution, calculate prioritization, define acceptance criteria, and assemble collaboration documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill in general operations or product-planning conversations.

Mitigation: Prefer explicit slash-command use and confirm that the user wants an Ops-PM Bridge workflow before producing structured collaboration artifacts.

Risk: Generated prioritization, attribution, and acceptance criteria can be mistaken for final business decisions.

Mitigation: Treat outputs as drafts for operations and product stakeholders to review, adjust, and approve.

Risk: Illustrative SQL patterns in examples are not production-ready.

Mitigation: Convert sample SQL to parameterized, environment-specific queries before using it with real data systems.

## Reference(s):

- [Ops-PM Bridge skill page](https://clawhub.ai/lijinhongucl-pixel/skills/ops-pm-bridge)
- [运营-产品翻译词典](references/ops_pm_dictionary.md)
- [优先级计算权重配置](references/priority_weights.md)
- [效果归因模型说明](references/attribution_models.md)
- [协同文档示例](examples/example-ops-doc.md)
- [效果归因配置示例](examples/example-attribution.yaml)
- [优先级计算示例](examples/example-priority.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, JSON, YAML, and structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language outputs may include tables, formulas, sample SQL, attribution settings, priority scores, acceptance criteria, and project coordination documents.]

## Skill Version(s):

1.0.0 (source: server release metadata and Hermes metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
