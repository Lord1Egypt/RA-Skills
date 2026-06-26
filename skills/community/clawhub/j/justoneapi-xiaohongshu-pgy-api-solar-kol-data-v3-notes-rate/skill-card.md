## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query Xiaohongshu Creator Marketplace note performance metrics for a specified KOL user ID. It supports content efficiency analysis, creator benchmarking, and campaign planning through JustOneAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a JustOneAPI token and queried Xiaohongshu user IDs, which can be sensitive if exposed through command history, process listings, logs, screenshots, or shared machines. <br>
Mitigation: Use tokens you trust with JustOneAPI, prefer scoped or short-lived tokens where available, avoid shared machines, and redact tokens and user IDs before sharing output. <br>
Risk: Backend error output may include API payloads or request context from the JustOneAPI endpoint. <br>
Mitigation: Review error output before reuse or sharing, and remove sensitive token, user ID, creator, or campaign data. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v3-notes-rate) <br>
- [Endpoint operations reference](generated/operations.md) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_notes_rate&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and userId; optional query filters include business, noteType, dateType, and advertiseSwitch.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
