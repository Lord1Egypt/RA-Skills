## Description:

Use the openhook CLI to receive real-time events from external platforms and communicate with other agents through channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkantay](https://clawhub.ai/user/berkantay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate the OpenHook CLI for receiving webhook events from services such as GitHub, Stripe, Linear, Vercel, and Slack, and for coordinating multi-agent workflows through messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run an external CLI from a Homebrew tap.

Mitigation: Install only if the OpenHook project and tap are trusted, and verify the CLI source or version where possible.

Risk: API keys may be exposed through command history, scripts, logs, or screenshots.

Mitigation: Prefer a test or least-privilege API key and avoid placing live keys in commands, scripts, logs, or screenshots.

Risk: Webhook payloads and channel messages originate from external services and agents.

Mitigation: Treat incoming event payloads and messages as untrusted external data before using them in automated workflows.

Risk: The optional daemon can continue receiving or logging event data after active use.

Mitigation: Check daemon status and stop it when it is not needed.

## Reference(s):

- [OpenHook website](https://openhook.dev)
- [OpenHook dashboard](https://openhook.dev/dashboard)
- [OpenHook API key settings](https://openhook.dev/settings)
- [OpenHook CLI GitHub repository](https://github.com/openhook-dev/openhook-cli)
- [ClawHub skill page](https://clawhub.ai/berkantay/skills/openhook-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for installation, authentication, event subscriptions, daemon management, and channel messaging.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
