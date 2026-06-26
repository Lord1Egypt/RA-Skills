## Description: <br>
Query real-time shipping status for mainstream EU/US carriers (UPS, FedEx, USPS, DHL, Royal Mail, PostNL, etc.) by tracking number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhongkedy-del](https://clawhub.ai/user/zhongkedy-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify shipping carriers, query Track123 for tracking updates, and summarize shipment status, tracking history, delivery estimates, and direct tracking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a Track123 API key in chat and save it in SKILL.md. <br>
Mitigation: Store the Track123 API key in a secret manager or environment variable, avoid pasting it into chat, and rotate any key that has already been shared or committed. <br>
Risk: Tracking output depends on Track123 API responses and may be unavailable, delayed, or incomplete. <br>
Mitigation: Review the returned tracking data before acting on it and use direct carrier links for confirmation when status is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhongkedy-del/logistics-tracker-en) <br>
- [Track123 API](https://www.track123.com/api) <br>
- [Track123 Import Endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/import) <br>
- [Track123 Query Endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tracking summaries, tables, status fields, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include up to 10 recent tracking events per shipment and direct carrier tracking URLs when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
