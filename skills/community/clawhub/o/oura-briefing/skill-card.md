## Description:

Fetches Oura Ring v2 sleep, readiness, and activity data and delivers a concise daily health briefing for sleep score, HRV, readiness, recovery, and related Oura metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silas-agent573](https://clawhub.ai/user/silas-agent573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal health agents use this skill to fetch Oura Ring v2 sleep, readiness, and activity data, then summarize daily recovery, sleep, HRV, and activity signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An Oura API token can be exposed locally when passed on the command line or captured in shell history, process arguments, or logs.

Mitigation: Prefer OURA_API_TOKEN, avoid --token in logged environments, and rotate the token if it was previously passed on the command line.

Risk: The skill retrieves and summarizes sensitive Oura health metrics with limited privacy guidance.

Mitigation: Run it only when the user intends to share Oura data and avoid storing or forwarding briefing output beyond the intended agent session.

## Reference(s):

- [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens)
- [Oura API v2 User Collection Endpoint](https://api.ouraring.com/v2/usercollection)
- [ClawHub Skill Page](https://clawhub.ai/silas-agent573/skills/oura-briefing)
- [ClawHub Publisher Profile](https://clawhub.ai/user/silas-agent573)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text briefing or JSON data, typically summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and an Oura API token; supports date-specific, JSON, and wake-check modes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
