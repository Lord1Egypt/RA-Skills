## Description:

NotFair Google Ads agent for OpenClaw. Diagnose live Google Ads accounts, audit wasted spend, review search terms, draft negative keywords, inspect policy errors, and propose approval-gated campaign changes through NotFair's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongchen92](https://clawhub.ai/user/tongchen92)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, PPC managers, and developers use this skill to audit and optimize connected Google Ads accounts through NotFair. It supports read-only diagnosis, search-term and wasted-spend review, policy-error inspection, and approval-gated campaign changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to Google Ads through a third-party plugin and hosted MCP service that may access sensitive advertising account data.

Mitigation: Install only from trusted NotFair distribution channels, authenticate only intended accounts, and review account scopes before running analysis.

Risk: Campaign, budget, bid, keyword, and ad changes can affect external spend and account performance.

Mitigation: Prefer read-only analysis first, present proposed actions before writes, require explicit user approval, and use paused or draft changes when supported.

Risk: Incorrect or destructive changes could remove entities or alter campaign behavior unexpectedly.

Mitigation: Do not delete entities unless the user explicitly requests the destructive action and confirms scope; verify Google Ads state after any approved write.

## Reference(s):

- [NotFair homepage](https://notfair.co)
- [ClawHub skill page](https://clawhub.ai/tongchen92/skills/notfair-google-ads-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/tongchen92)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, JavaScript snippets, and JSON tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose approval-gated Google Ads write actions; read-only analysis is preferred until account scopes and approval flow are clear.]

## Skill Version(s):

2026.5.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
