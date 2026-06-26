## Description: <br>
Create blockchain wallets and sign transactions using Para's MPC infrastructure where the private key never exists in a single place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adeets-22](https://clawhub.ai/user/adeets-22) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to teach agents how to create Para MPC wallets, check wallet readiness, and request signatures for EVM and Solana workflows through Para's REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can request wallet signatures for blockchain transactions or messages with financial impact. <br>
Mitigation: Use beta or test environments first and require explicit human approval after decoding and checking every sign-raw payload. <br>
Risk: PARA_API_KEY enables access to Para wallet API operations. <br>
Mitigation: Store PARA_API_KEY as a secret and expose it only to approved agent runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adeets-22/para-wallet) <br>
- [Para Developer Portal](https://developer.getpara.com) <br>
- [Para Website](https://getpara.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint descriptions, JSON request and response examples, and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARA_API_KEY and human review before signing blockchain data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
