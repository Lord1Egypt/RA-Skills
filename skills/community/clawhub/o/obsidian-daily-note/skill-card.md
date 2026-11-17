## Description:

Write structured entries into an Obsidian daily note vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongquanxu1993](https://clawhub.ai/user/hongquanxu1993)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record text, links, ideas, research notes, task summaries, meeting takeaways, and images into a configured Obsidian daily note with consistent timestamped formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and prepend content to local Obsidian daily note files and save a vault path under ~/.workbuddy.

Mitigation: Review the configured vault path before use and install it only where local note-file writes are expected.

Risk: Automatic title fetching for user-supplied URLs can expose private links or internal services.

Mitigation: Avoid sensitive or internal URLs unless the skill is changed to store links as-is by default or ask before fetching titles.

Risk: Trigger behavior is unclear because the evidence describes both broad note-taking triggers and explicit-only activation rules.

Mitigation: Use explicit invocation wording and review trigger rules before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongquanxu1993/skills/obsidian-daily-note)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown note entries with brief confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepends timestamped entries to local daily note files, may create attachment links, and saves vault path configuration for later use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
