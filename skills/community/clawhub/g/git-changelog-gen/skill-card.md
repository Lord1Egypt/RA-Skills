## Description:

Generate changelogs from git commits. Supports markdown, plain text, and JSON output with date ranges and tag-based filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT

## Use Case:

Developers and release engineers use this skill to generate changelogs from trusted git commit history for release notes, summaries, or automation inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated changelogs can include untrusted commit subjects, author names, or dates from repository history.

Mitigation: Use the skill with trusted repositories, or review and sanitize generated changelogs before publishing or feeding JSON output into automation.

Risk: Manual JSON construction and output escaping weaknesses could produce malformed output or preserve unsafe Markdown or terminal control content.

Mitigation: Review JSON output before automation use and replace manual JSON construction with a serializer when maintaining the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/git-changelog-gen)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Markdown, plain text, or JSON changelog output with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports date ranges, tag-based filtering, merge-commit exclusion, and optional grouping by conventional commit type.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
