## Description:

Generate PNG or SVG images from Mermaid diagram syntax using the mermaid.ink API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-ng](https://clawhub.ai/user/vincent-ng)

### License/Terms of Use:


## Use Case:

Developers, technical writers, and content creators use this skill to convert Mermaid diagrams into PNG or SVG assets for documentation, presentations, and shareable visual explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram text is sent to the external mermaid.ink rendering service.

Mitigation: Do not use the skill for diagrams containing secrets, private infrastructure details, customer data, or other sensitive information unless switching to a local renderer.

Risk: Image generation requires network access to mermaid.ink.

Mitigation: Confirm connectivity before use, or use a local Mermaid renderer for offline workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincent-ng/skills/mermaid-image-generator)
- [Mermaid.ink PNG endpoint](https://mermaid.ink/img/{base64_code})
- [Mermaid.ink SVG endpoint](https://mermaid.ink/svg/{base64_code})
- [Mermaid Live syntax validator](https://mermaid.live)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PNG or SVG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output format is selected from the file extension; Mermaid input can be read from a file or stdin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
