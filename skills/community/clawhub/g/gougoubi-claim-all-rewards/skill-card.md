## Description: <br>
Claim all Gougoubi rewards for one or more addresses, including winner rewards, governance rewards, and LP rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to claim winner, governance, and LP rewards for one or more Gougoubi addresses through a profile, quick, or full-scan claim path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct live on-chain reward-claim transactions through scripts that are not included or fully scoped in the package. <br>
Mitigation: Require a dry run first, then review the exact network, addresses, signer, gas estimate, transaction details, and wallet approval before any claim is submitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-claim-all-rewards) <br>
- [Publisher profile](https://clawhub.ai/user/chinasong) <br>
- [Gougoubi website](https://gougoubi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON with concise procedural guidance and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes claim method, addresses, per-address reward status, transaction hashes, warnings, and retryable failure details when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
