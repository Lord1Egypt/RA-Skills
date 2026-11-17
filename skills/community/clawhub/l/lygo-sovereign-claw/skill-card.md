## Description:

LYGO Sovereign Claw Router provides a consent-gated command routing framework for LYGO OpenClaw stack operations such as lattice checks, army sentinel status, memory recall, and kernel egg actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and LYGO stack operators use this skill to route LYGO OpenClaw commands through validation, local memory and ledger storage, optional consensus, and consent-gated planter operations without loading the full hybrid OS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes users into broad external command tooling and mutable install or self-check paths.

Mitigation: Review the skill before installing, use a pinned trusted installer version, and run setup in a low-privilege environment.

Risk: LYGO_STACK_ROOT controls which local stack the commands operate against.

Mitigation: Set LYGO_STACK_ROOT only to a trusted local LYGO stack.

Risk: Hybrid runtime operations may require credentials through lyra-openclaw.

Mitigation: Provide only least-privilege runtime credentials after confirming how lyra-openclaw handles them.

Risk: Kernel egg planter operations can be sensitive command actions.

Mitigation: Require explicit consent before planter actions and preserve the documented no-auto-push behavior.

## Reference(s):

- [Security notes](references/SECURITY.md)
- [Agent contract](references/AGENT_CONTRACT.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-claw)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local LYGO stack paths, consent-gated actions, and runtime credential handling for companion tooling.]

## Skill Version(s):

1.0.0 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
