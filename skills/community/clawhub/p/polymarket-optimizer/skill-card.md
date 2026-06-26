## Description: <br>
Automatic parameter optimizer for polymarket-executor that reads performance data, adjusts learned_config.json, builds paper-trade metrics, and assesses live trading readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to tune a Polymarket executor from paper-trading and portfolio performance data. It is intended to update strategy thresholds, allocations, Kelly fraction, scan cadence, logs, and readiness reports for future executor runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optimizer can automatically change future Polymarket executor behavior by updating trading thresholds, allocations, Kelly fraction, and scan cadence. <br>
Mitigation: Use paper mode first, back up learned_config.json, and review optimizer_log.jsonl before allowing changes to affect live trading. <br>
Risk: The setup guidance includes root service execution and shared environment-file usage, which can expand privilege and secret exposure. <br>
Mitigation: Run under a non-root service account with a minimal dedicated credentials file, and disable Telegram reporting if the bot token and chat ID are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/polymarket-optimizer) <br>
- [Source repository](https://github.com/georges91560/polymarket-optimizer) <br>
- [Configuration guide](CONFIGURATION.md) <br>
- [Systemd setup guide](SYSTEMD_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON configuration files, JSONL logs, console text, and optional Telegram report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes learned_config.json and optimizer_log.jsonl in the configured workspace when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
