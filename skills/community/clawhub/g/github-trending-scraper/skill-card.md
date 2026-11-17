## Description:

Scrapes GitHub Trending repositories into structured JSON with optional language filters and daily, weekly, or monthly ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yes999zc](https://clawhub.ai/user/yes999zc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect public GitHub Trending repository data for analysis, dashboards, or visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script overwrites the specified output file path.

Mitigation: Have the agent write only to an intended workspace or temporary file path.

Risk: Repeated scraping of GitHub Trending can create avoidable load or trigger site limits.

Mitigation: Use reasonable request frequency and cache or reuse recent output where possible.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [ClawHub skill page](https://clawhub.ai/yes999zc/skills/github-trending-scraper)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON to stdout or a user-specified file, with optional compact JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language, time range, result count, and compact formatting options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
