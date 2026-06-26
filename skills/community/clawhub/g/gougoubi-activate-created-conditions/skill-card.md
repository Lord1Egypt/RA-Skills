## Description: <br>
Activate all CREATED conditions under a Gougoubi proposal with deterministic committee checks, optional auto-stake joining, and structured voting results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent validate a Gougoubi BSC proposal, join the committee by minimum stake when explicitly approved, and vote to activate all CREATED conditions while returning structured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can stake funds and submit governance votes on BSC. <br>
Mitigation: Require a dry run, review every transaction, confirm the staking amount and asset, and require separate explicit approval before staking or voting. <br>
Risk: Voting may continue after an individual condition fails, producing partial activation results. <br>
Mitigation: Review the returned successes, failures, warnings, and next actions before treating the proposal activation as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-activate-created-conditions) <br>
- [Contract methods reference](references/CONTRACT_METHODS.md) <br>
- [Gougoubi website](https://gougoubi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [structured JSON, guidance] <br>
**Output Format:** [JSON object with success, failure, warning, and next action fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes transaction hashes, per-condition success and failure details, and retryable failure stages when applicable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
