## Description:

Agent skill that reproduces Hummingbot CLI commands through the Hummingbot API for core V2 trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to connect an agent to Hummingbot API workflows for exchange credentials, balances, bot configuration, V2 bot lifecycle management, status, history, and direct trade operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect to real exchange accounts and includes direct order placement workflows that could affect funds.

Mitigation: Use paper trading or testnet first, disable withdrawals on exchange API keys, and remove or avoid scripts/trade.py when direct orders are not intended.

Risk: Weak credential or API configuration could expose a Hummingbot API connection to unintended use.

Mitigation: Set an explicit trusted local or HTTPS Hummingbot API URL, avoid passing secrets on the command line, and replace any default admin/admin credentials before use.

## Reference(s):

- [PMM Mister Controller](references/pmm_mister.md)
- [PMM V1 Controller](references/pmm_v1.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and plain text tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include trading account operations, bot lifecycle actions, balances, history, market data, and order-related guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
