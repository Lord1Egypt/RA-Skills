## Description:

Generates a competitive patent-intelligence report for a named company and technology area, covering the patent landscape, competitors, and potential opportunities and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and patent teams use the skill to assess a company's technology-specific patent position and competitors' activity before strategic decisions. A PatentMax API key and confirmation before the paid report request are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, analysis objectives, or optional background materials are sent to PatentMax for processing.

Mitigation: Confirm third-party sharing is permitted and obtain organizational approval before sending trade secrets or sensitive materials.

Risk: Exposure of the PatentMax API key could allow unauthorized use.

Mitigation: Protect PATENTMAX_API_KEY like a password and do not include it in reports or shared materials.

Risk: Downloaded reports and JSON results are saved locally and may contain sensitive analysis.

Mitigation: Review the output files in the working directory or chosen output folder and handle them under applicable data policies.

Risk: Incomplete patent coverage or lower-quality results could lead to overconfident decisions.

Mitigation: Check report quality status, disclose search limitations, and obtain specialist review before legal or filing decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ip930/skills/patentmax-competitive)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Workflow](references/workflow.md)
- [Input materials guide](references/materials-guide.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown summary and locally saved DOCX report and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report quality status and source-coverage limitations should accompany conclusions.]

## Skill Version(s):

1.2.1 (source: server-resolved release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
