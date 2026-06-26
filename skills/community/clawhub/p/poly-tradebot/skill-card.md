## Description: <br>
Automated news analysis pipeline that fetches CNBC world news, classifies articles by topic (geopolitics vs macroeconomics), and invokes specialized skills (geopolitics-expert or the-fed-agent) to produce structured trading analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafimchmd](https://clawhub.ai/user/rafimchmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn recent CNBC world news into topic-classified geopolitical or macroeconomic analysis, then compare the analysis with related Polymarket markets. It is intended as a research aid for structured market review, not as financial advice or an instruction to trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-style YES/NO recommendations may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational research only and independently verify market odds, volume, dates, resolution rules, and underlying news before acting. <br>
Risk: Saved memory analysis files may cause stale market or news assessments to influence later runs. <br>
Mitigation: Clear old memory files before rerunning the workflow when stale analyses should not be reused. <br>


## Reference(s): <br>
- [Poly Tradebot ClawHub release](https://clawhub.ai/rafimchmd/poly-tradebot) <br>
- [classification_rules.md](references/classification_rules.md) <br>
- [output_templates.md](references/output_templates.md) <br>
- [CNBC World News](https://www.cnbc.com/world/?region=world) <br>
- [Polymarket example market: Fed rate cuts in 2026](https://polymarket.com/event/how-many-fed-rate-cuts-in-2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown table and Markdown analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a unified trading table and may save per-article analysis files under memory/.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
