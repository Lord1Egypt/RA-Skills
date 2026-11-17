## Description:

Delegate coding work to Codex, Claude Code, or OpenCode as background workers; not simple edits or read-only code lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate substantial feature work, pull request reviews, large refactors, and issue-to-PR work to background coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task prompts and project content may be sent to the configured external AI provider; the scan did not confirm that this data is approved for that provider.

Mitigation: Confirm the provider is approved for the project data before launching workers, and keep sensitive content out of prompts unless that use is authorized.

Risk: The security analysis was partial because two local references could not be resolved.

Mitigation: Review the skill and referenced materials before use, especially if those references are added or changed.

## Reference(s):

- [Coding Agent on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-coding-agent)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands]

**Output Format:** [Code changes, review findings, and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected coding agent and the task context.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
