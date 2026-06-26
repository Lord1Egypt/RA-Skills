## Description: <br>
Discover NEAR airdrops, check eligibility, claim rewards, and track claimed airdrops across multiple platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to find NEAR ecosystem airdrop links, record manual eligibility checks, and track claim status for accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate automated eligibility-checking and claiming capabilities. <br>
Mitigation: Treat output as links and notes only; verify eligibility and claim status directly with the relevant protocol before acting. <br>
Risk: The local claimed list can record a claim attempt even when no on-chain or protocol claim has completed. <br>
Mitigation: Confirm successful claims independently in the wallet, protocol UI, or trusted transaction records. <br>
Risk: Airdrop claim links may require wallet connection or transaction signing on third-party sites. <br>
Mitigation: Inspect each URL and transaction request before connecting a wallet or signing. <br>


## Reference(s): <br>
- [NEAR Ecosystem](https://near.org/ecosystem/) <br>
- [NEAR Airdrops](https://near.org/airdrops/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [CLI text output with URLs and local JSON tracking data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local tracking data to ~/.near-airdrop/tracking.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
