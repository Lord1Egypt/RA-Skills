## Description:

基于八步骤方法，结构化分析产品、公司、技术、市场等对象，从时间轴与生态轴提炼因果机制、挑战偏见，并输出定制化深度报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whisperbot](https://clawhub.ai/user/whisperbot)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要研究产品、公司、技术、市场、概念、人物、政策或趋势的产品、投资、战略和技术分析人员，用于组织证据、展开纵向发展史与横向竞品比较，并形成可追溯的中文长篇研究报告或决策备忘录。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may browse extensively and use multiple sub-agents, which can introduce weak, conflicting, or stale sources into the analysis.

Mitigation: Review source quality, prefer primary evidence, and preserve the skill's fact, interpretation, inference, and unconfirmed labels in final claims.

Risk: The workflow creates report files locally by default and can publish to Feishu when requested.

Mitigation: Review output paths and require explicit authorization before creating any external Feishu document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whisperbot/skills/product-analyze-insight-chrono-prism)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Long-form Chinese research report, optionally delivered as PDF, Markdown, or Feishu document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output creates a local report file and analysis archive; Feishu publishing is optional and should be explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
