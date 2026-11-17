## Description:

Retrieves structured public Douyin data for keyword search ranking, author post collection, video comment collection, and real-time hot-list lookup for marketing analysis, account operations, topic research, and public-opinion monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content operators, and analysts use this skill to collect public Douyin search results, author posts, hot-list entries, and comments as structured JSON for follow-on analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Guaikei API token and collection parameters are sent to www.guaikei.com, including token use in URL query strings.

Mitigation: Use a dedicated low-privilege token, avoid shared workspaces, and run the skill only when the user explicitly requests public Douyin data collection.

Risk: Collected Douyin data may be saved locally without opt-out or retention controls.

Mitigation: Review generated logs after each run and delete files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-author-posts)
- [Guaikei API site](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked CLIs write pure JSON to stdout and may save result logs locally.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
