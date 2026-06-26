## Description: <br>
Identifies high-conviction stock opportunities and tracks JB's retirement portfolio with weekly scans, quarterly reviews, and FIRE signal analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3m2b](https://clawhub.ai/user/j3m2b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal finance and investing users can use this skill to scan a stock watchlist, calculate RSI-based buy or sell signals, and maintain FIRE-oriented portfolio review notes. It is intended for recurring personal analysis and alerting rather than regulated financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles private financial records and portfolio details. <br>
Mitigation: Remove or redact personal financial records before installation, sharing, or reuse. <br>
Risk: The skill can post financial information to Discord without enough scoping or user control. <br>
Mitigation: Verify the Discord destination, move channel targets into private configuration, and require explicit confirmation before posting financial details externally. <br>
Risk: The artifact includes an exposed API key. <br>
Mitigation: Rotate the exposed key and move credentials into private environment variables or another secret store before running the skill. <br>


## Reference(s): <br>
- [Catalyst Edge ClawHub release](https://clawhub.ai/j3m2b/jb-catalyst-edge) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [FIRE model](artifact/FIRE_MODEL.md) <br>
- [Portfolio analysis](artifact/PORTFOLIO_ANALYSIS.md) <br>
- [Cash flow analysis](artifact/CASH_FLOW_ANALYSIS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON scan results, Discord-ready alert text, Python scripts, shell commands, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read personal financial records, fetch market data, write local scan logs, and send formatted alerts to Discord.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
