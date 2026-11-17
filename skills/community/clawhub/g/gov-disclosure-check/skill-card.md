## Description:

Checks government disclosure text for mentions of the decision basis, responsible department, deadline, remedy channel, and data source, then reports which fields appear to be missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Government communications teams, policy staff, and auditors can use the checker to scan proposed notices or disclosure replies for keyword mentions of five required fields and identify items for human review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checklist can be mistaken for a full legal or compliance validation, and its permission and CLI documentation are inconsistent.

Mitigation: Use only text or documents you choose, restrict file access through the host, do not grant write or web access, and treat results as a keyword checklist requiring human review before publication; correct the permission declarations and CLI documentation.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text summary or JSON containing the fields with absent keyword matches and a completeness flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keyword checklist; a human must review results before publication.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
