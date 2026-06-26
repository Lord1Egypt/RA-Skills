## Description: <br>
Autonomous prediction market agent - analyzes markets, researches news, and identifies trading opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andretuta](https://clawhub.ai/user/Andretuta) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search Polymarket prediction markets, research related news, compare market odds with estimated probabilities, and receive trading recommendations or execute approved trades through the poly CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a raw wallet private key for Polymarket trading. <br>
Mitigation: Use only a dedicated wallet with limited funds and review setup carefully before storing credentials. <br>
Risk: The skill can enable real-money trades without per-trade confirmation when autonomous mode is enabled. <br>
Mitigation: Keep autonomous mode disabled and manually confirm every trade before execution. <br>
Risk: Dependencies are unpinned in requirements.txt and may change over time. <br>
Mitigation: Prefer pinned dependency versions before setup or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Andretuta/polymarket-agent) <br>
- [Clawdis homepage](https://clawdhub.com/polymarket-agent) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with CLI command suggestions and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Polymarket APIs and trading commands when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
