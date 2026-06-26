## Description: <br>
使用积智数据参考价格查询 API，通过配件编码列表查询汽车配件参考价格信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, parts specialists, and agent developers use this skill to query reference prices for automotive part-code lists through the disclosed 积智数据 pricing API and summarize returned price, quality, and part-code fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Part codes and pricing queries are sent to the disclosed 积智数据/qipeidao pricing service. <br>
Mitigation: Use the skill only when that provider is trusted and the queried part codes are approved to be shared with the service. <br>
Risk: The skill requires a JZ_API_KEY credential for API access. <br>
Mitigation: Use a dedicated API key where possible and avoid embedding the key in prompts, logs, or shared command history. <br>
Risk: Returned reference prices may be incomplete, stale, or unsuitable for final commercial decisions without review. <br>
Mitigation: Treat results as reference pricing and review them against business requirements before quoting, purchasing, or customer-facing use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/price4r) <br>
- [积智数据 reference price API endpoint](https://erp.qipeidao.com/jzOpenClaw/getPriceRefer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JZ_API_KEY; sends part-code lists and optional quality filters to the disclosed pricing API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
