## Description:

谋道基于「道法术器」框架，把用户想法转化为前期调研、快速方案、深度规划或迭代诊断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ks1291665853-sketch](https://clawhub.ai/user/ks1291665853-sketch)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to turn goals, business ideas, career plans, learning paths, and execution problems into structured research, planning guidance, tool recommendations, and diagnostic advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planning prompts, profile details, constraints, diagnostic context, and generated research summaries may be sent to an external LLM provider.

Mitigation: Do not include secrets, confidential business details, or sensitive personal data in prompts or context.

Risk: A configurable external endpoint can receive the API key and request content.

Mitigation: Use only a trusted HTTPS endpoint, and avoid setting DEEPSEEK_BASE_URL unless you control and trust it.

Risk: The --output option writes generated reports to disk.

Mitigation: Choose output paths carefully and avoid writing sensitive reports into shared or persistent locations.

## Reference(s):

- [道法术器认知框架](references/framework.md)
- [谋道使用案例](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/ks1291665853-sketch/skills/moudao)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown, JSON, or plain text planning reports generated from LLM responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated reports to a user-specified output file]

## Skill Version(s):

1.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
