## Description: <br>
Create a Gougoubi proposal condition from minimal input with deterministic defaults for deadline, trade deadline, normalization, and transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to add a condition to an existing Gougoubi proposal from a proposal identifier and condition name, with deterministic deadline defaults and a normalized transaction payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect proposal or condition details could create or submit an unintended condition. <br>
Mitigation: Before signing, verify the proposal address, condition name, generated deadlines, network, gas cost, and wallet account shown in the generated payload and wallet confirmation. <br>
Risk: Wallet transaction submission can have financial or governance consequences. <br>
Mitigation: Do not bypass wallet confirmation; review the canonical contract call and normalized payload before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-create-condition) <br>
- [Gougoubi proposals](https://gougoubi.ai/premarket/proposals) <br>


## Skill Output: <br>
**Output Type(s):** [structured JSON, guidance] <br>
**Output Format:** [JSON success or failure object with normalized input, transaction hash when available, warnings, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses deterministic deadline defaults; wallet confirmation remains required before transaction submission.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
