## Description: <br>
禾连健康体检预约智能助手通过多轮对话引导用户完成体检医院和院区选择、套餐预订、登录校验、下单和支付流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwang412](https://clawhub.ai/user/xuwang412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to book health-check appointments through conversational channels such as OpenClaw, Qoder, WeChat, DingTalk, and Feishu. It guides hospital selection, package review, patient login, order creation, and payment handoff for Helian Health checkup services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real health-booking and payment flows and stores patient and bank-card data in local hidden files. <br>
Mitigation: Install only when the publisher is trusted; require explicit user consent, data minimization, masking for displayed saved records, and clear deletion controls before use. <br>
Risk: Payment credentials, SMS codes, and service responses may be exposed through console logging. <br>
Mitigation: Remove or redact logs for payment credentials, SMS codes, tokens, card data, and patient identity data before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuwang412/helian-health-assistant) <br>
- [Helian Health web client](https://healthcheck-web-client.helianhealth.com) <br>
- [Helian Health management service](https://management.helianhealth.com) <br>
- [LianLian Pay MCP service](https://mcp.lianlianpay.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API calls, Files, Guidance] <br>
**Output Format:** [Conversational Chinese guidance with Markdown tables, Python call snippets, API responses, payment links, and QR-code image files when payment is initiated.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles health-booking and payment workflows and may create local hidden records for patient, bank-card, and QR-code data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
