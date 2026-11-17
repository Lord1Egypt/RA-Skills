## Description:

Run MetaTrader 5 (MT5) fully headless on Linux/VPS with Wine, Xvfb, xdotool, and OCR to install MT5, log in, attach EAs, deploy experts, monitor heartbeat, and auto-restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operations engineers, and traders use this skill to run and maintain MetaTrader 5 expert advisors on Linux or VPS hosts without an interactive desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: System-level commands and broad process restarts can interrupt active MT5 trading sessions or detach expert advisors.

Mitigation: Review scripts before execution, test on demo or read-only accounts first, and replace broad process matching with PID- or service-scoped restart control before using it around live trading.

Risk: Screenshots and GUI automation can expose trading data, account details, or credentials if the wrong window or display is captured.

Mitigation: Run on an isolated VPS or dedicated account, verify the MT5 window focus before automation, and treat screenshot artifacts and temporary files as sensitive.

Risk: Declared Telegram network and credential access may be unnecessary for the included behavior.

Mitigation: Remove the Telegram permission and any related secrets unless explicit alerting is added and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/mt5-headless-automation)
- [Publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose system-level commands and scripts for Wine, Xvfb, MT5 automation, EA deployment, and heartbeat monitoring.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
