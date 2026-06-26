## Description: <br>
通过快递单号查询欧美主流物流状态（UPS、FedEx、USPS、DHL、英国皇家邮政、PostNL 等）。当用户发送快递单号或询问包裹状态时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhongkedy-del](https://clawhub.ai/user/zhongkedy-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to identify likely carriers from tracking-number patterns and retrieve shipment status through Track123. It formats current status, latest tracking events, estimated delivery, and carrier tracking links for single or batch package queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Track123 API key and the security evidence flags an unsafe pattern that asks users to put the key directly into the skill file. <br>
Mitigation: Store the Track123 API key in a secure secret store or environment variable, avoid pasting secrets into the skill file, and rotate any key that was already embedded. <br>
Risk: Shipment identifiers are sent to Track123 when querying package status. <br>
Mitigation: Use the skill only when users are comfortable sharing shipment identifiers with Track123 and avoid submitting unnecessary personal information. <br>


## Reference(s): <br>
- [Track123 API](https://www.track123.com/api) <br>
- [Track123 Track Import Endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/import) <br>
- [Track123 Track Query Endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown shipment-status summaries with optional tables and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Track123 API responses summarized as carrier, status, latest events, estimated delivery, and tracking links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
