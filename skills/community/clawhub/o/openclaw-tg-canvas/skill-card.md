## Description:

Telegram Mini App Canvas renders agent-generated HTML, markdown, and A2UI content in a Telegram Mini App with `tg-canvas push`, a JWT-gated server terminal, and an optional OpenClaw Control UI proxy disabled by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clvv](https://clawhub.ai/user/clvv)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to publish agent-generated HTML, markdown, text, or A2UI content to a Telegram Mini App canvas and optionally access a JWT-gated server terminal or OpenClaw Control UI proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved Telegram users can obtain powerful shell access on the server through the terminal feature.

Mitigation: Only include fully trusted Telegram IDs in ALLOWED_USER_IDS and run the service as a dedicated unprivileged user or in an isolated container.

Risk: Exposed tunnels can make local push and clear endpoints reachable in ways that weaken loopback-only assumptions.

Mitigation: Keep PUSH_TOKEN strong and private, rotate it if exposed, and do not rely on loopback checks as the only protection when using cloudflared or similar tunnels.

Risk: Pushed HTML scripts execute in the Mini App context.

Mitigation: Push content only from trusted agents or workflows and review generated HTML before using it in sensitive sessions.

Risk: The optional OpenClaw Control UI proxy can expose local control surfaces through the Mini App.

Mitigation: Leave ENABLE_OPENCLAW_PROXY disabled unless needed and ensure any upstream control service has strong access control before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clvv/skills/openclaw-tg-canvas)
- [Publisher Profile](https://clawhub.ai/user/clvv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON/A2UI payloads, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can push canvas content through a CLI or HTTP endpoint and can expose a browser terminal for approved Telegram users.]

## Skill Version(s):

0.2.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
