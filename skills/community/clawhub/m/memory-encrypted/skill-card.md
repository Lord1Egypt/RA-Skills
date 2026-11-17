## Description:

Provides guidance for local encrypted memory storage and scheduled memory backups for security, privacy, and backup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujw0214](https://clawhub.ai/user/liujw0214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to request guidance for encrypting local agent memory, backing it up, listing backups, and restoring memory in privacy-sensitive scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes strong encryption and backup claims without auditable implementation evidence.

Mitigation: Do not rely on the encryption claims unless the publisher provides auditable code, clear key-management details, and tested restore behavior.

Risk: The memory key is described as stored unencrypted and as suitable for separate backup, which could expose sensitive memory if mishandled.

Mitigation: Treat the memory key as highly sensitive, protect it with operating-system controls or a secret manager, and avoid uploading an unprotected key to cloud storage.

Risk: Automatic backup, restore, retention, and memory viewing behavior could expose or alter sensitive memory without clear user control.

Mitigation: Require explicit user control for viewing, restoring, automatic backup, retention, and disabling behavior before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujw0214/skills/memory-encrypted)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes memory encryption, backup, restore, key handling, and retention guidance; no implementation code is provided in the artifact.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
