## Description:

小红书自动化 skill that lets an agent run shell scripts to log in, fetch Xiaohongshu trends, generate posts and images, and publish notes through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearl799](https://clawhub.ai/user/pearl799)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to automate Xiaohongshu content workflows from chat, including trend discovery, content generation, login status checks, and publishing. It is intended for OpenClaw environments with uv, Chrome, a configured Xiaohongshu account, and an OpenAI-compatible image generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Xiaohongshu credentials and publishing authority.

Mitigation: Use a test Xiaohongshu account first, restrict cookie and openclaw.json permissions, and rotate or remove stored cookies and API keys when uninstalling.

Risk: Auto-publish mode can create public posts without an additional preview step.

Mitigation: Keep auto-publish disabled unless public posting is explicitly intended, and use preview mode for generated content review.

Risk: Running the bundled SSE MCP server on a network interface can expose skill capabilities beyond the local user.

Mitigation: Avoid exposing the SSE MCP server on a network interface unless access controls and network restrictions are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pearl799/skills/openclaw-xhs)
- [OpenClaw](https://openclaw.ai)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts emit JSON status fields and MEDIA lines for generated image attachments.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
