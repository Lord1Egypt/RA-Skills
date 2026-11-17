## Description:

Automates a brand marketing workflow from brand inputs through content drafting, public competitor-signal analysis, performance scoring, and iteration planning for channels such as Xiaohongshu, Weibo, and Douyin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, operators, and developers use this skill to turn structured brand inputs into briefs, channel-specific draft content, public competitor-signal summaries, scoring reports, and iteration plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw configuration and may use configured credentials for LLM and search-provider access.

Mitigation: Run it with a least-privilege OpenClaw configuration and review configured providers, API keys, and environment variables before execution.

Risk: Brand context and prompts may be sent to configured LLM providers.

Mitigation: Avoid submitting confidential brand data unless the selected provider and account terms are approved for that data.

Risk: Competitor analysis may fetch public pages through Jina or Brave and can produce incomplete or stale competitive intelligence.

Mitigation: Use the results as draft research, review source coverage, and verify claims before using them in market decisions.

Risk: The artifact includes a local Telegram or Feishu gateway sender that is under-disclosed in the public description.

Mitigation: Review messaging configuration and disable or remove gateway access unless outbound notifications are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/halfmoon82-brand-marketing-workflow)
- [Skill documentation](artifact/SKILL.md)
- [Optimization audit report](artifact/BMW_OPTIMIZATION_AUDIT_REPORT.md)
- [Integration test result](artifact/evidence/integration_test_result.txt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON workflow results with drafted markdown or text marketing assets and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads brand input JSON; may use configured LLM providers and public competitor data sources; publishing, payment, login, and captcha steps require human confirmation.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
