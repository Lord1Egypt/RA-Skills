## Description:

ZeeLin Deep Research 深度研究 is an AI-assisted research skill that sends user research questions to ZeeLin's Deep Research service to create deep or expert-mode research analysis and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run structured research tasks through ZeeLin's Deep Research API, choosing deep mode for general synthesis or expert mode for longer market, company, policy, product, investment, or technical reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and generated report data are processed by the external ZeeLin service.

Mitigation: Use only in environments where external processing by ZeeLin is approved, and avoid confidential, regulated, or proprietary research topics unless data-handling terms have been reviewed.

Risk: Automated report delivery can upload report contents to Feishu or send downloaded files through messaging channels.

Mitigation: Confirm the destination channel, recipient, and data-sharing policy before enabling automated delivery or Feishu document creation.

Risk: Background execution and temporary report-file workflows may leave generated research artifacts on shared systems.

Mitigation: Harden scripts before shared or automated use by constraining runtime, using unique temporary paths, limiting permissions, and cleaning up report files after delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/kelcey-zeelin-deep-research)
- [Publisher profile](https://clawhub.ai/user/kelcey2023)
- [ZeeLin Deep Research service](https://desearch.zeelin.cn)
- [ZeeLin registration and API key page](https://desearch.zeelin.cn/skill-activity)
- [ZeeLin conversation API](https://desearch.zeelin.cn/api/conversation/anew)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and research report text returned from API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, node, and a DESEARCH_API_KEY environment variable; can retrieve report content after polling a ZeeLin session.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
