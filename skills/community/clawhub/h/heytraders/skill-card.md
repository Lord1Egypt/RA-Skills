## Description:

Operates HeyTraders through its live browser command catalog to inspect, navigate, configure, and manage the application.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heytraders](https://clawhub.ai/user/heytraders)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to inspect and manage HeyTraders, guide exchange onboarding, and review or share completed backtests through the HeyTraders plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading actions, wallet approvals, deposits, and strategy starts can have significant financial consequences.

Mitigation: Require explicit operator approval for each action and verify the resulting state before reporting success.

Risk: Credentials or wallet secrets may be exposed if entered in chat or tool arguments.

Mitigation: Use only the secure browser or venue surface specified by the live guide; never pass secrets in chat or CLI arguments.

Risk: Anyone with an unlisted backtest share URL can view the report.

Mitigation: Share the link only with the intended operator; revoke future access when requested.

Risk: The skill requires browser access through the HeyTraders OpenClaw plugin.

Mitigation: Confirm the operator intends to install and enable the plugin and grant access to the managed browser session.

## Reference(s):

- [HeyTraders skill release](https://clawhub.ai/heytraders/skills/heytraders)
- [HeyTraders OpenClaw plugin installation guide](https://github.com/heytraders/HeyTraders-OpenClaw/blob/main/README.md#install-in-an-existing-openclaw-environment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown text with links and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Completed backtest reports may include an unlisted, read-only share link.]

## Skill Version(s):

2.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
