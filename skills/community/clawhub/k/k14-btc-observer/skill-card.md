## Description:

Run the complete BTC K14 strategy in paper mode with dynamic exits, a persistent ledger and a separate Simmer virtual SIM execution mirror.

This skill is for research and development only.

## Publisher:

[l337-krew-cs](https://clawhub.ai/user/l337-krew-cs)

### License/Terms of Use:

Custom proprietary terms (all rights reserved)

## Use Case:

Developers and strategy researchers use the skill to run a bounded BTC K14 paper strategy, inspect its modeled ledger, and compare it with separate virtual SIM receipts. It supports evaluation and deployment testing, not claims of real trading performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs may continue longer than intended or the published automation manifest may not reflect an active hosted run.

Mitigation: Review the schedule before enabling it, retrieve the actual run report, and create STOP in the state directory to halt activity.

Risk: An exposed API key or concurrent runs using separate state can compromise or desynchronize virtual account activity.

Mitigation: Supply SIMMER_API_KEY through secret configuration, protect and reuse one persistent state directory, and run only one instance per key.

Risk: Hypothetical fills and virtual SIM receipts may be mistaken for real execution or profit evidence.

Mitigation: Keep the model ledger, virtual SIM ledger, and connection-test transactions separate; treat all results as simulations.

Risk: The bundled thresholds expire after October 2026 and may no longer be valid for new signals.

Mitigation: Check that thresholds are valid for the current UTC month before running; missing or expired thresholds should block new signals.

## Reference(s):

- [BTC K14 Paper Trader on ClawHub](https://clawhub.ai/l337-krew-cs/skills/k14-btc-observer)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands]

**Output Format:** [JSON status reports and virtual trade receipts, SQLite ledgers, and a shell command interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent state across runs; paper-model results and virtual SIM receipts are recorded separately.]

## Skill Version(s):

0.2.0 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
