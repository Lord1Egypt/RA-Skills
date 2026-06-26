## Description: <br>
Helps stock traders analyze market data, calculate technical indicators, manage positions, and generate strategy execution reminders for A-share, Hong Kong, and U.S. stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaxHou-infinity](https://clawhub.ai/user/MaxHou-infinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to support stock analysis workflows, including technical indicator calculation, position tracking, staged take-profit and stop-loss planning, and trade execution review. It is a decision-support helper and should not be treated as professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store position, trade history, and strategy notes in local memory files. <br>
Mitigation: Use non-sensitive records, review where files are written before use, and avoid entering brokerage credentials or account identifiers. <br>
Risk: Generated buy, sell, and stop-loss suggestions can be incorrect or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as decision support only and require independent review before making trades. <br>
Risk: External research queries and unpinned Python dependencies can expose data or change behavior over time. <br>
Mitigation: Review query content before sending it to external tools and pin dependency versions in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaxHou-infinity/human-stock-helper) <br>
- [Publisher profile](https://clawhub.ai/user/MaxHou-infinity) <br>
- [Declared skill homepage](https://github.com/openclaw/skills/human-stock-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional JSON-backed local records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files for positions, trades, strategies, and execution analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
