## Description:

Fetch and report Peloton cycling workout statistics, including ride counts, duration, calories, output, power, resistance, cadence, instructor data, and recent ride history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niemesrw](https://clawhub.ai/user/niemesrw)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve a Markdown summary of recent Peloton cycling workouts and performance metrics. It is useful when a user asks for weekly cycling stats, ride history, or Peloton workout data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs Peloton credentials stored locally or supplied through environment variables.

Mitigation: Use the OpenClaw credential manager where possible, restrict access to the credential file, and remove the stored profile if the skill is no longer used.

Risk: The skill contacts Peloton's unofficial API to retrieve workout history and performance metrics.

Mitigation: Install and run it only when this external API access is acceptable for the user's account and data handling expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niemesrw/skills/peloton-stats)
- [Publisher profile](https://clawhub.ai/user/niemesrw)
- [Peloton API endpoint](https://api.onepeloton.com)
- [Peloton OAuth token endpoint](https://auth.onepeloton.com/oauth/token)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with summary metrics and a recent rides table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Peloton credentials from OpenClaw configuration or PELOTON_USERNAME and PELOTON_PASSWORD environment variables.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
