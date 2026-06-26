## Description: <br>
Generates HK stock market morning reports for bank trading desks, with Chinese report formatting, source-gathering steps, and WeChat/Feishu delivery guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjlrestlong-ai](https://clawhub.ai/user/cjlrestlong-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bank trading-desk users or their agents use this skill to gather HK market data and news, assemble a Chinese morning report, and prepare it for approved internal channels. <br>

### Deployment Geography for Use: <br>
Global, for Hong Kong market reporting. <br>

## Known Risks and Mitigations: <br>
Risk: Generated market data or news could be incorrect or misleading when search results, source availability, or the partial helper script do not complete the full workflow. <br>
Mitigation: Verify market figures and news against approved sources before relying on or distributing the report. <br>
Risk: The workflow describes internal-labeled reports and WeChat/Feishu delivery without clear recipient controls. <br>
Mitigation: Use only approved delivery channels and configured recipients, and require explicit confirmation before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjlrestlong-ai/hk-stock-morning-report) <br>
- [Stock report format](references/stock_report_format.md) <br>
- [Common report errors](references/errors.md) <br>
- [Tencent Finance quote API](https://qt.gtimg.cn/q={code}) <br>
- [Sina HK stock news](https://finance.sina.com/stock/hkstock/) <br>
- [Gelonhui](https://www.gelonghui.com) <br>
- [Securities Times](https://www.stcn.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report text with source-checking guidance and an optional Python helper script workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports are intended for internal review; the helper script covers only part of the full data collection, report, and delivery workflow.] <br>

## Skill Version(s): <br>
1.4.10 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
