## Description:

提及混沌课程、课程学习、方法论、思维模型、课程检索、课程文稿提炼时使用；提炼价值点、激发创意、总结卖点、产品和服务定价、挖掘创业机会时使用；问及泛商业决策类问题时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundun-online](https://clawhub.ai/user/hundun-online)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external users use this skill to work with Hundun course search, learning paths, transcript-based course summaries, and business innovation tools for value propositions, ideation, differentiation, pricing, and market-entry analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hundun-related requests, business context, and user prompts may be shared with the Hundun/AIA service.

Mitigation: Avoid confidential strategy, regulated personal data, and secrets in prompts used with this skill.

Risk: The skill handles an hd_sk_ API key and supports a configurable API base URL.

Mitigation: Keep the API base URL on the official Hundun HTTPS endpoint and rotate or replace credentials if validity is uncertain.

Risk: The patch write workflow can persist remote instruction material.

Mitigation: Review downloaded content before using any patch write workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hundun-online/skills/hundun)
- [Hundun API Key Page](https://tools.hundun.cn/h5Bin/aia/#/keys)
- [Hundun API Base Endpoint](https://hddrapi.hundun.cn)
- [Authentication and Troubleshooting](artifact/references/auth-and-troubleshooting.md)
- [Course Learning Workflow](artifact/references/course-workflow.md)
- [Innovation Tools Shared Playbook](artifact/references/innovation-tools/_shared-playbook.md)
- [First Principles Reference](artifact/references/foundations/第一性原理.md)
- [Second Curve Innovation Reference](artifact/references/foundations/第二曲线创新.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional inline shell commands and structured course or innovation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require HUNDUN_API_KEY and may call Hundun/AIA APIs; raw course transcripts should not be persisted.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
