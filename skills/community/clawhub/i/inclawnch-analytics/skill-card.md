## Description: <br>
Provides real-time INCLAWNCH token analytics on Base, including price, volume, liquidity, staking TVL, UBI APY, distribution rates, and platform metrics through a public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stuart5915](https://clawhub.ai/user/stuart5915) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public INCLAWNCH market, staking, and platform analytics for user answers, dashboards, alerts, and ecosystem-health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts inclawbate.com to retrieve public token analytics. <br>
Mitigation: Install and use it only when outbound requests to inclawbate.com are acceptable for the agent environment. <br>
Risk: Market, staking, APY, and token-contract data may be incomplete, stale, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Verify important financial or contract information independently before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stuart5915/inclawnch-analytics) <br>
- [Inclawbate skills homepage](https://inclawbate.com/skills) <br>
- [INCLAWNCH analytics endpoint](https://inclawbate.com/api/inclawbate/analytics) <br>
- [INCLAWNCH analytics skill spec](https://inclawbate.com/api/inclawbate/skill/analytics) <br>
- [INCLAWNCH BaseScan token page](https://basescan.org/token/0xa1F72459dfA10BAD200Ac160eCd78C6b77a747be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct endpoint access; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
