## Description:

Helps teams iterate existing company-internal process management systems by collecting workflow evidence, classifying add, modify, and delete changes, and producing a delta PRD plus a before-and-after prototype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lailiai](https://clawhub.ai/user/lailiai)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, product designers, and internal-system teams use this skill to structure iteration work for an existing internal process management system. It guides collection of roles, current workflow, screenshots or interface descriptions, change scope, validation checks, and final PRD/prototype outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided product notes, screenshots, HTML prototypes, internal URLs, credentials, or production secrets may be written into the local project workspace.

Mitigation: Redact customer data, credentials, internal URLs, and production secrets before providing screenshots, HTML, or workflow details.

Risk: Generated prototype templates may load third-party CDN scripts.

Mitigation: Open generated prototypes in an isolated browser context where possible and review external dependencies before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lailiai/skills/prd-design-iteration)
- [Step 1: Baseline Collection](references/steps/step1-baseline-collection.md)
- [Step 2: Adjustment List](references/steps/step2-adjustment-list.md)
- [Step 3: Material Collection](references/steps/step3-material-collection.md)
- [Step 4: Validation and Output](references/steps/step4-validation-output.md)
- [Prototype Template](references/templates/prototype-template.html)
- [Self-check Checklist](references/appendices/selfcheck.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Files]

**Output Format:** [Markdown documents and an HTML/React prototype]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged project files after user confirmations; generated prototypes may load React, Babel, and Tailwind from third-party CDNs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
