## Description: <br>
Access Coinbase API to fetch balances, get EUR trading pairs, create market or limit crypto orders, and view order history and fills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtrab](https://clawhub.ai/user/mtrab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to let an agent inspect Coinbase account data, discover EUR trading products, and submit Coinbase market or limit orders through configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Coinbase crypto orders using local credentials without built-in confirmations or limits. <br>
Mitigation: Require human approval before every order and test with minimal funds or a sandbox or paper setup where possible. <br>
Risk: The skill depends on sensitive Coinbase API key and private key files stored near the script. <br>
Mitigation: Use least-privilege credentials, restrict file permissions, and avoid committing or sharing key files. <br>


## Reference(s): <br>
- [ClawHub Coinbase release](https://clawhub.ai/mtrab/openclaw-coinbase) <br>
- [Coinbase Developer Platform](https://portal.cdp.coinbase.com) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Python functions with Markdown usage examples and shell dependency commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Coinbase API key and private key files; API calls return Coinbase account, product, order, and fill data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
