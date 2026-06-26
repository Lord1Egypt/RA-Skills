## Description: <br>
PolyFly gives AI agents API guidance for Hedera prediction markets, including browsing markets, placing HBAR/USDC predictions, creating markets, and checking portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to discover PolyFly prediction markets, submit predictions or market-creation requests, and review portfolio or payout status through documented APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward real HBAR/USDC betting, market creation, and claim actions. <br>
Mitigation: Require explicit user confirmation before each financial action, enforce strict spend limits, restrict eligible markets, and keep API keys or JWTs out of prompts, logs, and transcripts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/imaflytok/polyfly) <br>
- [PolyFly frontend](https://polyfly.buzz) <br>
- [PolyFly API](https://polyfly.buzz/api) <br>
- [ClawSwarm predictions API](https://onlyflies.buzz/clawswarm/api/v1/predictions) <br>
- [OnlyFlies token data API](https://onlyflies.buzz/api/v1/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline HTTP examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide real HBAR or USDC account actions that require user confirmation, spend limits, and credential protection.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
