## Description:

Uses a Moonshot-style multimodal model workflow for image analysis, OCR extraction, copywriting, and multimodal conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mendynew](https://clawhub.ai/user/mendynew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to configure and call a multimodal API workflow for image understanding, OCR, marketing copy generation, and image-plus-text conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, prompts, and the API key may be sent to a configurable remote endpoint.

Mitigation: Use only non-sensitive images or documents unless the endpoint and provider data handling are trusted; keep BASE_URL restricted to trusted hosts and store API keys in environment variables.

Risk: Broad activation triggers may cause unintended use of the multimodal API workflow.

Mitigation: Review activation triggers and require explicit user intent before sending images, documents, or prompts to the remote service.

Risk: The current package may need fixes before it runs correctly.

Mitigation: Smoke test configuration checks, CLI commands, and core Python API paths in an isolated environment before relying on the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mendynew/skills/moonshot)
- [Moonshot Platform](https://platform.moonshot.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, JSON-style structured results, Python examples, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process local image paths, prompts, model parameters, temperature, token limits, language options, and optional output files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
