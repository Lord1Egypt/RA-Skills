## Description:

Guides an agent to create and upload a mobile-compatible HTML game package with configuration, game code, and preview image files to a third-party game-hosting API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianclan](https://clawhub.ai/user/brianclan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to package a simple browser game and upload its required config.json, index.html, and preview.png files. The workflow is intended for publishing mobile-compatible HTML games through the documented thenext.games upload flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may upload game files to a third-party service and produce a public game URL.

Mitigation: Only upload files intended for publication, confirm the gameFolder and destination endpoint, and review generated files before running the curl commands.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/brianclan/skills/nextgame)
- [aigames upload API host](https://www.idlab.top)
- [thenext.games game URL pattern](https://thenext.games/game/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of config.json, index.html, and preview.png, then reports the public game URL after a successful upload.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
