## Description: <br>
Read and manage Kubera.com portfolio data, including net worth, assets, debts, allocation, and holdings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BYWallace](https://clawhub.ai/user/BYWallace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query Kubera portfolios, review net worth, holdings, allocation, assets, and debts, and update asset or debt values when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive financial portfolio data. <br>
Mitigation: Use read-only Kubera API keys when possible, keep credentials private, and run commands only for explicit user requests. <br>
Risk: The skill can update Kubera asset or debt records when write-enabled credentials are used. <br>
Mitigation: Use write credentials only when needed; review update commands before execution and require the documented --confirm flag. <br>
Risk: Repeated portfolio queries can hit Kubera API rate limits. <br>
Mitigation: Cache full JSON output when running multiple queries in a session and stay within the documented request limits. <br>


## Reference(s): <br>
- [Kubera API Reference (V3)](references/api.md) <br>
- [Kubera](https://www.kubera.com) <br>
- [Kubera API Base URL](https://api.kubera.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI text and JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kubera API credentials; update operations require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
