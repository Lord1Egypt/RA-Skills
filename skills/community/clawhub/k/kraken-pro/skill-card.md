## Description: <br>
Manage Kraken accounts through a Python CLI for portfolio views, market data, trading, earn and staking actions, ledger export, deposits, and withdrawals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in-liberty420](https://clawhub.ai/user/in-liberty420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage a Kraken account from the command line. It supports read-only account review and market data, plus user-confirmed account actions such as orders, staking allocation, and withdrawals when credentials permit them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real financial actions if granted Kraken API credentials with trading, staking, or withdrawal permissions. <br>
Mitigation: Use a dedicated least-privilege Kraken API key, start with read-only permissions, and add trading or withdrawal permissions only when required. <br>
Risk: Confirmed commands may place orders, allocate or deallocate earn positions, cancel orders, or withdraw funds. <br>
Mitigation: Review the exact asset, pair, amount, price, strategy, and withdrawal key before allowing any command that uses --confirm; use --validate for trading dry runs when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/in-liberty420/kraken-pro) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/in-liberty420) <br>
- [Kraken API Key Setup](https://www.kraken.com/u/security/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [CLI text, Markdown command guidance, CSV exports, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and python-kraken-sdk; authenticated account actions require KRAKEN_API_KEY and KRAKEN_API_SECRET.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
