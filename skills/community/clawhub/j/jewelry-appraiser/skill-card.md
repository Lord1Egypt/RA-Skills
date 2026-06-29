## Description: <br>
AI珠宝鉴定与选购全领域助手，覆盖钻石4C、彩宝、翡翠、珍珠、彩钻、贵金属、证书解读、投资收藏和婚戒定制，面向自然语言问题或珠宝图片/证书提供鉴定分析、价格评估、真伪辨别、投资建议和交互式HTML可视化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External consumers, collectors, jewelry enthusiasts, and agents use this skill to research jewelry quality, interpret certificates, compare purchase options, estimate market ranges, and generate appraisal-style HTML reports. Its outputs are reference guidance and should be checked against authoritative labs or professionals before purchase decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Jewelry prices, investment commentary, and market comparisons can be outdated or unsuitable for a specific transaction. <br>
Mitigation: Treat market prices and investment suggestions as references, use current authoritative market data, and verify with qualified professionals before buying or investing. <br>
Risk: Uploaded certificates or jewelry documents may contain personal, certificate, or transaction details. <br>
Mitigation: Avoid uploading personal or transaction details unless needed, and redact sensitive information before analysis. <br>
Risk: Optional web lookup may expose search terms to the agent's search tools. <br>
Mitigation: Use web lookup only when current market data is needed and avoid including private details in search queries. <br>
Risk: AI appraisal-style conclusions can be mistaken for authoritative authentication. <br>
Mitigation: Present outputs as reference analysis and direct users to verify physical items and certificates with authoritative labs or professional appraisers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bettermen/jewelry-appraiser) <br>
- [GIA Report Check](https://www.gia.edu/report-check) <br>
- [珠宝鉴定证书解读指南](references/certificates.md) <br>
- [彩钻 (Fancy Color Diamond) 鉴定与选购指南](references/colored-diamonds.md) <br>
- [彩色宝石鉴定与选购指南](references/colored-gems.md) <br>
- [钻石 4C 标准与选购指南](references/diamond-4c.md) <br>
- [珠宝投资收藏指南](references/investment-guide.md) <br>
- [翡翠鉴定与选购指南](references/jadeite.md) <br>
- [珍珠鉴定与选购指南](references/pearls.md) <br>
- [贵金属鉴定与选购指南](references/precious-metals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with optional generated HTML report files and report metadata JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web lookup for current prices and market data; generated HTML reports contain placeholders that the agent fills from the skill knowledge base and user query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
