## Description: <br>
Provides omni.fun API guidance and curl examples for agents to browse tokens, request strategy analysis, launch tokens, prepare trades, monitor portfolios, claim rewards, and configure spending controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xzcov](https://clawhub.ai/user/0xzcov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate against omni.fun endpoints for market discovery, token launch and trading workflows, reward tracking, webhook setup, and agent security controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides financial and crypto trading actions, and its memecoin return and bounty language is speculative. <br>
Mitigation: Treat market and reward language as informational, keep OMNIFUN_API_KEY private, configure low per-trade and daily limits with chain and action allowlists, and manually review any unsigned transaction calldata before signing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xzcov/omnifun) <br>
- [omni.fun homepage](https://omni.fun) <br>
- [omni.fun app](https://app.omni.fun) <br>
- [omni.fun OpenAPI specification](https://app.omni.fun/.well-known/openapi.json) <br>
- [Published omni.fun SKILL.md](https://app.omni.fun/.well-known/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples, endpoint tables, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples and OMNIFUN_API_KEY for authenticated endpoints; public market data endpoints do not require credentials.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
