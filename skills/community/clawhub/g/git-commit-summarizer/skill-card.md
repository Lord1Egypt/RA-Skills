## Description:

Generates structured summaries of recent Git commit activity for changelog drafting, standup notes, and repository change review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to summarize recent Git history for changelog drafts, standup updates, release notes, or quick review of repository activity across a time range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON output and terminal text may not fully escape commit metadata when used in automated pipelines or on untrusted repositories.

Mitigation: Review or sanitize summarizer output before pipeline ingestion, and prefer trusted repositories until JSON escaping and terminal-control sanitization are improved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/git-commit-summarizer)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown-style text summaries or JSON commit summaries, with shell-command guidance for running the summarizer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports filtering by date range, author, output format, and repository path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
