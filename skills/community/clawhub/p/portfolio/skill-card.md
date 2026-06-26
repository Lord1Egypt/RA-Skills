## Description: <br>
Manage investment portfolios by recording positions, analyzing allocation, calculating returns, and generating rebalance suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users managing local investment records use this skill to add or remove holdings, review allocation and performance, and draft rebalance suggestions from stored transaction data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and transaction history are stored in plaintext on the user's machine. <br>
Mitigation: Protect ~/.portfolio on shared or backed-up systems and keep controlled backups if the records matter. <br>
Risk: Rebalance and performance output can affect financial decisions if accepted without review. <br>
Mitigation: Verify calculations and assumptions before making real trades or other investment decisions. <br>


## Reference(s): <br>
- [ClawHub Portfolio Skill](https://clawhub.ai/bytesagain1/portfolio) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Terminal text, tables, JSON, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores holdings and transaction records as local JSON files under ~/.portfolio.] <br>

## Skill Version(s): <br>
3.4.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
