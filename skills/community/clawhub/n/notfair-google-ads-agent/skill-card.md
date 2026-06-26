## Description: <br>
NotFair Google Ads agent for OpenClaw. Diagnose live Google Ads accounts, audit wasted spend, review search terms, draft negative keywords, inspect policy errors, and propose approval-gated campaign changes through NotFair's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongchen92](https://clawhub.ai/user/tongchen92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, PPC managers, and agents use this skill to inspect connected Google Ads accounts, diagnose wasted spend and policy issues, and prepare approval-gated optimization changes through NotFair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access live Google Ads account data through NotFair's hosted service. <br>
Mitigation: Install it only when NotFair and the openclaw-notfair plugin are trusted, and connect only the intended Google Ads accounts. <br>
Risk: Approved writes can affect campaign budgets, bids, keywords, ads, or account state. <br>
Mitigation: Review the exact account, campaign, budget, bid, keyword, deletion, and mutation scope before approving any write, and verify the Google Ads state after execution. <br>


## Reference(s): <br>
- [NotFair homepage](https://notfair.co) <br>
- [ClawHub skill page](https://clawhub.ai/tongchen92/notfair-google-ads-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, findings, and proposed actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis may run directly; Google Ads writes require explicit user approval and follow-up verification.] <br>

## Skill Version(s): <br>
2026.5.14 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
