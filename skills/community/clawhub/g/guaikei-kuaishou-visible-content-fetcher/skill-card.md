## Description:

Fetches public Kuaishou videos, creator posts, and video comments through Guaikei and returns structured JSON for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, content operators, marketers, MCN teams, and analysts use this skill to collect public Kuaishou search results, creator posts, and comments for topic research, competitor monitoring, KOL screening, public-comment analysis, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends a third-party Guaikei API token and Kuaishou keywords or URLs to www.guaikei.com.

Mitigation: Install and run it only when sharing those inputs with Guaikei is acceptable; avoid submitting sensitive business research terms or URLs unless authorized.

Risk: Generated logs may retain business research, user comments, or other collected data locally.

Mitigation: Review and delete generated logs when the retained data should not remain on disk, and restrict access to the workspace where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-visible-content-fetcher)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may be written to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
