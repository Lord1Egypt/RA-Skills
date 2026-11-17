## Description:

Prevent memory loss in OpenClaw by adding a practical continuity and recovery layer that preserves active work across restarts, compaction, and crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smarthomesus](https://clawhub.ai/user/smarthomesus)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use No Amnesia to preserve active work context and recover more consistently after restarts, compaction, or crashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing memory or recovery components could overwrite or disrupt existing OpenClaw state.

Mitigation: Review the package before making changes and back up existing OpenClaw memory and recovery files before installation.

Risk: A recovery setup may not preserve the intended task context in a specific workspace.

Mitigation: Run a controlled recovery test on a small task before relying on the workflow for active work.

## Reference(s):

- [No Amnesia on ClawHub](https://clawhub.ai/smarthomesus/skills/no-amnesia)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown guidance and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only artifact; no executable code or automatic file changes were found in the inspected release.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
