## Description:

Financial Search Engine lets agents run natural-language searches against Eastmoney financial data for news, announcements, research reports, policy updates, and market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial research agents use this skill to retrieve timely financial information about companies, sectors, themes, policies, and market events. It supports event tracking, sentiment monitoring, research report review, announcement analysis, and investment research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Eastmoney EM_API_KEY and sends financial research queries to the configured Eastmoney service.

Mitigation: Use only approved Eastmoney credentials, avoid confidential client or regulated information in queries unless the service is approved for that use, and rotate or revoke the key if exposed.

Risk: Returned financial search results can be saved locally by default.

Mitigation: Use --no-save for sensitive searches and review local output files before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/mx-finance-search)
- [Eastmoney MX Claw](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [Text, Files, Code, Configuration]

**Output Format:** [Plain text financial search results, optional .txt files, and Python dictionary results with raw JSON available for code use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; saves results locally by default unless --no-save is used.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
