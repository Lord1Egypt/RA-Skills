## Description:

通用结构化决策模块，接收上游分析 agent 输出的多维 findings payload，应用业务上下文（风险偏好、权重、硬约束），通过 structured-decision-block 引擎合成标准化决策块，包含明确判决、维度得分表、反证条件和优先级动作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn upstream multi-dimensional analysis into an auditable decision block with a verdict, weighted dimension scores, counter-evidence, and prioritized actions. It is suited for workflows where a thick analysis needs to be converted into a concise business decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent monitoring tasks.

Mitigation: Require explicit user confirmation before creating or enabling any scheduled monitoring task.

Risk: The skill may handle account-scoped LinkFox API credentials.

Mitigation: Use scoped, rotatable API keys and avoid setting LinkFox gateway environment variables to untrusted endpoints.

Risk: The skill can upload files or media references to LinkFox services.

Mitigation: Avoid uploading sensitive local files and confirm that any uploaded file is intended for public or service-side use.

Risk: The skill references order creation or payment-related actions.

Mitigation: Require explicit user confirmation before any order creation or payment action.

## Reference(s):

- [Structured Decision Block Input Schema](skills/structured-decision-block/references/structured-decision-block-input-schema.json)
- [Structured Decision Block Output Example](skills/structured-decision-block/references/structured-decision-block-output-example.md)
- [Structured Decision Block Example Payload](skills/structured-decision-block/references/structured-decision-block-example-payload.json)
- [Analysis Report Component Library](skills/linkfox-report-generator/references/analysis-layouts.md)
- [LinkFox Scheduled Task API Reference](skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown decision block plus structured JSON, with optional HTML report file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision output includes a verdict, overall score, confidence, dimension table, veto checks, top evidence, counter-evidence, prioritized actions, and data limitations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
