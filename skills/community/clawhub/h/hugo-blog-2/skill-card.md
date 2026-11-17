## Description:

This skill helps agents publish Markdown content to a Hugo blog by generating Hugo front matter, adding summary markers, mapping tags and categories, and preparing git-based publication steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and personal bloggers use this skill to turn Markdown drafts into Hugo-compatible posts and manage the supporting publication workflow for a trusted blog repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify and push changes to a Hugo blog repository.

Mitigation: Restrict use to a specific trusted blog path and require confirmation before file writes, git commits, or git pushes.

Risk: The skill may read local memory files or git configuration while detecting blog settings.

Mitigation: Review allowed file access before use and avoid automatic reads of memory files or git configuration unless their contents are approved.

Risk: Broad activation language can make the skill appear relevant outside the intended Hugo publishing workflow.

Mitigation: Use it only for Hugo blog publishing tasks and confirm the target repository before executing commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/hugo-blog-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML front matter examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file writes, Hugo content paths, git commits, and git push commands for a user-approved blog repository.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
