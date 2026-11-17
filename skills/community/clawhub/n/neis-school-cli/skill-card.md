## Description:

Query Korean school information, meals, and timetables from the official NEIS OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techkwon](https://clawhub.ai/user/techkwon)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and users who need Korean school data use this skill to look up school codes, meal menus, and class timetables from NEIS, with JSON output available for downstream agent or tool consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: School lookup details are sent to the official NEIS service when the CLI queries school, meal, or timetable data.

Mitigation: Use the skill only for intended NEIS lookups and avoid entering unrelated sensitive data.

Risk: If NEIS_API_KEY is used and the fallback curl path runs, the key could be visible through local process-argument logging or inspection.

Mitigation: Prefer environments where Python networking succeeds, set NEIS_API_KEY only when needed, and run on trusted local or managed systems.

## Reference(s):

- [NEIS API Notes](references/neis-api.md)
- [Official NEIS OpenAPI Portal](https://open.neis.go.kr/portal/mainPage.do)
- [NEIS OpenAPI Hub](https://open.neis.go.kr/hub)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands; CLI responses are plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional NEIS_API_KEY and queries official NEIS OpenAPI endpoints.]

## Skill Version(s):

0.2.1 (source: server release metadata, scripts/neis_cli.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
