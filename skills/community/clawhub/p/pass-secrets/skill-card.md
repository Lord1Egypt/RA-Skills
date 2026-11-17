## Description:

Store, retrieve, list, and remove GPG-encrypted secrets using the pass password-store with a specified GPG key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage local password-store secrets and generate pass commands for storing, retrieving, listing, exporting, and removing entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret values can be exposed through plaintext retrieval or printed shell export commands.

Mitigation: Use only password-store entries you control, avoid eval or source on generated export output, and treat terminal output as sensitive.

Risk: Removing a password-store entry with the wrong path can delete the wrong secret.

Mitigation: Confirm exact secret paths before removal and maintain separate backups of the password store and GPG data.

Risk: Generated environment export output can become unsafe when consumed as shell code.

Mitigation: Prefer direct pass commands or revise the helper to validate variable names and shell-escape values before using generated exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/pass-secrets)
- [Publisher profile](https://clawhub.ai/user/space-cadet)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print plaintext secrets or shell export commands when retrieving or exporting entries; treat output as sensitive.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
