## Description:

Autonomous but risk-bounded paper-trading options agent spec for the Perfect Storm strategy, covering OpenClaw setup, Alpaca paper execution constraints, liquid long call/put selection, conservative sizing, daily risk controls, and auditable trade decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[essam9009](https://clawhub.ai/user/essam9009)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-system operators use this skill to configure or evaluate an OpenClaw paper-trading options agent that scans an approved universe, scores PS+/PS- setups, selects liquid contracts, sizes positions conservatively, and journals each decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An autonomous agent may receive broker credentials and order authority while the paper-only boundary is ambiguous.

Mitigation: Use only paper Alpaca credentials and enforce the exact origin https://paper-api.alpaca.markets before every authenticated request.

Risk: A live-trading toggle or confirmation bypass could weaken the intended paper-trading boundary.

Mitigation: Remove live-trading toggles and confirmation bypasses before installation or execution.

Risk: Skipped, rejected, or failed symbols may be lost from the audit trail if decision states are not aligned.

Mitigation: Align decision states and log every skipped or rejected symbol consistently, including blockers and journal notes.

Risk: Options execution can amplify losses when data, spreads, or broker state are stale or uncertain.

Mitigation: Keep the configured halts for stale data, abnormal spread expansion, broker uncertainty, daily loss limits, weekly loss limits, portfolio heat, and consecutive losses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/essam9009/skills/perfect-storm-options-trader-v2)
- [AGENTS.md strategy rulebook](artifact/AGENTS.md)
- [OpenClaw best-practices risk configuration](artifact/risk_config_openclaw_best_practices.yaml)
- [Alpaca paper API endpoint](https://paper-api.alpaca.markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON trade-decision objects and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade decisions include action, symbol, direction, setup type, confidence score, regime, thesis, contract candidate, entry plan, stop plan, target plan, position size, risk checks, blockers, and journal note.]

## Skill Version(s):

2.0.0 (source: artifact/SKILL.md frontmatter; server release version: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
