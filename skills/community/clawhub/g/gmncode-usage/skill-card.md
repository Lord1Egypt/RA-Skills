## Description:

GMNCODE Usage helps agents query GMNCODE/gmncode.cn dashboard usage over HTTP, including account quota, daily trends, and per-model token and cost data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and GMNCODE users use this skill to have an agent retrieve account daily quota, dashboard summaries, usage trends, and per-model token and cost reports without manually opening the web dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires GMNCODE login credentials.

Mitigation: Prefer environment variables over a saved password file, avoid shared machines, and restrict any credential file to the current user.

Risk: The skill can cache a bearer token locally.

Mitigation: Restrict cache file permissions, clear the token cache when finished, and review the cache behavior before use.

## Reference(s):

- [GMNCODE Usage API Reference](references/api.md)
- [GMNCODE](https://gmncode.cn)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output as compact text tables or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are scoped to the authenticated GMNCODE account and selected date range.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
