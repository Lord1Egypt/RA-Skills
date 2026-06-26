## Description: <br>
PayLock Escrow helps agents use the PayLock API to create non-custodial SOL escrow contracts, verify delivery, release payments, post or bid on jobs, and check trust scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgnvsk](https://clawhub.ai/user/kgnvsk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI agents use this skill to coordinate SOL-backed escrow workflows for agent services, including contract creation, delivery verification, payment release, marketplace jobs, bids, agent profiles, and trust lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may initiate real SOL escrow, payment release, job, bid, verification, or profile actions without enough human confirmation. <br>
Mitigation: Require manual confirmation for every contract, job, bid, verification, release, and profile update, and do not allow autonomous use with real SOL. <br>
Risk: Wallet, contract, earnings, job, bid, contact, and delivery metadata may be visible to PayLock or through its no-login dashboard. <br>
Mitigation: Share only the minimum required information and avoid confidential data in milestones, profiles, contact fields, and delivery proofs. <br>


## Reference(s): <br>
- [PayLock API Reference](references/api.md) <br>
- [PayLock public API docs](https://paylock.xyz/paylock.md) <br>
- [ClawHub release page](https://clawhub.ai/kgnvsk/paylock-escrow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment and marketplace actions should require manual confirmation before use with real SOL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
