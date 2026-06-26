## Description: <br>
Generates daily A-share market momentum reports with market stance, candidate watchlists, position sizing, and risk controls for small-capital trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ycyjy](https://clawhub.ai/user/ycyjy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to produce informational A-share pre-market reports from configured market data sources, including market stance, scored watchlists, and suggested position parameters. It is intended as analysis support and not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims automatic report pushing and includes optional email, webhook, JoinQuant, iFinD, and Tushare credential fields. <br>
Mitigation: Review configuration before installing, leave optional credentials blank unless their use is documented, and confirm whether any scheduled job or push destination is enabled. <br>
Risk: The skill presents win-rate estimates and trading position suggestions that could be mistaken for guaranteed outcomes or investment advice. <br>
Mitigation: Use the reports only as informational analysis, independently verify market data and assumptions, and avoid relying on stated win rates for trading decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ycyjy/marcus-a-stock) <br>
- [Tushare Pro registration](https://tushare.pro/register) <br>
- [JoinQuant](https://www.joinquant.com/) <br>
- [iFinD](https://www.51ifind.com/) <br>
- [ServerChan](http://sc.ftqq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with console status output and optional saved Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report content includes financial-market observations, scored stock candidates, position sizing, and risk reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
