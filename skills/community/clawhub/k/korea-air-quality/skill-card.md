## Description:

대한민국 대기질(미세먼지, 초미세먼지, 오존, 통합대기) 조회·브리핑·알림을 위한 OpenClaw 스킬.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to answer Korean air-quality questions, compare regions, save default locations, generate concise briefings, and create local alert or cron-plan workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store API keys and precise user locations in local plaintext data files.

Mitigation: Use environment variables for AirKorea credentials where possible, restrict access to the data directory, and avoid committing or syncing local data files.

Risk: The skill can generate executable OpenClaw cron-agent instructions from user or region values.

Mitigation: Inspect cron-plan JSON before registering scheduled jobs, especially when user or region values came from chat input.

Risk: JSON output may expose configured secrets or sensitive local state during setup and inspection flows.

Mitigation: Avoid JSON output while configuring secrets and review generated or displayed configuration before sharing logs.

## Reference(s):

- [Korea Air Quality Skill Plan](references/api-and-product-plan.md)
- [Alert and Morning Briefing](references/alert-and-briefing.md)
- [Domestic API Notes](references/domestic-api-notes.md)
- [Integration Roadmap Status](references/integration-roadmap.md)
- [Location Resolution Strategy](references/location-resolution.md)
- [Open-Meteo Geocoding API endpoint](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Air Quality API endpoint](https://air-quality-api.open-meteo.com/v1/air-quality)
- [Open-Meteo Weather Forecast API endpoint](https://api.open-meteo.com/v1/forecast)
- [AirKorea realtime air-quality API endpoint](https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Korean Markdown or plain text summaries, optional JSON from CLI commands, and cron-plan configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local data files for user preferences, provider configuration, alert rules, alert state, and station cache.]

## Skill Version(s):

2026.4.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
