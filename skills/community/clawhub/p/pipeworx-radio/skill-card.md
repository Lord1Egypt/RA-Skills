## Description:

Search and discover internet radio stations worldwide by name, genre, or country with direct stream URLs and detailed metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building music, localization, or creative-coding features use this skill to discover internet radio stations, inspect metadata, and retrieve direct stream URLs through the Pipeworx radio MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Radio search queries are routed through the Pipeworx-hosted MCP endpoint.

Mitigation: Avoid sending sensitive personal or internal project information as search terms unless the service is trusted.

## Reference(s):

- [Pipeworx radio skill page](https://clawhub.ai/brucegutman/skills/pipeworx-radio)
- [Bruce Gutman publisher profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx radio MCP endpoint](https://gateway.pipeworx.io/radio/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns station metadata such as stream URL, codec, bitrate, country, language, and tags.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
