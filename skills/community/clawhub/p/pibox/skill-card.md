## Description:

Install, configure, or run pi-coding-agent through the pibox wrapper, or connect to its HTTP, MCP, Telegram, or cron surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Pibox to run pi-coding-agent in a workspace, either interactively or through HTTP, OpenAI-compatible, MCP, Telegram, and scheduled interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance runs a remote installer directly and uses mutable container image tags, so the installed code may change or may not match a reviewed release.

Mitigation: Review the installer source and verify the image; pin installations to reviewed versions where possible.

Risk: API and MCP modes are unauthenticated when their respective tokens are unset, and host networking can expose those services beyond the local machine.

Mitigation: Set distinct API and MCP tokens and restrict network access by binding to loopback or placing the service behind an authenticating proxy.

## Reference(s):

- [Setup guide](references/setup.md)
- [Pibox repository](https://github.com/psyb0t/docker-pibox)
- [Pi coding agent](https://github.com/earendil-works/pi-mono/tree/main/packages/coding-agent)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/pibox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover interactive and one-shot use, plus optional service configuration.]

## Skill Version(s):

0.22.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
