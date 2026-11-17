## Description:

Monitors Polymarket positions, tracks profit and loss, sends portfolio alerts, enforces a daily-loss circuit breaker, and can trigger reinvestment helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-automation users can use this skill to monitor a Polymarket wallet, summarize open and resolved positions, receive alerts, and coordinate automated reinvestment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use wallet secrets and trigger automatic trading helper scripts that may spend funds without per-trade approval.

Mitigation: Review and supply the helper scripts yourself, use a dedicated low-balance wallet, pin dependencies, and confirm automatic trading behavior before enabling cron or daemon execution.

Risk: Secrets such as private keys and Telegram tokens may be loaded from the runtime environment or a .env file.

Mitigation: Do not use a main wallet private key, keep unrelated secrets out of the same .env file, and restrict file and process access on the host running the monitor.

Risk: The bundled monitor invokes unbundled scripts including auto_reinvest.py, weather_scanner.py, and exit_manager.py when present.

Mitigation: Inspect or replace those scripts before running the monitor, and verify spending limits and circuit-breaker behavior with small balances first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/themsquared/skills/polymarket-portfolio-tracker-v2)
- [Publisher profile](https://clawhub.ai/user/themsquared)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable monitoring alerts and writes local JSON state files when the provided script runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
