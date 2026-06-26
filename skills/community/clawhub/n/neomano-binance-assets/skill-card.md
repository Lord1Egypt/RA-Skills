## Description: <br>
Safe, read-only Binance balance viewer (Spot wallet) using Binance API keys with READ-ONLY permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with read-only Binance API credentials use this skill to list Spot wallet balances and check holdings without placing trades, transfers, or withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Binance API credentials that can read Spot account balances. <br>
Mitigation: Use a Binance API key with reading only, keep trading and withdrawals disabled, and consider an IP allowlist. <br>
Risk: The printed asset list can reveal private financial holdings. <br>
Mitigation: Treat the output as private financial information and avoid sharing logs or terminal output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-binance-assets) <br>
- [Binance Spot account endpoint](https://api.binance.com/api/v3/account) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON printed to stdout, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters to non-zero Spot balances by default; --all includes zero balances and --min sets a minimum displayed total.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
