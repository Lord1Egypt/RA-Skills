## Description: <br>
Mpp Mobula lets agents fetch crypto prices, wallet positions, and market data through Mobula's pay-per-call MPP API using a funded Tempo wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill when they want an agent to retrieve Mobula crypto market data without a subscription or API key, while paying small USDC.e amounts per request from a controlled Tempo wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses a low-balance hot wallet to make paid API calls, so repeated requests can spend down available funds. <br>
Mitigation: Keep only a small balance in the wallet, monitor usage, and rely on the documented per-call spending cap for anomalous payment challenges. <br>
Risk: Wallet secrets on a shared or compromised machine could expose the funded wallet. <br>
Mitigation: Avoid running the skill on shared or untrusted machines and treat the wallet as a small-balance hot wallet. <br>
Risk: Dependency or source compromise could affect wallet-signing behavior. <br>
Mitigation: Review the source and the viem dependency before deployment, and pin or audit dependencies in managed environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flotapponnier/mpp-mobula) <br>
- [Mobula MPP API Base](https://mpp.mobula.io) <br>
- [Tempo RPC](https://rpc.tempo.xyz) <br>
- [Relay Tempo Bridge](https://relay.link/bridge/tempo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text and API responses from Mobula endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a funded Tempo hot wallet; each paid call spends the amount specified in the server payment challenge.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
