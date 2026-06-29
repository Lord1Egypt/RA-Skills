## Description: <br>
Reads public A-share stock data with akshare, computes fixed finance indicators, and drafts neutral retrospective finance reports with built-in compliance guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiyonghkw](https://clawhub.ai/user/huiyonghkw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and finance writers use this skill to turn an A-share stock code into a neutral public-data recap with computed indicators, draft article or image-copy outputs, and finance-compliance guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock recaps may be mistaken for investment advice or contain finance content that needs review before publication. <br>
Mitigation: Review generated finance content before publishing and keep the no-recommendation, no-prediction, no-buy-or-sell-point, and risk-disclosure guardrails in place. <br>
Risk: The skill may run commands, fetch public financial data, and write local report artifacts when invoked. <br>
Mitigation: Install and run it only when a local stock-data recap helper is intended, and review generated artifacts before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiyonghkw/hekouwang-stock-data-reader-skill) <br>
- [Server-resolved GitHub provenance](https://github.com/huiyonghkw/hekouwang-stock-data-reader-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and report-writing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of local CSV, JSON, draft report, and screenshot artifacts when invoked with the supporting scripts.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
