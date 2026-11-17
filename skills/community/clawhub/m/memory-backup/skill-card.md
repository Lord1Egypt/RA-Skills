## Description:

Inspect OpenClaw memory configuration and on-disk memory artifacts, confirm which enabled memory systems should be backed up, prepare a deterministic local memory backup bundle, and optionally hand that bundle off to mnemospark or other storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pawlsclick](https://clawhub.ai/user/pawlsclick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit enabled memory systems, confirm durable memory files on disk, and create a restorable memory-only backup archive. When requested, it can prepare a local archive for a separate mnemospark cloud-storage handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup discovery and packaging could include unintended local files if paths are not reviewed.

Mitigation: Review every proposed canonical path before approving archive creation, and use only discovery JSON generated and inspected in the current session.

Risk: Cloud handoff could export memory artifacts that should remain local.

Mitigation: Keep archives local unless cloud storage is explicitly requested and the exact archive selected for upload has been shown to the user.

Risk: The documented mnemospark install command uses an unsafe force-install flag.

Mitigation: Avoid the unsafe install path unless the user accepts that risk after reviewing the plugin source and operational need.

Risk: Running on an untrusted workspace or stale discovery input can make backup contents unreliable.

Mitigation: Do not use the skill on untrusted workspaces or with discovery JSON that was not freshly generated from the target workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pawlsclick/skills/memory-backup)
- [mnemospark](https://mnemospark.ai)
- [Scope and paths](references/scope-and-paths.md)
- [Manifest schema](references/manifest-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and generated archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing backup proposals, local tar.gz backup bundles, and manifest JSON when backup creation is confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
