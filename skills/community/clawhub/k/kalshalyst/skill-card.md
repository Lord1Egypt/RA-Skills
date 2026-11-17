## Description:

Kalshalyst helps agents scan Kalshi prediction markets for contrarian opportunities, estimate probability edge, track calibration, and size or optionally execute trades under configured controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and prediction market operators use Kalshalyst to identify potential mispricings on Kalshi, generate probability and edge analysis, monitor forecast calibration, and prepare or execute trades when they intentionally enable trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended auto-trading can place real-money Kalshi orders when configured and enabled.

Mitigation: Keep auto_trader_config.json disabled or run dry-run mode unless live trading is intentional; use daily loss, exposure, position, duplicate, and per-trade controls.

Risk: Credentials used by the skill can grant access to trading and paid API services.

Mitigation: Restrict credentials to the minimum needed, store them outside shared outputs, and review API cost exposure before scheduling frequent scans.

Risk: Persistent agent modification instructions can alter installed skill files.

Mitigation: Remove or ignore the Agent Bug-Fix Protocol before deployment and review any local file changes before reuse.

Risk: Market forecasts, edge estimates, and Kelly sizing can be wrong and may lead to losses.

Mitigation: Treat outputs as decision support, monitor calibration with Brier reports, cap position size, and require human review before increasing risk limits.

## Reference(s):

- [Kalshalyst Skill Page](https://clawhub.ai/kingmadellc/skills/kalshalyst)
- [README](README.md)
- [Blocklist Reference](references/blocklist.md)
- [Brier Score Tracking](references/brier-schema.md)
- [Contrarian Prompt](references/contrarian-prompt.md)
- [Kelly Criterion Math](references/kelly-math.md)
- [Kalshi](https://kalshi.com)
- [Anthropic Console](https://console.anthropic.com)
- [Polygon.io](https://polygon.io)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command snippets and JSON/YAML configuration examples; runtime scripts emit console text, JSON cache files, SQLite records, and CSV/JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Kalshi, Anthropic, Polygon, and optional local Ollama/Qwen; the auto-trading path can place live Kalshi orders when configured and enabled.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
