## Description:

NotFair Meta Ads Agent helps OpenClaw users diagnose live Meta Ads accounts across Facebook and Instagram, audit spend and delivery, inspect campaigns, ad sets, ads, and creatives, and propose approval-gated changes through NotFair's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongchen92](https://clawhub.ai/user/tongchen92)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketers, and OpenClaw operators use this skill to audit and manage Meta Ads accounts, identify delivery or spend issues, and prepare approval-gated campaign, budget, status, targeting, or creative changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and connecting the external NotFair plugin can grant access to sensitive Meta Ads account data and write-capable advertising workflows.

Mitigation: Install only if the publisher is trusted, use least-privilege Meta permissions where possible, and review the connected account scope before use.

Risk: Budget, targeting, creation, enablement, bid, or creative changes can affect live ad delivery and spend.

Mitigation: Require explicit user approval before any write action, prefer paused or draft entities when available, and verify the resulting Meta Ads state after approved changes.

Risk: Meta budget values may be returned in minor currency units, which can lead to incorrect spend or budget interpretation.

Mitigation: Convert budget and spend values into the account currency before presenting recommendations or requesting approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tongchen92/skills/notfair-meta-ads-agent)
- [NotFair Meta Ads MCP](https://notfair.co/meta-ads-mcp)
- [NotFair Meta Ads setup](https://notfair.co/connect/meta-ads)
- [Hosted Meta Ads MCP endpoint](https://notfair.co/api/mcp/meta_ads)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include approval-gated Meta Ads write proposals; read-only diagnostics can include account, campaign, ad set, ad, creative, and insight summaries.]

## Skill Version(s):

2026.5.23 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
