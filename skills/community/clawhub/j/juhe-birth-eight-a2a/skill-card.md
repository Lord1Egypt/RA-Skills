## Description: <br>
基于聚合数据稳定生辰八字 API 能力，根据阳历日期和出生时辰查询生辰八字、五行属性、干支纪年、农历日期、星座等信息，并通过支付宝 A2M 402 付费流程获取结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to submit a confirmed Gregorian birth date and birth hour for a paid entertainment-oriented birth-chart lookup, including lunar calendar, heavenly-stem/earthly-branch, zodiac, constellation, eight-character, and five-elements information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends birth date and hour to Juhe's API for a paid lookup. <br>
Mitigation: Proceed only after explicit user confirmation and share only the four required date and hour fields. <br>
Risk: The skill relies on an Alipay payment flow before returning paid results. <br>
Mitigation: Review the payment prompt, order details, and user consent before completing payment. <br>
Risk: Birth-chart and five-elements results may be mistaken for decision-grade advice. <br>
Mitigation: Treat results as entertainment content and avoid using them for medical, financial, legal, career, or relationship decisions. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/juhemcp/skills/juhe-birth-eight-a2a) <br>
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query.php) <br>
- [生辰宝典输出格式](OUT_FORMAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, API Calls, shell commands, guidance] <br>
**Output Format:** [Markdown tables and explanatory text after a paid API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only returned Juhe API fields for the final birth-chart report and includes an entertainment-only disclaimer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
