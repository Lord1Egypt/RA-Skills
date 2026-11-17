## Description:

Automates Kalshi prediction-market scanning, research, trade execution, position tracking, and daily portfolio reporting for configured user accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobthemom987](https://clawhub.ai/user/bobthemom987)

### License/Terms of Use:

MIT-0

## Use Case:

External users who trade Kalshi prediction markets use this skill to configure an automated bot that scans markets, evaluates opportunities, places orders, monitors positions, and reports portfolio status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable unattended real-money trading with local Kalshi credentials and limited user control.

Mitigation: Use a dedicated low-permission Kalshi key, test in a sandbox or dry-run mode before enabling cron, and require clear approvals for order execution.

Risk: Automated trading can create financial exposure if research, sizing, logging, or shutdown controls are incomplete.

Mitigation: Set hard exposure and loss limits, keep research separate from order execution, configure logging, and define an emergency shutdown process before deployment.

## Reference(s):

- [Kalshi API Reference](references/api.md)
- [Cron Prompt for 15-Minute Scan](references/cron-prompt.md)
- [Trade Research Workflow](references/trade-research.md)
- [Kalshi Trader ClawHub Page](https://clawhub.ai/bobthemom987/skills/kalshi-trader)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance, cron prompt text, API usage notes, trading criteria, and portfolio reporting format.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
