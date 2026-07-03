## Description: <br>
Operate Customer.io through an OOMOL-connected account for reading, creating, updating, deleting, and tracking customer data with the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Customer.io action schemas and run customer profile and event operations through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some Customer.io state-changing actions are not consistently tagged as write or destructive in the skill text. <br>
Mitigation: Treat identify, suppress, unsuppress, merge, delete, and event-tracking actions as write operations; confirm the exact target, payload, and effect before execution. <br>
Risk: Commands can affect live Customer.io workspace data. <br>
Mitigation: Fetch the live action schema before building payloads and review the JSON payload with the user before running connector commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-customerio) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Customer.io homepage](https://customer.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI schema and run commands; command responses are JSON with data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
