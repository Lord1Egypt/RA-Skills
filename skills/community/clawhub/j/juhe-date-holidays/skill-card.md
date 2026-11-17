## Description:

Queries Juhe holiday schedule data for a specified date, including holiday or make-up workday status, weekday, lunar calendar details, and almanac notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer user questions about Chinese holiday schedules, make-up workdays, weekdays, lunar dates, and almanac details for a supplied date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Juhe endpoint uses HTTP, which can expose the Juhe API key in transit.

Mitigation: Use the skill only after changing or confirming the endpoint to HTTPS, and rotate any Juhe key previously used through the HTTP endpoint.

Risk: Passing the API key with --key or storing it in scripts/.env can expose credentials through shell history, files, or version control.

Mitigation: Prefer JUHE_DATE_HOLIDAY_KEY from the environment; keep any .env file out of version control and restrict file permissions.

Risk: Holiday queries send the requested date to Juhe.

Mitigation: Use the skill only when sending those date queries to Juhe is acceptable for the intended workflow.

## Reference(s):

- [Juhe Holiday Schedule API documentation](https://www.juhe.cn/docs/api/id/606)
- [Juhe data platform](https://www.juhe.cn)
- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-date-holidays)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_DATE_HOLIDAY_KEY credential; queried dates are sent to Juhe.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
