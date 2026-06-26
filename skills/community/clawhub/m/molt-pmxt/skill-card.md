## Description: <br>
Grants the agent real-time access to prediction markets (Polymarket, Kalshi, Limitless) for fact-checking, probability analysis, and order execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realfishsam](https://clawhub.ai/user/realfishsam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent search prediction markets, retrieve market-implied probabilities, and submit prediction-market orders when trading credentials are configured and the user has explicitly confirmed the order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses private trading credentials for prediction-market accounts. <br>
Mitigation: For read-only use, do not configure private keys or trading API keys; for trading use low-balance or tightly scoped accounts. <br>
Risk: The skill can submit live money orders without an enforced confirmation gate. <br>
Mitigation: Keep manual confirmation outside the agent and configure exchange-side limits where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realfishsam/molt-pmxt) <br>
- [README](README.md) <br>
- [Agent operating guide](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Structured data, API calls, Guidance] <br>
**Output Format:** [JSON-like tool results and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market IDs, titles, volumes, implied yes/no probabilities, order confirmations, and error messages.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
