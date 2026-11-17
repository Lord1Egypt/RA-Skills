## Description:

Comprehensive Greek individual tax return processing skill for employed individuals that handles E1 form preparation, personal income tax calculations, deduction optimization, property taxes (ENFIA), and individual compliance management for Greek tax residents with employment, property, and investment income.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

External users and tax-preparation agents use this skill to prepare Greek individual E1 return materials, calculate income tax and deductions, coordinate ENFIA property tax data, and assemble submission-ready guidance from local files. Human review is expected before filing, payment, digital signing, or any tax authority interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions extend beyond local tax preparation into email access, bank-data import, cloud upload, digital signing, AADE submission, and payment handling.

Mitigation: Require explicit human approval and separate operational controls before enabling any external account access, submission, signature, storage, or payment action.

Risk: Tax calculations and filing guidance may affect legal or financial obligations.

Mitigation: Use outputs as preparation material only and route all filing decisions, authority submissions, and payment schedules through qualified human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/greek-individual-taxes)
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, YAML, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local tax data files, jq, and OPENCLAW_DATA_DIR; no external credentials are required for local preparation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
