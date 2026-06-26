## Description: <br>
自动抓取韭研公社异动数据，分析市场环境、机会、风险及热门板块，生成结构化简报并推送 QQ 纯文本及 IMA 笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajian11](https://clawhub.ai/user/ajian11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis users use this skill to collect daily market-movement data from 韭研公社 and produce a Chinese market brief covering conditions, opportunities, risks, hot sectors, and leading stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded IMA and QQ credential or destination values may route generated reports to fixed external accounts. <br>
Mitigation: Replace all embedded credential and destination values with user-controlled secrets before installation, and treat the exposed API key as compromised. <br>
Risk: Scheduled or automatic delivery can save or send reports externally without a fresh user confirmation. <br>
Mitigation: Disable automatic send or scheduled behavior until the skill requires explicit confirmation for each external save or message. <br>
Risk: Generated market briefs may be mistaken for investment advice. <br>
Mitigation: Keep the disclaimer in generated output and require users to independently verify market data and decisions. <br>


## Reference(s): <br>
- [韭研公社异动页面](https://www.jiuyangongshe.com/action) <br>
- [ClawHub skill page](https://clawhub.ai/ajian11/jiuyan-yidong-market) <br>
- [Market brief template](artifact/templates/market-brief-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report for IMA notes and plain-text QQ message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language market brief with market environment, opportunities, risk prompts, hot sectors, leading stocks, summary, and disclaimer.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
