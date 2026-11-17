## Description:

OpenClip lets an agent connect to the OpenClip MCP server to turn long videos or URLs into short captioned clips and run media utilities such as transcription, conversion, image editing, background removal, and UGC clip generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yordilorenzo](https://clawhub.ai/user/yordilorenzo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to connect agents to OpenClip for asynchronous video clipping, captioned rendering, transcription, media conversion, image editing, background removal, reusable presets, and short UGC-style clip generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, images, URLs, and related metadata are sent to the remote OpenClip service for processing.

Mitigation: Use the skill only with media appropriate for external processing, prefer OAuth over manual token handling, and avoid private or sensitive inputs unless OpenClip's retention and processing practices are acceptable.

Risk: Completed processing can return permanent CDN output links.

Mitigation: Review generated output links before sharing them and avoid submitting media where persistent URLs would create privacy, confidentiality, or rights-management concerns.

Risk: Manual Bearer-token setup exposes an authentication secret to the agent client configuration.

Mitigation: Prefer the OAuth connection path where supported; if manual tokens are required, rotate tokens when no longer needed and do not paste them into conversation history.

## Reference(s):

- [OpenClip skill page](https://clawhub.ai/yordilorenzo/skills/openclip)
- [OpenClip MCP server](https://openclip.app/mcp)
- [OpenClip manual token MCP endpoint](https://openclip.app/mcp/key)
- [OpenClip reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown guidance with inline commands, JSON configuration snippets, tool names, status values, and generated media URLs returned by the OpenClip service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides asynchronous MCP workflows that return job identifiers, status strings, transcripts, clip metadata, captioned render URLs, CDN output URLs, and error messages.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
