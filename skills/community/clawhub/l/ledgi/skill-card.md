## Description:

Interact with a user's Ledgi personal finance data for accounts, balances, net worth, holdings, investments, ISA allowances, pensions, snapshots, and financial record updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelsongallardo](https://clawhub.ai/user/nelsongallardo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent read and maintain their Ledgi personal finance records, including accounts, holdings, net worth snapshots, and ISA deposits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a remote curl-to-bash installation flow for the Ledgi CLI.

Mitigation: Install the Ledgi CLI through a pinned, verifiable release instead of running the remote installation script directly.

Risk: API keys and personal financial data could be exposed through command lines or shared logs.

Mitigation: Use the narrowest available API scopes, prefer environment or login-based credentials, and avoid placing API keys in command arguments or shared logs.

Risk: Write commands can create or update persistent financial records such as accounts, holdings, snapshots, and ISA deposits.

Mitigation: Require confirmation of the exact write action and target data before running modification commands, and use external identifiers for idempotent account and holding upserts.

## Reference(s):

- [Ledgi Skill Page](https://clawhub.ai/nelsongallardo/skills/ledgi)
- [Ledgi Publisher Profile](https://clawhub.ai/user/nelsongallardo)
- [Ledgi CLI Command Reference](artifact/commands.md)
- [JSON Schemas for Bulk Operations](artifact/schemas.md)
- [Ledgi CLI Install Script](https://raw.githubusercontent.com/LedgiApp/ledgi-cli/main/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text summaries with Ledgi CLI commands and JSON configuration files for bulk operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON by default; table output is recommended when presenting results to users.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
