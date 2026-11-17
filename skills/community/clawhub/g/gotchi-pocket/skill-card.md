## Description:

Manage Aavegotchi pocket wallets (escrow) on Base with Bankr. Use when the user wants to deposit ERC20 tokens into a gotchi pocket, withdraw ERC20 tokens from a pocket, check pocket balances/ownership by gotchi ID, or issue plain-English pocket commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Aavegotchi pocket ownership and balances, then deposit or withdraw ERC20 tokens on Base through Bankr-mediated transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial transactions and can submit deposits or withdrawals through Bankr.

Mitigation: Review every transaction request, amount, token, gotchi ID, and destination address before execution; use dry-run parsing for natural-language commands when possible.

Risk: Bankr credential and endpoint handling are security-sensitive.

Mitigation: Protect and rotate BANKR_API_KEY, keep BANKR_API_URL unset unless intentionally testing, and avoid runtimes where untrusted agents or wrappers can control environment variables.

Risk: Natural-language wallet commands can be misparsed or routed to an unintended action.

Mitigation: Use explicit script arguments for high-value transfers and require the built-in withdraw approval path before executing natural-language withdrawal intents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/gotchi-pocket)
- [Skill homepage](https://github.com/aavegotchi/aavegotchi-agent-skills)
- [Publisher profile](https://clawhub.ai/user/aaigotchi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and key-value command output, with transaction hashes and explorer URLs for submitted transactions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cast, jq, curl, python3, and BANKR_API_KEY; commands operate on Base and supported ERC20 token aliases or token addresses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
