## Description:

Use for low-frequency archival recall when primary memory is insufficient, authorized cold-memory maintenance, or setting up and repairing automatic user-memory detection and recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuetsui](https://clawhub.ai/user/fuetsui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Hui-Yi to retrieve, maintain, and reinforce low-frequency cold-memory context when current conversation, primary memory, and recent notes are insufficient. It also supports explicitly authorized setup or repair of local recall integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a persistent local memory archive that can retain sensitive or outdated information.

Mitigation: Use it only in a trusted workspace, avoid storing secrets, and verify persisted evidence before treating a memory as current or reliable.

Risk: Explicit apply or enable operations can modify local memory files, hook files, or an existing OpenClaw configuration that may contain credentials.

Mitigation: Review dry-runs first, keep configuration backups private, and apply changes only within an authorized maintenance task.

Risk: Optional native recall integration may use host-configured model or embedding services and is scoped to the reviewed runtime and channels.

Mitigation: Confirm the runtime, channel scope, and cost expectations before enabling integration; re-audit after host upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuetsui/skills/hui-yi)
- [Cold Memory Schema Reference](references/cold-memory-schema.md)
- [Trigger Modes + Integration Patterns](references/integration-patterns.md)
- [Automatic Recognition and Recall](references/native-memory.md)
- [Hui-Yi 1.2.13 Release Notes](references/release-1.2.13.md)
- [Hui-Yi 1.2.12 Security Upgrade and Validation](references/security-upgrade-1.2.12.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell commands, and local configuration or file-change instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local cold-memory files, hook files, and OpenClaw configuration only when explicitly authorized by the user.]

## Skill Version(s):

1.2.13 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
