## Description:

Searches Xiaohongshu (RedNote/XHS) public notes, note details, comments, and creator posts for content research and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, analysts, and agent operators use this skill to search public Xiaohongshu content, inspect note details and comments, and monitor creator posts for topic research, competitor tracking, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API token exposure or quota abuse if a paid or broad-privilege Guaikei token is used carelessly.

Mitigation: Use a dedicated low-privilege token, review the skill before installation, and rotate the token if exposure is suspected.

Risk: Research terms, target URLs, and fetched public content may be saved locally in generated logs.

Mitigation: Avoid sensitive research terms or private tracking URLs, and periodically delete or protect the logs directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-trend-pulse)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Analysis, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes fetched results to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
