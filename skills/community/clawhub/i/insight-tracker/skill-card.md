## Description:

Track, categorize, search, and analyze insights, patterns, and observations discovered during OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to record session observations as sourced, tagged Markdown insight records, retrieve them by tag or priority, and summarize patterns over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local insight records may contain secrets or sensitive personal details if saved.

Mitigation: Review content before saving, avoid sensitive data unless intended, and remove or archive records when they should no longer be retained.

Risk: Insights can become stale or be contradicted by later evidence.

Mitigation: Use evidence grades and status values to keep claims reviewable, and validate important insights before relying on them for future behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/insight-tracker)
- [Tag taxonomy](references/tag-taxonomy.md)
- [Output examples](references/output-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown insight records, summaries, search results, and concise shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local records persist until manually removed or archived; scripts may use INSIGHT_DATA_DIR to choose the data directory.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
