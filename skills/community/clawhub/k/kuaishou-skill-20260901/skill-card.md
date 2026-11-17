## Description:

Searches Kuaishou public videos, creator posts, and video comments, then returns structured JSON for topic research, competitor monitoring, KOL discovery, comment analysis, and trend insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content teams, marketers, MCNs, and analysts use this skill to collect public Kuaishou data for structured research and downstream reporting. It is suited to keyword video search, creator post tracking, comment insight, competitor monitoring, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou keywords, profile links, video links, and an API token to the third-party guaikei.com service.

Mitigation: Confirm the data-sharing and authorization terms for guaikei.com before use, and avoid sending confidential or sensitive inputs.

Risk: The inspected artifact contains only skill instructions; the referenced CLI scripts are not bundled in the release evidence.

Mitigation: Verify the referenced scripts and runtime environment before installing or executing the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/kuaishou-skill-20260901)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command suggestions and structured JSON results from the referenced CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and routes requests to Kuaishou keyword search, creator post, or comment collection workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
