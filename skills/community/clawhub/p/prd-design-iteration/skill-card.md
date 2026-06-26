## Description: <br>
Use this skill when the user wants to iterate on an existing company-internal process management system by adding, modifying, or deleting features through a screenshot-centered four-step workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lailiai](https://clawhub.ai/user/lailiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, designers, and internal tooling teams use this skill to gather iteration requirements for existing process-management systems and produce a delta PRD plus a modified prototype with before/after comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may collect and persist internal screenshots, HTML prototypes, customer data, credentials, tokens, internal URLs, or proprietary details in local project artifacts. <br>
Mitigation: Redact sensitive content before use and review generated project files before sharing or committing them. <br>
Risk: Generated prototypes may load public CDN dependencies. <br>
Mitigation: Replace or pin CDN-loaded dependencies with approved internal copies and stronger integrity controls before opening prototypes that contain sensitive content. <br>
Risk: Iteration guidance and generated PRD/prototype changes may be incomplete or misleading if screenshots or workflow details are missing. <br>
Mitigation: Require the documented confirmation checkpoints and review the validation output before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lailiai/prd-design-iteration) <br>
- [Step 1 baseline collection](references/steps/step1-baseline-collection.md) <br>
- [Step 2 adjustment list](references/steps/step2-adjustment-list.md) <br>
- [Step 3 material collection](references/steps/step3-material-collection.md) <br>
- [Step 4 validation and output](references/steps/step4-validation-output.md) <br>
- [Prototype template](references/templates/prototype-template.html) <br>
- [Iteration design self-check](references/appendices/selfcheck.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown documents and HTML prototype files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project artifacts including baseline notes, adjustment lists, delta PRD content, validation notes, and prototype HTML.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
