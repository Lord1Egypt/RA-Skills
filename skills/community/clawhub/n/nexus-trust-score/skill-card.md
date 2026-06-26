## Description: <br>
Generate on-chain trust scores for wallets and agents using Masumi transaction data on Cardano. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to request wallet or agent trust scoring from the NEXUS remote service when evaluating on-chain reputation signals. It is most relevant for Cardano, Stellar, and XRP Ledger payment-aware agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid remote payment flows may incur charges or initiate transaction-related activity without clear per-call consent or spending limits. <br>
Mitigation: Require explicit approval before each paid call or transaction, set spending limits outside the skill, and test with sandbox_test before using live payment credentials. <br>
Risk: Wallet, agent trust-score requests, payment proofs, and payment metadata are sent to a third-party remote service. <br>
Mitigation: Install only when the operator trusts NEXUS for this data, send the minimum necessary input, and avoid broad signing authority or reusable payment proofs. <br>


## Reference(s): <br>
- [NEXUS Trust Score on ClawHub](https://clawhub.ai/cyberforexblockchain/nexus-trust-score) <br>
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host) <br>
- [NEXUS Trust Score API](https://ai-service-hub-15.emergent.host/api/original-services/trust-score) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stellar Payment Information](https://ai-service-hub-15.emergent.host/api/mpp/stellar) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON service response or text summary returned by the remote NEXUS API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment proof or payment credential for paid calls; sandbox testing is documented with sandbox_test.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
