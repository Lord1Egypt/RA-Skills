## Description:

Quick reference for every OpenClaw CLI command, sub-command, and flag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teeddub](https://clawhub.ai/user/teeddub)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agent users use this skill to answer OpenClaw CLI usage questions, verify flags, and produce concise command examples before making operational changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste examples can target external accounts, message channels, vault paths, or other user-controlled resources.

Mitigation: Replace placeholder or hardcoded targets with user-confirmed values before execution, and confirm destructive or state-changing operations explicitly.

Risk: Some examples can run local scripts or live operational commands whose behavior is outside the cheatsheet itself.

Mitigation: Independently inspect local scripts, permissions, and runtime targets before running live commands.

Risk: CLI reference material may be stale or incomplete for a specific installed OpenClaw version.

Mitigation: Verify uncovered or uncertain flags with `openclaw <command> --help` before recommending execution.

## Reference(s):

- [OpenClaw CLI Cheatsheet](references/openclaw-cheatsheet.md)
- [ClawHub skill page](https://clawhub.ai/teeddub/skills/openclaw-cheatsheet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise explanations and inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be scoped to the requested OpenClaw command area, with warning language before destructive or state-changing operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
