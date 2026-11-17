## Description:

Guides agents in choosing PixelLab workflows for setup, image and sprite creation or editing, animation, and related asset tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shilo](https://clawhub.ai/user/shilo)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to configure PixelLab access, select documented MCP or REST workflows, and create or manage game art assets. It also provides guidance for editing, animation, and local asset review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some workflows may send user-provided images to PixelLab, and the security guidance notes that some workflows may lack a privacy disclosure.

Mitigation: Before using an image-upload workflow, make the external processing clear and confirm the user is comfortable with it.

Risk: The security scan was partial: some local references were unresolved and binary content was outside static analysis.

Mitigation: Review unresolved references and binary assets before relying on the scan as a complete assessment.

## Reference(s):

- [PixelLab API documentation](https://www.pixellab.ai/docs)
- [PixelLab REST API reference](https://api.pixellab.ai/v2/docs)
- [PixelLab MCP tool guide](https://api.pixellab.ai/mcp/docs)
- [Setup guidance](references/setup.md)
- [Credential guidance](references/credentials.md)
- [Cost and route guidance](references/cost-routing.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls, Code, Shell commands, Configuration, Image and animation files]

**Output Format:** [Markdown guidance, commands, code and configuration snippets, and image or animation assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the requested task; live asset workflows may send images to PixelLab.]

## Skill Version(s):

3.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
