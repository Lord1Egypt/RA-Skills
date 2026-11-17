## Description:

深度测评各模型在 OpenClaw 上的实际表现，支持中文理解/代码/推理/工具调用多维度评估。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and model evaluators use this skill to benchmark model behavior in OpenClaw across Chinese understanding, coding, tool-use explanation, reasoning, and response speed, then record results in a standardized report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuring additional model providers can expose API keys if credentials are stored in shared files.

Mitigation: Keep provider API keys out of shared repositories and verify how OpenClaw models.json stores or references secrets before sharing benchmark configurations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leosheep821-debug/skills/model-benchmark)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown benchmark prompts, scoring rubrics, and report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider setup guidance for OpenClaw models.json and a fixed scoring structure.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
