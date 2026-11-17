## Description:

Render JSON schemas to images and generate schemas from prompts using declare-render and AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cai-zhuo](https://clawhub.ai/user/cai-zhuo)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to validate declare-render JSON schemas, render them to PNG or JPG images, and optionally generate a schema from a natural-language prompt before rendering it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says unreviewed local code receives the OpenAI API key.

Mitigation: Review the installed code and dependency set before use, and run with a scoped API key in an environment that limits credential exposure.

Risk: The security evidence flags a Windows launcher pattern that can turn crafted arguments into shell commands.

Mitigation: Avoid using the Windows launcher path until the release removes shell-based launching or the command arguments have been independently reviewed.

Risk: The security guidance calls out missing clarity around render dimensions and data sent to the configured OpenAI-compatible endpoint.

Mitigation: Validate schema dimensions before rendering and document or review prompt/schema data handling before enabling AI-assisted generation.

## Reference(s):

- [Materials Cli release page](https://clawhub.ai/cai-zhuo/skills/materials-cli)
- [node-canvas installation guide](https://github.com/Automattic/node-canvas#installation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON schema or image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Node, canvas system dependencies, and OPENAI_API_KEY for AI-assisted generation.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
