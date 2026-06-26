## Description: <br>
OpenClaw skill for requesting NEAR testnet tokens via faucet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to request NEAR testnet tokens and check testnet account balances from an agent workflow or command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NEAR testnet account IDs entered into the skill are sent to NEAR testnet services. <br>
Mitigation: Use only testnet account identifiers and avoid entering sensitive production account information. <br>
Risk: The release documentation advertises status tracking, default account configuration, and local rate limiting that the artifact does not implement. <br>
Mitigation: Treat request and balance commands as the supported behavior for this version, and independently track rate limits or request status when needed. <br>


## Reference(s): <br>
- [NEAR Testnet Faucet](https://wallet.testnet.near.org/) <br>
- [NEAR CLI Documentation](https://docs.near.org/tools/near-cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/shaiss/near-faucet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NEAR testnet account identifiers supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
