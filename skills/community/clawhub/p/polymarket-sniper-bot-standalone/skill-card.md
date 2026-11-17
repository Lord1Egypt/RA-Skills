## Description:

An autonomous trading agent for Polymarket on Polygon that scans 15-minute markets for momentum, supports dashboard monitoring, and can run in simulation or live execution modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjs829](https://clawhub.ai/user/wjs829)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading operators use this agent to configure automated Polymarket market scans, monitor activity through a dashboard, and optionally execute live orders on Polygon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can spend real funds from a configured Polymarket wallet.

Mitigation: Start in simulation mode, use only a burner wallet with limited funds, and verify the executed code path before enabling live trading.

Risk: The dashboard may expose trading status and logs if it is bound to a public interface.

Mitigation: Bind the dashboard to localhost, restrict network access, or add authentication before running it on a server.

Risk: A fabricated momentum fallback can produce buy signals when live market data is unavailable.

Mitigation: Remove the fallback or require confirmed live market data before allowing order placement.

Risk: License validation environment variables can send license keys to a configured validation service.

Mitigation: Set PRO_LICENSE_KEY or LICENSE_SERVER only when the validation service is trusted and understood.

Risk: Unpinned dependencies and system-level package installation can make deployments harder to reproduce.

Mitigation: Install in a virtual environment and pin dependency versions before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wjs829/skills/polymarket-sniper-bot-standalone)
- [Publisher Profile](https://clawhub.ai/user/wjs829)
- [Project Website](https://github.com/wjs829/polymarket-sniper-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code references, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide setup, configuration, dashboard operation, market scanning, simulation, and live trading workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
