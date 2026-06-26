## Description: <br>
Manage NEAR Name Service (.near domains) - check availability, register, resolve, and manage names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NEAR users use this skill to check .near domain availability, register names, resolve names to account IDs, and manage names from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration builds shell commands from user-provided name and account values. <br>
Mitigation: Review commands before execution, avoid untrusted names or account IDs, and replace shell-string execution with safe argument passing before using funded accounts. <br>
Risk: Registration is a transaction-capable flow that can spend NEAR. <br>
Mitigation: Verify the network, cost, account, and domain before approving any NEAR signing prompt. <br>


## Reference(s): <br>
- [NEAR Name Service](https://near.org/names/) <br>
- [NEAR CLI](https://docs.near.org/tools/near-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with shell command examples and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NEAR RPC endpoints and NEAR CLI for network queries and registration transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
