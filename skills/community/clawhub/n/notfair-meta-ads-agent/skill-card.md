## Description: <br>
NotFair Meta Ads agent for OpenClaw. Diagnose live Meta Ads accounts across Facebook and Instagram, audit spend and delivery, inspect campaigns/ad sets/ads/creatives, draft budget/status/creative fixes, and propose approval-gated changes through NotFair's hosted MCP server: https://notfair.co/meta-ads-mcp <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongchen92](https://clawhub.ai/user/tongchen92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and advertising operators use this skill to audit, diagnose, and optimize live Meta Ads accounts across Facebook and Instagram through NotFair. It supports read-only analysis and proposes user-approved changes for budgets, status, creatives, campaigns, ad sets, and ads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved Meta Ads write actions can affect account spend, delivery, targeting, creative content, or public ad behavior. <br>
Mitigation: Review proposed changes carefully and require explicit approval before executing any budget, delivery, targeting, creative, or creation action. <br>
Risk: The skill accesses live Meta Ads data and account controls through NotFair. <br>
Mitigation: Install only when the user trusts NotFair with the connected Meta Ads data and account permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tongchen92/notfair-meta-ads-agent) <br>
- [NotFair Meta Ads MCP](https://notfair.co/meta-ads-mcp) <br>
- [NotFair Meta Ads Setup](https://notfair.co/connect/meta-ads) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with shell commands, JavaScript examples, audit findings, and proposed actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions are approval-gated and should be followed by read-tool verification.] <br>

## Skill Version(s): <br>
2026.5.23 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
