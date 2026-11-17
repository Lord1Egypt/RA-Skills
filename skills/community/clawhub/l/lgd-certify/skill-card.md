## Description:

Provides a command-line workflow for recording an AI system passport, hashing supplied evidence files, and producing a gate verdict with certification and badge files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI governance teams can use this CLI to organize identity, data, validation, behavior, change, and issuance evidence for an AI system and create local records and a gate result. Its output is bookkeeping based on supplied files and should not be treated as proof of compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A passing certificate may be issued without verifying the supplied evidence, so the result can be mistaken for proof of compliance.

Mitigation: Review the evidence independently before relying on a PASS result, and treat certificates and badges as local bookkeeping rather than compliance proof.

Risk: The tool does not preserve the audit history it promises.

Mitigation: Keep separate audit backups of the evidence and generated records.

Risk: Using a project directory with symbolic links can undermine containment assumptions.

Mitigation: Use a dedicated project directory without symbolic links.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-certify)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [JSON records, a Markdown badge snippet, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes records and badge files under the user-specified project directory; it does not send data externally by default.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
