## Description:

Generates personal or corporate KYC document checklists and scores completeness based on the items a user reports having.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and onboarding teams can generate a preliminary personal or corporate KYC materials checklist and identify items they report as missing before submitting documents for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A checklist pass may be mistaken for verified KYC compliance or legal advice.

Mitigation: Treat the result as a preliminary materials aid; independently check actual documents and applicable institution and jurisdiction requirements.

Risk: The bundled usage text describes outdated flags and a data-file input that the current script does not support.

Mitigation: Use the declared scripts/kyc_checklist_gen.py entry point and its --help output; provide item numbers with --have and choose --type personal or corporate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/kyc-checklist-gen)
- [LGD theory project (background linked in README)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text checklist or JSON result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing items, a completeness score, and a pass/fail exit status based on supplied item numbers.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
