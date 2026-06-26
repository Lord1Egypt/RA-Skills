## Description: <br>
Monitor stock/crypto holdings, get price alerts, track portfolio performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhillin8](https://clawhub.ai/user/jhillin8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to track stock, crypto, and ETF holdings through conversational commands, including price checks, target alerts, and portfolio gain/loss summaries. It is informational only and does not connect to brokerage accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may involve sensitive portfolio details in the agent environment. <br>
Mitigation: Share only holdings information needed for tracking, avoid brokerage credentials or account numbers, and remove stored holdings through the host agent when no longer needed. <br>
Risk: Price checks and performance summaries could be mistaken for trading advice or execution-grade market data. <br>
Mitigation: Treat outputs as informational only, verify prices independently before trading, and do not rely on the skill for financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jhillin8/portfolio-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portfolio prices may update every few minutes and are informational only.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
