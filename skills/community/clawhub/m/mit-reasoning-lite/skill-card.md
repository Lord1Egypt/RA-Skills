## Description:

Provides a 3-step reasoning scaffold prompting agents to clarify objectives, check constraints, and articulate reasoning before significant decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgapol](https://clawhub.ai/user/kgapol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a lightweight decision checkpoint before high-impact, ambiguous, or hard-to-reverse agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The `npx clawhub@latest` install command is mutable and may resolve to a different installer over time.

Mitigation: Prefer the manual copy path or a pinned, reviewed ClawHub installer version before installation.

Risk: The included `install.sh` refers to files that are not present in the artifact, making that installer path unreliable.

Mitigation: Use the manual SKILL.md copy path or review and adapt the installer before running it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kgapol/skills/mit-reasoning-lite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with numbered reasoning steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No configuration required; manual copy path is supported.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
