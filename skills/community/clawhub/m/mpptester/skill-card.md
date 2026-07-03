## Description: <br>
Runs a Machine Payments Protocol conformance test that verifies an agent or wallet can complete a $0.50 USDC payment on Solana and produce a shareable proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kris-hansen](https://clawhub.ai/user/kris-hansen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to verify Machine Payments Protocol payment integrations by starting a Solana USDC send or receive test and obtaining a shareable proof after on-chain confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward a real mainnet USDC payment path. <br>
Mitigation: Use devnet by default, require manual confirmation before any mainnet transaction, and use a dedicated wallet with limited funds. <br>
Risk: Autonomous execution could sign or send payments without sufficiently clear spend caps or irreversibility warnings. <br>
Mitigation: Avoid autonomous mainnet execution until spending limits and irreversible transaction warnings are explicit and enforced. <br>


## Reference(s): <br>
- [MPP Tester homepage](https://mpptester.com) <br>
- [ClawHub skill page](https://clawhub.ai/kris-hansen/mpptester) <br>
- [Solana Pay documentation](https://docs.solanapay.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API examples, payment URLs, status text, and receipt links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate real or test Solana USDC payment flows depending on the selected network.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
