## Description:

Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to retrieve Xiaohongshu Creator Marketplace note performance metrics for content efficiency analysis, creator benchmarking, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments, URL query strings, logs, process listings, telemetry, or error reports.

Mitigation: Use a narrowly scoped or disposable token when available, avoid sharing transcripts or full request URLs, and rotate the token if exposure is suspected.

Risk: Requests send the JustOneAPI credential to the declared JustOneAPI endpoint.

Mitigation: Install and run the skill only when that credential flow matches the user's trust and data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-api-solar-kol-data-v3-notes-rate)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_notes_rate&utm_content=project_link)
- [Xiaohongshu Pugongying operations reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when results are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and userId; optional query filters include business, noteType, dateType, and advertiseSwitch.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
