## Description:

LYGO OpenClaw is a sovereign command router for LYGO stack operators, mapping P0 validation, lattice status, sentinel checks, and consent-gated kernel planter commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and operators use this skill to route LYGO OpenClaw stack commands through documented validation, status, lattice, sentinel, and consent-gated planter workflows. It is most relevant when working with a trusted local LYGO protocol stack clone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer command is unpinned in the skill documentation.

Mitigation: Prefer a pinned clawhub installer version when available and avoid running installation commands with elevated privileges.

Risk: Stack commands depend on the local path provided through LYGO_STACK_ROOT.

Mitigation: Point LYGO_STACK_ROOT only at a LYGO stack clone the operator trusts before running linked tools.

Risk: Hybrid runtime workflows may require sensitive credentials outside this skill package.

Mitigation: Do not provide Discord tokens, API keys, wallets, or browser credentials unless intentionally invoking a separate trusted runtime that needs them.

Risk: Kernel planter and live chart operations can perform higher-impact actions.

Mitigation: Require explicit human consent before planter or live chart workflows, matching the artifact security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-open-claw)
- [LYGO protocol stack](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Agent contract](references/AGENT_CONTRACT.md)
- [Security](references/SECURITY.md)
- [SkillSpector audit](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and command maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local LYGO_STACK_ROOT for stack-tool execution; the package self-check is local and uses the Python standard library.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
