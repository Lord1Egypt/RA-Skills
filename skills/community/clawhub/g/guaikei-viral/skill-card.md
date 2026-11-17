## Description:

guaikei-viral helps agents search Xiaohongshu public notes, retrieve note details and comments, monitor creator posts, and return structured data for content, competitor, trend, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, analysts, and agents use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for topic research, competitor monitoring, KOL screening, and reporting. The skill requires a Guaikei API token and should be used only for public data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and access-bearing Xiaohongshu URLs may be exposed in query strings or saved local logs.

Mitigation: Use a dedicated low-value Guaikei token, rotate it if exposed, avoid sensitive or private links, and treat the logs directory as sensitive.

Risk: Automatically saved result data may retain public-platform content and full analysis outputs longer than intended.

Mitigation: Review, restrict, redact, or delete generated logs after use, and avoid sharing logs outside the authorized team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-viral)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be saved under logs/ by the skill scripts and may include Xiaohongshu URLs, interaction metrics, comments, and API-derived records.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
