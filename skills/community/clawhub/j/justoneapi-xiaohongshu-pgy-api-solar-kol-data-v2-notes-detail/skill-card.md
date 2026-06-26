## Description: <br>
Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV2/notesDetail/v1 for Xiaohongshu Creator Marketplace (Pugongying) User Published Notes through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve Xiaohongshu Creator Marketplace (Pugongying) published-note data for a KOL user ID. It supports creator monitoring and campaign research by returning note metadata and engagement signals from the JustOneAPI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required JustOneAPI token may be exposed through command arguments or request URLs. <br>
Mitigation: Use a low-privilege token, avoid sharing command history, process listings, URLs, logs, screenshots, and error output, and rotate the token if exposure is possible. <br>
Risk: The release is published by a third-party owner with a low trust tier. <br>
Mitigation: Install only after deciding that JustOneAPI is an acceptable publisher for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v2-notes-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v2_notes_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and the userId query parameter; optional query filters control ad status, source platform, note type, ordering, and page number.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, created 2026-05-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
