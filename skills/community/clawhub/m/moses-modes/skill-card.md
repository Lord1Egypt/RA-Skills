## Description:

Moses Modes applies operator-selected governance modes as behavioral guardrails for an agent, using persistent mode state from the companion moses-governance skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to apply explicit governance postures such as high-security, high-integrity, research, creative, problem-solving, or unrestricted behavior to an agent. It is intended for environments where trusted operators control the active governance state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent mode state can affect agent behavior across tasks.

Mitigation: Install only where trusted operators control governance state and review the active mode before sensitive work.

Risk: Unrestricted mode can remove the skill's behavioral constraints.

Mitigation: Avoid unrestricted mode for sensitive tasks and require explicit operator approval before enabling it.

Risk: Audit and growth-log behavior has unclear privacy limits.

Mitigation: Define logging scope, retention, and privacy boundaries before enabling audit or growth-log behavior.

## Reference(s):

- [Moses Modes ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-modes)
- [MO§ES™ Governance Modes Reference](artifact/references/modes.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on moses-governance state in ~/.openclaw/governance/state.json.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
