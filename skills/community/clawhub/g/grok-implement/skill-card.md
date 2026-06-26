## Description: <br>
ClawPump V2 Token Launchpad helps agents launch real on-chain SPL tokens priced in CLAW via Meteora DBC, trade them, and track graduation to DAMM v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to guide Solana mainnet token launches, CLAW-quoted swaps, pool monitoring, and wallet-signing flows for ClawPump v2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may handle raw Solana wallet private keys while launching tokens or submitting swaps. <br>
Mitigation: Do not paste funded wallet private keys into an agent; use hardened secret handling and prefer user-controlled signing where possible. <br>
Risk: The skill can guide real Solana mainnet transactions with financial consequences. <br>
Mitigation: Require explicit review of every transaction, fee, address, token, pool, and amount before signing or broadcasting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/grok-implement) <br>
- [ClawPump v2 homepage](https://clawpump-v2.vercel.app) <br>
- [ClawPump v2 API base](https://clawpump-v2.vercel.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through real Solana mainnet launch, swap, and pool-state workflows; transaction details require user review before signing.] <br>

## Skill Version(s): <br>
0.7.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
