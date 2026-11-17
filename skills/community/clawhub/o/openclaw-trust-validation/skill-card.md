## Description:

Adds memory trust validation guidance for OpenClaw 4.2 so an agent verifies memory-derived file, code, and configuration claims before acting on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicshliu](https://clawhub.ai/user/nicshliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add memory trust checks to OpenClaw behavior before an agent edits code, answers from remembered implementation details, or sends messages based on potentially stale memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to persistently change OpenClaw system prompt behavior.

Mitigation: Review the persistent prompt changes before installing and apply them only when the user wants memory-validation behavior across sessions.

Risk: The skill includes shell-command templates that use memory-derived file paths, functions, variables, and configuration names.

Mitigation: Revise command examples to use structured arguments, quoted values, -- option termination, and workspace-bound path checks before operational use.

## Reference(s):

- [OpenClaw: trust validation ClawHub page](https://clawhub.ai/nicshliu/skills/openclaw-trust-validation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested file, code, and configuration verification commands before using memory-derived claims.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
