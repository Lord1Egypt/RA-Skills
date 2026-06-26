## Description: <br>
Query Polymarket prediction markets for market prices, event probabilities, betting odds, and related Polymarket data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent fetch public Polymarket market data, including top markets, text-filtered market searches, individual market details by slug, and event groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-supplied search terms and market slugs to the public Polymarket API. <br>
Mitigation: Avoid private, sensitive, or confidential information in search terms and prompts that trigger the skill. <br>
Risk: The skill performs outbound network requests whenever it retrieves markets or events. <br>
Mitigation: Use network allowlisting or declared network permissions if stricter governance is required. <br>
Risk: Prediction market prices can be incomplete, volatile, or unsuitable as sole decision-making evidence. <br>
Mitigation: Treat returned prices as market signals and compare them with other sources before making important decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dannyshmueli/polymarket-api) <br>
- [Publisher profile](https://clawhub.ai/user/dannyshmueli) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Plain text summaries or raw JSON from Polymarket API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access to the public Polymarket Gamma API is used when the skill is invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
