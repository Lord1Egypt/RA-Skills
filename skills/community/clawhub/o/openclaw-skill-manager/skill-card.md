## Description:

Manages OpenClaw skill installation, listing, updates, moves, and custom skill spaces through CLI-guided workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to manage skill spaces, install skills, inspect available skills, update existing skills, and move skills between configured spaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation from arbitrary URLs into active skill folders without integrity checks.

Mitigation: Use trusted skill sources, independently verify downloaded archives and publishers, and review the target directory before confirming an install.

Risk: The skill can guide changes to OpenClaw skill directories and gateway state.

Mitigation: Review proposed updates, moves, configuration edits, backups, and gateway restarts before execution.

## Reference(s):

- [OpenClaw Skill Manager on ClawHub](https://clawhub.ai/liberalchang/skills/openclaw-skill-manager)
- [Publisher profile: liberalchang](https://clawhub.ai/user/liberalchang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation prompts, status reports, troubleshooting guidance, and suggested OpenClaw or ClawHub CLI commands.]

## Skill Version(s):

3.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
