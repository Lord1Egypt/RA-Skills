## Description: <br>
Pay-as-you-go Mobula API access for fetching crypto prices, wallet positions, and market data using a Tempo wallet that pays per call in USDC.e. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents pay-per-call access to Mobula crypto market data and wallet positions. It is intended for workflows where a user-controlled Tempo wallet funds small per-call API payments instead of using an API key or subscription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an encrypted hot wallet that can spend USDC.e for API calls. <br>
Mitigation: Keep only a small balance in the wallet and use an isolated user or workspace when possible. <br>
Risk: Every paid API call can trigger an irreversible on-chain payment. <br>
Mitigation: Rely on the built-in per-call cap and monitor wallet balance before enabling unattended use. <br>
Risk: A compromised host or dependency could expose wallet secrets in memory or on disk. <br>
Mitigation: Pin and review dependencies and treat the wallet as suitable only for limited funds. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flotapponnier/mobula-mpp) <br>
- [Publisher profile](https://clawhub.ai/user/flotapponnier) <br>
- [Agent-facing skill documentation](SKILL.md) <br>
- [Project README](README.md) <br>
- [Security model](SECURITY.md) <br>
- [Mobula MPP API endpoint](https://mpp.mobula.io) <br>
- [Tempo bridge](https://relay.link/bridge/tempo) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON API responses with Markdown setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Tempo USDC.e hot wallet for per-call payments and rejects payment challenges above the documented per-call cap.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
