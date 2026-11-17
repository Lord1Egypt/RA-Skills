## Description:

Screen legal AI research, drafting, and opinion assistance against traceability, evidence, and gating rules, returning an advisory pass-or-hold assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Legal teams, law firms, and developers can use the skill to run a lightweight self-assessment of AI systems used for legal research, drafting, or opinion assistance. Treat its score as advisory and have qualified people verify the underlying evidence.

### Deployment Geography for Use:

Global; assess legal and professional requirements in the applicable jurisdiction.

## Known Risks and Mitigations:

Risk: A PASS result could be mistaken for a legal-compliance certification.

Mitigation: Use the result only as an advisory checklist and require human review of the underlying evidence and applicable obligations.

Risk: Keyword matches and self-reported answers do not establish valid credentials or reliable citations.

Mitigation: Independently verify professional credentials, cited sources, and supporting records before relying on an assessment.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD governance theory](https://github.com/zhaoxinghua09-cell/LGD)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [Published skill source link](https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-law-ethic)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [JSON or plain-text assessment on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scores for three governance rules, a pass-or-hold result, and missing evidence; a pass is not legal compliance certification.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
