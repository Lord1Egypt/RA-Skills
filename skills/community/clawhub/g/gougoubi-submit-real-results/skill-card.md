## Description: <br>
Submit real-world outcomes for Gougoubi conditions using deterministic evidence from condition skills and public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to map public evidence to Gougoubi condition results and submit one result per condition. It supports resolved-only settlement, full result submission, and explicit forced fallback handling for pending conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real on-chain state changes through project-local scripts that are not included in the release artifact. <br>
Mitigation: Inspect the referenced project scripts, run help or dry-run modes first, and confirm the proposal, chain, wallet, signer, gas cost, and evidence mapping before any real submission. <br>
Risk: Forced fallback mode can submit a result for conditions that are not officially resolved. <br>
Mitigation: Prefer resolved-only mode, use force mode only after explicit user confirmation, and keep evidence mapping with every submitted transaction result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-submit-real-results) <br>
- [Gougoubi website](https://gougoubi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON with submitted, skipped, failed, warning, and transaction-hash fields; may include shell command guidance for project script entry points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs preserve the proposal address, selected mode, evidence mapping, result status, and transaction hashes when submissions occur.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
