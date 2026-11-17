## Description:

Integrate Massive market data through Pontx. Use for bars, snapshots, ticker lookup, backtests, dashboards, entitlements, pagination, market-session time zones, throttling, or licensing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to integrate Massive market data through Pontx while handling entitlement checks, pagination, throttling, market-session time semantics, credential hygiene, and data-rights decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data credentials could be exposed through logs, command arguments, URLs, examples, or traces.

Mitigation: Keep API credentials scoped in environment variables and never print, persist, or include credential values in commands, URLs, examples, or traces.

Risk: Market data could be cached, exported, redistributed, or publicly displayed without the required rights.

Mitigation: Verify subscriber classification and written licensing rights before caching, exporting, selling, or publicly displaying market data.

Risk: Plan tier, entitlement, recency, or throttling assumptions could produce unavailable data or unreliable integrations.

Mitigation: Inspect the live Pontx/Massive contract, confirm plan coverage, preview requests, bound concurrency, and handle throttling with Retry-After or exponential backoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-massive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and code or configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Pontx CLI/API preview commands and integration guidance; data retrieval should follow explicit approval and credential-safety checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
