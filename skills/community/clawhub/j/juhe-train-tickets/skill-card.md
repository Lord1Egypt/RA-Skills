## Description:

Queries Juhe Data's China train timetable API for trains between departure and arrival stations, including train numbers, departure and arrival times, duration, fares, and remaining seats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up China train schedules for a requested route and date, with optional filters for train type, departure time window, booking availability, and fare details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Juhe API key could be exposed if passed on the command line or committed in a local .env file.

Mitigation: Prefer JUHE_TRAIN_KEY as an environment variable, avoid using --key for routine use, and do not commit scripts/.env.

Risk: Route and date searches are sent to Juhe for lookup.

Mitigation: Install and use the skill only when sending train query details to Juhe is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-train-tickets)
- [Juhe Train Ticket API documentation](https://www.juhe.cn/docs/api/id/817)
- [Juhe Data](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal table output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_TRAIN_KEY; route and date queries are sent to Juhe.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
