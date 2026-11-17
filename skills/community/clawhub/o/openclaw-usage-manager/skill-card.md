## Description:

Monitors dual Claude Max accounts' 5-hour and 7-day usage, shows a local real-time dashboard, and can auto-switch the active OpenClaw account when utilization exceeds 80%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[takao-mochizuki](https://clawhub.ai/user/takao-mochizuki)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to monitor two Claude Max accounts, review utilization windows, and prepare or run account switching when one account reaches its configured usage threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Anthropic account tokens.

Mitigation: Use it only on a trusted single-user machine, prefer 1Password or another secrets manager, keep token files permission-restricted, and rotate any tokens used during testing.

Risk: The auto-switcher rewrites OpenClaw authentication state.

Mitigation: Review the checker behavior before enabling cron, confirm the target auth profile path, and enable automatic switching only after accepting that it can change the active authentication profile.

Risk: The dashboard launch flow and server behavior can terminate local processes on the configured port.

Mitigation: Remove or modify the port-killing alias and server behavior if other local services may use the same port.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/takao-mochizuki/skills/openclaw-usage-manager)
- [OpenClaw Usage Manager Setup Guide](https://github.com/Takao-Mochizuki/openclaw-usage-manager)
- [OpenClaw](https://openclaw.ai)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [Original Author Post](https://x.com/5dmgmt/status/2032770037728113118)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JavaScript code, JSON status output, and local dashboard configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and usage guidance for a localhost dashboard and an auto-switching checker that reads usage headers and updates OpenClaw authentication state.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
