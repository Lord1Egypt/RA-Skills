## Description:

Scan Polymarket markets for a configurable thesis, compare your probability to the market price, and trade only when the edge clears a safety threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external operators can use this skill as an automated Polymarket trading template that scans markets, compares current prices against a user-supplied fair probability, and reports or submits trades when the configured edge threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled live mode can repeatedly place real-money trades without built-in exposure limits.

Mitigation: Keep the skill in dry-run until account-level spending limits, position checks, order deduplication, cooldowns, and pinned dependencies are added or enforced.

Risk: A shared or inherited RUN_LIVE setting could enable live execution unexpectedly.

Mitigation: Avoid setting RUN_LIVE in shared environments and require deliberate live execution controls for production use.

Risk: The AION_API_KEY can authorize market reads and trade execution.

Mitigation: Use a restricted API key scoped to the minimum permissions and environment needed for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fivegive249-ship-it/skills/polymarket-thesis-trader)
- [Publisher profile](https://clawhub.ai/user/fivegive249-ship-it)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI summaries with configuration-driven execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AION_API_KEY; dry-run mode is the default unless live execution is explicitly enabled.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
