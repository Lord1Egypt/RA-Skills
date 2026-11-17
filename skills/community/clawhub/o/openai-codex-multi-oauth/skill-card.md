## Description:

Helps developers manage and debug multiple OpenAI Codex OAuth profiles in OpenClaw, including profile switching, session overrides, usage mismatches, auth ordering, active-slot routing, broken-token recovery, and same-email workspace selection issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wthh031230](https://clawhub.ai/user/wthh031230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and repair OpenClaw deployments that route more than one OpenAI Codex OAuth identity, especially when status, session, usage, or helper-command behavior disagrees with the intended profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics can expose unredacted account, session, and usage details.

Mitigation: Run diagnostics locally, share only redacted output, and treat JSON usage reports as account metadata.

Risk: Usage or status checks can report the wrong profile when local selection falls back to provider order instead of the intended identity.

Mitigation: Prefer specific profile selection and verify the current session override, auth order, active slot, and usage source before patching.

Risk: Editing OpenClaw auth or session state can disrupt profile routing.

Mitigation: Back up the affected runtime files, change the smallest inconsistent layer, and retest status, switching, and usage after each change.

## Reference(s):

- [Runtime Files and Inspection Points](references/runtime-files.md)
- [Profile-Specific Usage Debugging](references/usage-debugging.md)
- [Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON diagnostics, and targeted code or configuration edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local OAuth profile, session, and usage files; diagnostic JSON can include account metadata.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
