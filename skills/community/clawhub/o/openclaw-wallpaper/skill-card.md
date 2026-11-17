## Description:

OpenClaw Wallpaper turns a Lively Wallpaper desktop into an OpenClaw chat surface with streaming replies, image input, achievements, persistent context, reconnect logic, and one-click setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femnn](https://clawhub.ai/user/femnn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and run a desktop wallpaper chat companion backed by OpenClaw, with streaming conversation, image input, achievement tracking, and persistent session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated local network services may be reachable beyond the intended desktop session.

Mitigation: Bind services to 127.0.0.1, add a per-install authentication token, and avoid exposing the bridge on broader network interfaces.

Risk: An embedded gateway token can be reused if the artifact is shared or installed unchanged.

Mitigation: Remove the embedded token and load a user-specific token from local configuration or environment variables at install time.

Risk: Permissive CORS allows unexpected web origins to call the local bridge endpoints.

Mitigation: Restrict allowed origins, methods, and headers to the wallpaper UI and required local clients.

Risk: The UI file server path handling may serve unintended files if requests are not constrained.

Mitigation: Normalize requested paths, reject traversal attempts, and serve only files under the intended wallpaper UI directory.

Risk: Conversation and image-derived data may remain on disk or in browser storage after a user clears the visible chat.

Mitigation: Delete persisted session files and relevant browser storage when clearing data, and document what data is retained.

## Reference(s):

- [OpenClaw Wallpaper release page](https://clawhub.ai/femnn/skills/openclaw-wallpaper)
- [Lively Wallpaper](https://github.com/rocksdanister/lively)
- [Lively Wallpaper releases](https://github.com/rocksdanister/lively/releases)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and bundled JavaScript, HTML, CSS, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local wallpaper chat experience that exchanges text and optional image inputs with OpenClaw through local HTTP endpoints.]

## Skill Version(s):

0.2.1 (source: server release evidence, created 2026-03-21; artifact changelog top entry is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
