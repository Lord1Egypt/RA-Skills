## Description: <br>
Access Monarch Money financial data: accounts, transactions, budgets, and cashflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silentknight87](https://clawhub.ai/user/silentknight87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Monarch Money accounts, transactions, budgets, and cashflow, or to request a refresh of linked financial accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive financial account data and stores a reusable Monarch Money session locally. <br>
Mitigation: Install only on a trusted machine, protect ~/.monarchmoney/mm_session.pickle, avoid syncing it to untrusted storage, and delete it when no longer needed. <br>
Risk: The refresh command can request synchronization for all linked financial institutions. <br>
Mitigation: Run refresh only when the user intentionally wants linked accounts synced. <br>
Risk: Authentication depends on the third-party monarchmoney Python package. <br>
Mitigation: Review the monarchmoney package before entering Monarch credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silentknight87/monarch) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON from CLI commands, with Markdown setup and usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the monarchmoney Python package, and a local Monarch Money session saved at ~/.monarchmoney/mm_session.pickle.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
