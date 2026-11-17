## Description:

输入产品和竞品列表，生成结构化竞品分析报告，包括行业概览、竞品逐一分析、对比矩阵、战略建议和风险预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyjaixiao](https://clawhub.ai/user/hyjaixiao)

### License/Terms of Use:

MIT-0

## Use Case:

Entrepreneurs, product managers, investors, strategy teams, freelancers, and student founders use this skill to draft competitor-analysis reports for product planning, fundraising preparation, due diligence, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business inputs and the API key can be sent to the configured remote LLM endpoint.

Mitigation: Use only trusted endpoints, avoid confidential product strategy unless remote processing is acceptable, and review OPENAI_BASE before running.

Risk: The documented CA_FREE_MODE setting does not prevent API calls when OPENAI_API_KEY is set in this version.

Mitigation: Unset OPENAI_API_KEY or use quick mode when API calls must be avoided, and verify generated reports before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyjaixiao/skills/hyjaixiao-competitor-analysis)
- [Publisher profile](https://clawhub.ai/user/hyjaixiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report files and terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in quick template mode or call a configured OpenAI-compatible chat completions endpoint when OPENAI_API_KEY is set.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
