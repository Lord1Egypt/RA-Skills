## Description:

Use the local kalshi CLI for bounded Kalshi series and market research, keyword discovery, fixed-point portfolio and candlestick reads, order reconciliation, and explicitly confirmed demo or production order operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobashopcashier](https://clawhub.ai/user/bobashopcashier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a local Kalshi CLI for bounded market research, portfolio reads, order reconciliation, and explicitly confirmed demo or production order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kalshi API private keys or credential file paths could be exposed if credentials are placed in command arguments, logs, prompts, or outputs.

Mitigation: Use protected credential files or environment variables that point to files, keep credential and PEM files at mode 0600 or stricter, and avoid putting private keys in argv, params, logs, or prompts.

Risk: Order creation or cancellation could trigger unintended trading activity, especially in production.

Mitigation: Prefer demo mode unless production is explicitly requested, require dry-run review with policy caps, and execute real writes only with the matching confirmation digest.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance emphasizes compact JSON, bounded reads, field requirements, dry-run review, and explicit confirmation for writes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
