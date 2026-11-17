## Description:

Lightweight markdown editor with optional OpenClaw gateway chat. Filesystem-based, no database required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT

## Use Case:

Developers, technical writers, and individual users can run this skill to browse, edit, preview, and save Markdown files from a local directory, with optional chat assistance through an OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File access, network exposure, and chat context sharing can create privacy or access-control issues when used with sensitive Markdown directories.

Mitigation: Run the skill only against trusted Markdown directories, keep HOST on 127.0.0.1, and avoid using it for secrets or private notes.

Risk: Enabling chat can send the full current document to the configured OpenClaw gateway.

Mitigation: Enable chat only with a trusted gateway and token, and review document contents before sending chat requests.

Risk: The security guidance calls out unresolved controls around authentication, markdown sanitization, request limits, and explicit chat-context controls.

Mitigation: Deploy in a local, controlled environment and add those controls before broader or shared use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/musketyr/skills/markdown-editor-with-chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files edited through a local web UI, with JSON API responses and optional chat responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured MARKDOWN_DIR; optional chat uses OPENCLAW_GATEWAY_URL and OPENCLAW_GATEWAY_TOKEN.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
