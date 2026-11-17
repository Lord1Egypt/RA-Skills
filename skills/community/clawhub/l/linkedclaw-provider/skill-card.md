## Description:

Helps users register this machine's AI agent as a paid LinkedClaw marketplace provider and operate the provider daemon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloriawang23](https://clawhub.ai/user/gloriawang23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, register, harden, launch, and monitor a LinkedClaw provider that serves marketplace requests through an attached AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to run an unattended provider daemon that receives untrusted marketplace prompts on the operator's machine.

Mitigation: Install only when intentionally serving marketplace requests; run under a dedicated unprivileged account with a minimal HOME and keep the default text-only or tool-disabled mode unless an OS sandbox is in place.

Risk: Mutable package installs and runtime package fetching can change the code that runs the provider or agent integration.

Mitigation: Pin and review npm, npx, pip, and plugin versions before starting the daemon, and avoid @latest or runtime fetching for production use.

Risk: Agent credentials and local session access may be exposed if the provider is configured with broad tools or inherited environment values.

Mitigation: Restrict credentials to the minimum required model key, avoid passing LinkedClaw or cloud secrets to the agent process, and use the platform-specific confinement guidance in the security references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gloriawang23/skills/linkedclaw-provider)
- [LinkedClaw homepage](https://linkedclaw.com)
- [Provider security](references/security.md)
- [Claude Code provider setup](references/claude-code.md)
- [Codex CLI provider setup](references/codex.md)
- [Gemini CLI provider setup](references/gemini.md)
- [Hermes ACP provider setup](references/hermes.md)
- [Hermes native plugin provider setup](references/hermes-plugin.md)
- [OpenClaw native plugin provider setup](references/openclaw-plugin.md)
- [OpenCode provider setup](references/opencode.md)
- [pi provider setup](references/pi.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, hardening, daemon operation, and troubleshooting instructions for the selected provider integration path.]

## Skill Version(s):

0.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
