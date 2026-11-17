## Description:

A preliminary checklist that scores whether a financial AI system documents registration, supporting evidence, and decision gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial compliance teams can use the checklist to review model registration, evidence, and decision gates before deployment. Its result is preliminary and does not verify evidence or establish regulatory compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The keyword checklist can approve descriptions of missing safeguards and does not verify licences, evidence, or regulatory compliance.

Mitigation: Treat results as preliminary; independently verify evidence, require explicit approval of affected financial flows, and establish a recovery plan before using results in financial workflows.

Risk: The documented automatic enforcement modes are not implemented by the bundled code, so the checklist itself does not control transactions or data flows.

Mitigation: Do not rely on this tool to execute or block financial actions; specify and review any separate enforcement mechanism before connecting it to the output.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-fin-guard)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON or plain-text checklist report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A self-assessment based on keyword matches or supplied answers; results are not independently verified.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata; bundled SKILL.md says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
