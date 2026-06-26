## Description: <br>
Deploy and control AI agents on Hatcher, a managed hosting platform for OpenClaw, Hermes, ElizaOS, and Milady agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hatcherlabs](https://clawhub.ai/user/hatcherlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to register for Hatcher, create hosted AI agents, manage lifecycle actions, configure platform integrations, and handle tier or addon purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through workflows that use HATCHER_KEY, JWTs, platform tokens, wallet credentials, and other sensitive secrets. <br>
Mitigation: Use scoped test accounts first, store secrets in a secret manager, avoid exposing tokens in shared terminals or logs, and rotate any credential that may have been disclosed. <br>
Risk: The skill includes payment, wallet-signing, subscription, addon, and credit workflows that can spend funds or alter account billing state. <br>
Mitigation: Require explicit human confirmation before purchases, tier changes, wallet signing, or hosted checkout handoff, and verify target tier, billing period, amount, and recipient before execution. <br>
Risk: The skill can create, start, stop, restart, delete, and reconfigure hosted agents and connected social integrations. <br>
Mitigation: Confirm destructive or public-facing actions with the user, prefer stop over delete when state should be preserved, and test integrations in low-risk channels before enabling production traffic. <br>
Risk: The security scan summary says the documentation does not provide enough explicit confirmation and secret-handling guardrails for its broad credential, payment, integration, and hosted-agent workflows. <br>
Mitigation: Treat generated commands as proposals for human review, use low-scope tokens during initial setup, and require approval before public posts, DMs, plugin installs, deletes, or account-changing operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hatcherlabs/hatcher-skill) <br>
- [Hatcher homepage](https://hatcher.host) <br>
- [Hatcher OpenAPI specification](https://api.hatcher.host/openapi.json) <br>
- [Hatcher skill entry point](https://hatcher.host/skill.md) <br>
- [Authentication guide](https://hatcher.host/skill/auth.md) <br>
- [Agent management guide](https://hatcher.host/skill/agents.md) <br>
- [Pricing and payments guide](https://hatcher.host/skill/pricing.md) <br>
- [Integrations guide](https://hatcher.host/skill/integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JSON request and response examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls that create accounts, manage hosted agents, install skills or plugins, configure integrations, and initiate payment or wallet flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
