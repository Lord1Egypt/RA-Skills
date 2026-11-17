## Description:

Fetch KBO game schedules and results for a specific date with the kbo-game npm package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5eun](https://clawhub.ai/user/5eun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sports-focused agents use this skill to fetch compact KBO game schedules, statuses, and scores for a requested absolute or relative date, with optional team filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to globally install and execute an unpinned npm package.

Mitigation: Use the skill in a sandbox or pin and review the kbo-game package version before installation.

Risk: The underlying KBO package or upstream site can change, which may break results or produce empty schedules.

Mitigation: Check returned data before presenting it as final and explain empty or failed responses as possible package or schedule issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5eun/skills/kbo-results)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with compact scoreboard summaries and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize raw JSON from kbo-game and filter results by team when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
