## Description:

Generate comparative market analysis (CMA) and home valuation reports from IDX listing data and selected comparable properties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

External real estate agents, brokers, and support staff use this skill to build CMA packages from subject-property details and selected IDX comparables, including valuation calculations, a client-facing report, and an interactive handoff prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated interactive reports can run code hidden in listing data if opened or shared.

Mitigation: Review or patch the generated HTML handling before using untrusted IDX or comparable data, especially before publishing the interactive report.

Risk: CMA outputs may contain private property or client information.

Mitigation: Treat generated CMA files as private and only upload cma_data.json or reports to Google tools when the user expects that sharing.

Risk: Missing, stale, or low-quality comparable data can weaken the valuation estimate.

Mitigation: Surface data gaps, outliers, and assumptions before presenting the estimate, and keep the output framed as CMA support rather than a licensed appraisal.

## Reference(s):

- [CMA Input Schema](references/cma-input-schema.md)
- [Valuation Guidelines](references/valuation-guidelines.md)
- [Gemini Canvas / AI Studio Publish Checklist](references/gemini-canvas-publish.md)
- [Google AI Studio](https://aistudio.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, guidance]

**Output Format:** [Markdown report, JSON calculation payload, single-file HTML, and Markdown prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CMA outputs may include property and client information and should be reviewed before sharing.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
