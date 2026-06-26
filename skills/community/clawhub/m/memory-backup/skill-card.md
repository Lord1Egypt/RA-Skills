## Description: <br>
Inspect OpenClaw memory configuration and on-disk memory artifacts, confirm which enabled memory systems should be backed up, prepare a deterministic local memory backup bundle, and optionally hand that bundle off to mnemospark or other storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pawlsclick](https://clawhub.ai/user/pawlsclick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to audit enabled memory systems, review the exact memory artifacts proposed for backup, and create a restorable memory-only archive. It is also used when an explicit mnemospark handoff is requested after local backup preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memory can contain private or sensitive context. <br>
Mitigation: Review the proposed included paths before approving a backup and keep config files as discovery inputs rather than backup payloads. <br>
Risk: Optional mnemospark storage can move the backup archive outside local control. <br>
Mitigation: Prefer local backup unless mnemospark and the storage destination are trusted, and approve cloud upload only after the archive contents and handoff are clear. <br>


## Reference(s): <br>
- [Scope and paths](references/scope-and-paths.md) <br>
- [Manifest schema](references/manifest-schema.md) <br>
- [mnemospark](https://mnemospark.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with optional shell commands, JSON discovery data, and a deterministic tar.gz backup archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local archive with manifest metadata after user confirmation; cloud handoff remains a separate optional step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
