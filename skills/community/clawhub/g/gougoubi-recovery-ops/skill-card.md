## Description: <br>
Detect and repair partial failures in Gougoubi PBFT operations, including missing activation, missing risk LP, missing results, and pending reward claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill after a Gougoubi batch workflow partly succeeds to scan a proposal, classify missing work, and repair only the requested activation, risk LP, result submission, or reward-claim gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive high-impact crypto repair transactions, including activation, risk LP, result submission, and reward claiming. <br>
Mitigation: Confirm the proposal address, wallet or profile, network, contract addresses, repair class, transaction value, gas, and explicit user approval before each transaction. <br>
Risk: The skill depends on project recovery scripts that are referenced but not bundled in the artifact. <br>
Mitigation: Inspect the local Gougoubi project checkout and confirm the referenced scripts exist and match the intended recovery flow before running repairs. <br>
Risk: A broad repair request could affect healthy conditions if scope is not controlled. <br>
Mitigation: Use the scan results to build the smallest possible repair plan and do not rerun healthy conditions or widen beyond the requested repair set. <br>


## Reference(s): <br>
- [Gougoubi project repository](https://github.com/gougoubi/gougoubi) <br>
- [Gougoubi website](https://gougoubi.ai) <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-recovery-ops) <br>
- [Publisher profile](https://clawhub.ai/user/chinasong) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON final report with transaction hashes, failures, and warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill keeps detection counts separate from repaired counts and returns a retryable failure object when scanning, repair, or confirmation fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact clawhub.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
