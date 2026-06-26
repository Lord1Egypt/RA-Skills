## Description: <br>
Orchestrates end-to-end Gougoubi market operations by routing high-level market requests to the appropriate downstream skill for creation, activation, liquidity staking, result submission, reward claiming, or recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn high-level Gougoubi PBFT market requests into an auditable choice of the smallest downstream workflow skill and a compact operation summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route an agent toward high-impact Gougoubi market actions such as staking liquidity, submitting results, or claiming rewards without built-in confirmation rules. <br>
Mitigation: Require manual approval before any downstream skill changes market state, stakes liquidity, submits official results, or claims rewards. <br>
Risk: A routing error could select the wrong downstream workflow stage for a market operation. <br>
Mitigation: Review the selected skill, reason, stage, inputs, outcome, and recommended next action before executing the chosen downstream skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-market-orchestrator) <br>
- [Gougoubi website](https://gougoubi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON operation summary with concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects a downstream Gougoubi skill, explains the routing reason, passes inputs through, and recommends the next action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
