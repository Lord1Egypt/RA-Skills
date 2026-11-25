## Description:

Apply anonymization (Art. 5, XI) and pseudonymization (Art. 13, §4) techniques to take data out of LGPD scope or reduce risk in analytics pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to choose and apply anonymization or pseudonymization approaches in analytics pipelines involving personal data under Brazil's LGPD, and to assess re-identification risk.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: The privacy-focused skill may activate for general analytics or ML pipeline work.

Mitigation: Confirm that the task involves LGPD privacy, anonymization, or pseudonymization before applying its guidance.

Risk: Pseudonymized or insufficiently anonymized data can remain vulnerable to re-identification.

Mitigation: Treat pseudonymized data as personal data and run linkage, inference, and singling-out checks before declaring a dataset anonymized.

## Reference(s):

- [ClawHub release](https://clawhub.ai/goul4rt/skills/lgpd-anonymization)
- [Server-resolved source repository](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-anonymization)
- [Anonymization and pseudonymization recipes](assets/anonymization-recipes.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown guidance with SQL and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation examples and re-identification checks; no fixed output schema.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
