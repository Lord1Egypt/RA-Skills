## Description: <br>
使用慧穗云发票查验 API，根据发票代码、号码、日期和金额等信息查询发票详情。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyierle](https://clawhub.ai/user/xiaoyierle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to verify Chinese VAT invoice details through Huisuiyun from invoice number, date, amount, type, and related fields. It helps summarize whether an invoice check succeeded and return key invoice details from the provider response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice details are sent to the external Huisuiyun provider for verification. <br>
Mitigation: Use the skill only when authorized to submit the relevant invoice information to Huisuiyun. <br>
Risk: HSY_AK and HSY_SK are provider credentials used to obtain access tokens. <br>
Mitigation: Keep the credentials private, provide them through environment variables, and avoid exposing them in prompts, logs, or shared command history. <br>
Risk: Changing HSY_API_URL can send credentials and invoice data to a nonstandard endpoint. <br>
Mitigation: Leave HSY_API_URL on the official Huisuiyun endpoint unless the replacement endpoint is fully trusted. <br>
Risk: The storeFlag request option affects whether provider-side storage is acceptable for the submitted invoice data. <br>
Mitigation: Set storeFlag according to the user's data retention and provider-storage requirements before making verification requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyierle/invoice-verify-hsy) <br>
- [Huisuiyun invoice check API documentation](https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/invoice-check) <br>
- [Huisuiyun token documentation](https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96token-%E5%90%8C%E6%AD%A5) <br>
- [Huisuiyun secret key management](https://huisuiyun.com/account/conf/secretkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON provider responses with concise text guidance for setup and result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus HSY_AK and HSY_SK environment variables; HSY_API_URL defaults to the official Huisuiyun endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
