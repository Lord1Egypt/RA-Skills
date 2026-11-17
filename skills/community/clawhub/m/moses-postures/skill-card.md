## Description:

Moses Postures defines posture controls for agents, including read-only, protected confirmation, and execution modes for transaction and state-changing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to apply posture-based controls before an agent reads state, changes files, makes external calls, or executes transactions. It is intended for governance workflows that distinguish read-only analysis from confirmed protective actions and higher-autonomy execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence broad agent execution and transaction behavior, including a full-autonomy posture.

Mitigation: Permit installation only in environments where the moses-governance bundle is trusted, posture changes are controlled, and full-autonomy operation is explicitly approved or disabled.

Risk: The skill depends on posture state stored under ~/.openclaw/governance, so unauthorized state changes could alter execution controls.

Mitigation: Protect ~/.openclaw/governance/state.json with appropriate file permissions, audit posture changes, and require operator confirmation for outbound or state-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-postures)
- [ClawHub publisher profile](https://clawhub.ai/user/sunrisesillneversee)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the companion moses-governance bundle and reads posture state from ~/.openclaw/governance/state.json.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
