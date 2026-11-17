## Description:

MOSES Role Hierarchy defines Primary, Secondary, and Observer agent roles with enforced sequencing so Primary leads, Secondary validates, and Observer flags risks or inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to define a multi-agent role hierarchy where Primary, Secondary, and Observer agents respond in a controlled order. It supports governance workflows that require validation, oversight, audit logging, and operator-controlled broadcast overrides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent role and sequencing rules can block or constrain agent responses in a workspace.

Mitigation: Install only where operators intentionally want this governance behavior, and review AGENTS.md changes before use.

Risk: The skill loads mutable governance state from ~/.openclaw/governance/state.json before responses.

Mitigation: Restrict who can edit the governance state file and review changes to the governance directory.

Risk: Audit behavior depends on companion moses-governance tooling.

Mitigation: Install and verify the companion moses-governance audit script before relying on audit logging.

Risk: MOSES_OPERATOR_SECRET is declared as optional sensitive configuration, while the artifact says no secrets are required for this skill.

Mitigation: Leave MOSES_OPERATOR_SECRET unset unless an operator confirms the local signing gate is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-roles)
- [ClawHub publisher profile](https://clawhub.ai/user/sunrisesillneversee)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with command examples and AGENTS.md configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local governance state, optional environment configuration, and companion moses-governance audit tooling.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
