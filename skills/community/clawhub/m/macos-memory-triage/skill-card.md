## Description:

Guides agents through macOS memory-pressure triage, including reading swap and process stats, identifying AI-tool or plugin process bloat, clearing regenerable caches, and performing user-reviewed reversible remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruthviishere](https://clawhub.ai/user/pruthviishere)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Mac users, and support operators use this skill to diagnose slow, hanging, or freezing Macs and propose safe, reversible cleanup steps for memory pressure and process bloat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose stopping processes, disabling plugin flags, unloading launch agents, or clearing npm/npx cache files.

Mitigation: Require the user to review each target and command before approval, and keep actions scoped to reversible changes.

Risk: Process IDs and process names can become stale between inspection and remediation.

Mitigation: Show the current process details immediately before any kill command and confirm that the target still matches the user's intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pruthviishere/skills/macos-memory-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review before remediation commands that stop processes, edit configuration, unload launch agents, or clear named caches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
