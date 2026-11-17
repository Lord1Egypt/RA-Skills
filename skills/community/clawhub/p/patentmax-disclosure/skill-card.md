## Description:

Turns invention ideas and R&D materials into patent technical disclosure documents and review notes using PatentMax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Inventors, R&D teams, and patent professionals use this skill to turn technical materials or a preliminary idea into a patent disclosure for review. It can suggest invention directions before drafting; the output is not a patent application or a guarantee of patentability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive invention materials are sent to PatentMax for processing.

Mitigation: Confirm the user is comfortable sending the materials and redact secrets or unnecessary core parameters before submission.

Risk: An untrusted API endpoint could receive invention data or API credentials.

Mitigation: Use a trusted PATENTMAX_API_KEY and do not set PATENTMAX_BASE_URL to an unknown host.

## Reference(s):

- [PatentMax skill release](https://clawhub.ai/ip930/skills/patentmax-disclosure)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Materials guide](references/materials-guide.md)
- [Workflow and results guide](references/workflow.md)
- [Frequently asked questions](references/faq.md)

## Skill Output:

**Output Type(s):** [Files, Text, JSON]

**Output Format:** [Two Word (.docx) documents, with text progress and result summaries and JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a technical disclosure and separate review notes; idea exploration can return ranked directions.]

## Skill Version(s):

1.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
