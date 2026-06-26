## Description: <br>
Moses Roles defines Primary, Secondary, and Observer agent roles with enforced response sequencing for a multi-agent governance workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to assign Primary, Secondary, and Observer responsibilities to agents and keep multi-agent responses in a defined sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent role sequencing and AGENTS.md overrides can change how agents respond in a workspace. <br>
Mitigation: Review any AGENTS.md changes before applying them and install only where persistent multi-agent sequencing is intended. <br>
Risk: The governance state file influences active role, mode, and posture behavior. <br>
Mitigation: Keep ~/.openclaw/governance/state.json under operator control and review its contents when behavior changes. <br>
Risk: MOSES_OPERATOR_SECRET is documented as an optional sensitive local signing secret. <br>
Mitigation: Leave MOSES_OPERATOR_SECRET unset unless local signing is required, and do not transmit or commit the value. <br>
Risk: Audit logging depends on a companion moses-governance bundle. <br>
Mitigation: Review the companion moses-governance bundle before relying on its audit script. <br>


## Reference(s): <br>
- [Moses Roles on ClawHub](https://clawhub.ai/sunrisesillneversee/moses-roles) <br>
- [Publisher profile](https://clawhub.ai/user/sunrisesillneversee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References a local governance state file and optional companion audit command.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
