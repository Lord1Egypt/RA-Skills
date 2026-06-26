## Description: <br>
Interact with XPR Network on-chain governance: view communities, proposals, vote with weighted tokens, and create proposals paying community fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect XPR Network governance communities, proposals, vote records, and global governance configuration. With explicit confirmation and XPR signing credentials, it can cast governance votes or create proposals that pay the required community fee. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed write operations can sign XPR governance votes and proposal transactions, including fee-paying proposal creation. <br>
Mitigation: Review transaction details before setting confirmed=true, and use a limited XPR account instead of a main wallet where possible. <br>
Risk: The security review flagged under-disclosed private-key environment variables for write operations. <br>
Mitigation: Install only after review, keep XPR private keys out of shared environments, and use read-only tools when signing is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/governance) <br>
- [XPR Governance website](https://gov.xprnetwork.org) <br>
- [XPR Governance proposal API](https://gov.api.xprnetwork.org/api/v1/proposals) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [Tool responses with governance data and transaction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only tools query public governance data; write tools require confirmed=true and configured XPR signing credentials.] <br>

## Skill Version(s): <br>
0.2.11 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
