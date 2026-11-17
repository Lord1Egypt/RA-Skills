## Description:

A cross-session handoff protocol for Claude Code and other AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allen-cao](https://clawhub.ai/user/allen-cao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to pause long-running work, save the minimum execution context in a handoff file, and resume in a later session or another compatible agent after reviewing the recovered state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved handoff files can persist task context, session metadata, secrets, proprietary details, or sensitive customer data under the local handoff directory or a configured cloud-sync path.

Mitigation: Review handoff contents before relying on them, avoid saving secrets or sensitive data, and use only trusted, access-controlled storage for HANDOFF_ROOT.

Risk: Restoring handoffs has weak ID validation and path containment according to the security evidence.

Mitigation: Use explicit handoff commands and known IDs, inspect restored handoff content before continuing, and fix ID validation and path containment before use in shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allen-cao/skills/handoff-session)
- [README.md](artifact/README.md)
- [Templates V2](artifact/references/templates.md)
- [Handoff V2 usage documentation](artifact/使用文档.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown handoff file content, recovery previews, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one handoff.md package per saved session context and short recovery previews before resuming.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
