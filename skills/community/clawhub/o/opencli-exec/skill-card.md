## Description:

Deprecated compatibility alias for the canonical `opencli` skill, intended only for older notes, memory, or prompts that still refer to `opencli-exec`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this compatibility alias when legacy workspace notes or prompts still reference `opencli-exec`, then route to the canonical `opencli` skill and wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alias routes agent behavior and shell execution to files at a fixed local path outside the released package.

Mitigation: Install only when that canonical `opencli` skill exists at the referenced path and has been independently reviewed and trusted.

Risk: The package does not pin or validate the external skill and script that will actually be followed or executed.

Mitigation: Verify the external skill and wrapper before use and repeat review when the referenced local files change.

## Reference(s):

- [Deprecated alias commands](artifact/references/commands.md)
- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/opencli-exec)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates command execution to a canonical local wrapper outside this package.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
