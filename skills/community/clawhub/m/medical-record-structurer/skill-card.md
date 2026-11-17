## Description:

Structures unstructured medical notes into standardized electronic medical record fields with text, file, batch, demo, and SkillPay-enabled usage paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare developers and operators can use this skill to convert clinical notes, patient histories, and other unstructured medical text into structured EMR-style records. Because the artifact handles sensitive medical information, outputs and deployment controls should be reviewed before use with real PHI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the package includes an unbounded self-evolution daemon and overstated privacy claims around sensitive medical data.

Mitigation: Review this package carefully before installing, do not run auto-evolve-daemon.sh or scripts/self_evolve.py, and scan the package before deployment.

Risk: The skill processes medical records that may contain PHI, while the inspected evidence does not support all advertised encryption, hashing, audit logging, and no-storage claims.

Mitigation: Avoid processing real PHI unless independent privacy, retention, encryption, access control, and audit controls are in place and verified.

Risk: Non-demo usage can call external billing endpoints and write local trial or subscription state.

Mitigation: Review SkillPay configuration, outbound network policy, and local state paths before enabling paid or trial workflows.

## Reference(s):

- [EMR schema reference](artifact/references/emr-schema.md)
- [SkillPay API reference](artifact/references/skillpay-api.md)
- [ClawHub skill page](https://clawhub.ai/andyxcg/skills/medical-record-structurer)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON EMR records with Markdown usage guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured records include patient demographics, clinical information, assessment and plan fields, provider information, and processing metadata.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
