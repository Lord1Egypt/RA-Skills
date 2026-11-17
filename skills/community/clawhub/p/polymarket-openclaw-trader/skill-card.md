## Description:

Reusable Polymarket + OpenClaw trading operations skill for any workspace. Use when the user needs to set up, run, tune, monitor, and deploy an automated Polymarket trading project (paper/live), including env configuration, risk controls, reporting, and dashboard operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[08820048](https://clawhub.ai/user/08820048)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure, run, monitor, tune, and deploy a Polymarket trading workspace with paper or live execution, risk controls, reporting, and dashboard operations.

### Deployment Geography for Use:

Jurisdictions where Polymarket trading is legally permitted

## Known Risks and Mitigations:

Risk: The skill can guide agents through live financial trading operations with private-key configuration.

Mitigation: Use paper mode first, avoid heavily funding the configured wallet, and require explicit user approval before any live launch or restart.

Risk: Trading execution may be attempted from a restricted region.

Mitigation: Stop trading attempts when geoblock or region-restriction responses occur, state the compliance limitation, and do not provide bypass steps.

Risk: Deployment or automation commands may run with broad approval flags or unreviewed project code.

Mitigation: Review dependencies and cli_bot.py before running them, remove --yes from production deploys, and avoid committing secrets or unreviewed memory content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/08820048/skills/polymarket-openclaw-trader)
- [Publisher profile](https://clawhub.ai/user/08820048)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, restart commands, environment-variable guidance, and compliance warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
