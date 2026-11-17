## Description:

Creates original orange-booth performance prompts and short shot plans from authorized photo, text, or motion references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and other users draft original performance prompts and timed shot plans for authorized subjects and references, with rights checks and continuity guidance before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup fetches and runs an unpinned GitHub package, creating a mutable code-execution supply-chain risk.

Mitigation: Use the text-only workflow by default; review the MCP source and pin a trusted commit or release before installing, especially in sensitive environments.

Risk: Unlicensed references or requests to copy a performance or identity may infringe rights or mislead viewers.

Mitigation: Confirm rights to reference media and audio, reject deceptive impersonation, and reframe exact copies as original scenes before drafting a generation-ready prompt.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gpt-img-2/skills/hotel-lobby-ai-prompt-director)
- [Hotel Lobby video generator](https://aihotellobby.art/hotel-lobby-video)
- [Hotel Lobby tutorial](https://aihotellobby.art/how-to-do-hotel-lobby-ai-trend)
- [Optional MCP source](https://github.com/gpt-img-2/hotel-lobby-ai-prompt-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a prompt, timed shot beats, rights check, and warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides continuity anchors and a live-setting check; does not generate media.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
