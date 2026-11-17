## Description:

OpenClaw AI intelligent-agent troubleshooting skill for startup errors, stalled tasks, tool failures, GPU memory issues, memory loss, logic failures, and session problems using a standardized intake, check, diagnosis, treatment, and follow-up workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speakmen](https://clawhub.ai/user/speakmen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to triage and repair OpenClaw AI agent failures, including startup errors, deadlocks, tool registration issues, GPU memory pressure, context problems, permission failures, and gateway crashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides powerful repair commands without enough safety checks or warnings.

Mitigation: Review each command before execution, verify target paths, back up affected files, and avoid automatic package installs, deletes, chmod changes, or API-key exports.

Risk: Credential-handling guidance includes exporting a replacement OpenClaw API key.

Mitigation: Use least-privilege credentials, avoid storing secrets in shell history, and rotate exposed keys.

Risk: Permission repair examples can broaden access to workspace memory and project files.

Mitigation: Prefer owner-only permissions where possible and confirm file ownership before changing permissions recursively.

## Reference(s):

- [Openclaw Ai Doctor on ClawHub](https://clawhub.ai/speakmen/skills/openclaw-ai-doctor)
- [speakmen publisher profile](https://clawhub.ai/user/speakmen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with diagnostic steps, tables, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed before execution because several repair steps can install packages, delete lock files, change permissions, or export credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
