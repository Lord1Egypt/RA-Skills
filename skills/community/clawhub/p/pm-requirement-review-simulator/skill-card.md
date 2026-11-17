## Description:

PRD review stress-test simulator: five cross-functional roles challenge requirements and output a scored HTML or Markdown survival report with a radar chart and meeting script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and cross-functional teams use this skill to rehearse requirement reviews before a meeting, surface engineering, operations, design, executive, and legal objections, and generate review assets. It is especially oriented toward Chinese-language PRD review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML report output can carry script-injection risk when report fields include untrusted PRD content.

Mitigation: Prefer Markdown for untrusted PRD input; if HTML is required, escape dynamic fields, allowlist placeholder values, use a restrictive CSP, and review the generated report before sharing.

Risk: The workflow is Chinese-oriented and may not match every review culture or language context.

Mitigation: Confirm that the role prompts, scoring labels, and final report language fit the intended organization before deployment.

## Reference(s):

- [Intake Form](assets/intake-form.html)
- [Scoring Engine](references/scoring-engine-deterministic.md)
- [Review Playbook](references/review-playbook.md)
- [Report Template](references/report-template-pro.html)
- [User Templates](references/user_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [HTML or Markdown report with structured review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes survival score, Go decision, five-role objections, top counterarguments, RACI matrix, meeting script, action checklist, and disclaimer.]

## Skill Version(s):

1.2.8 (source: server release evidence and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
