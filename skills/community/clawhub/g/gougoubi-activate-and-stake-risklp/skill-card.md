## Description: <br>
Activate Gougoubi proposal conditions and stake risk LP per condition in one deterministic workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to activate Gougoubi proposal conditions and add fixed risk LP to selected conditions in a single workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide live crypto voting, committee staking, and risk LP additions. <br>
Mitigation: Inspect the referenced project scripts, run a dry run first, and require explicit approval before signing or broadcasting transactions. <br>
Risk: The selected proposal, conditions, LP amount, network, wallet, or total funds at risk may be incorrect. <br>
Mitigation: Confirm the wallet, network, proposal address, selected conditions, LP amount, and total maximum funds at risk before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-activate-and-stake-risklp) <br>
- [Gougoubi repository](https://github.com/gougoubi/gougoubi) <br>
- [Gougoubi website](https://gougoubi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-condition activation, risk LP, failure, warning, and next-action fields for the agent to report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
