## Description:

A modular 5-step engineering verification loop that helps agents plan, execute, check, and summarize complex coding or planning tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwe77](https://clawhub.ai/user/uwe77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to apply a structured verification loop to complex engineering, architecture, coding, and planning tasks before producing final output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks agents to persistently register the skill in memory and auto-activate on broad future tasks.

Mitigation: Install only with explicit user approval, and prefer removing the registration hook or requiring explicit /lor invocation for each use.

Risk: Broad automatic activation can cause this verification loop to influence unrelated future complex tasks.

Mitigation: Keep activation manual or project-scoped, and review generated verification plans before executing proposed actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uwe77/skills/lor-skill)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and console-style verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a five-step verification flow with up to three retries; setup emits a registration hook.]

## Skill Version(s):

1.0.1 (source: server evidence release.version, package.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
