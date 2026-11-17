## Description:

OpenClaw plugin skill map for live Haven pulse, stack verification, registry comparison, star chart gating, and alignment readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and operators use this skill to install and follow an OpenClaw plugin tool map for checking LYGO lattice readiness, comparing registries, verifying a trusted local stack, and gating live chart submissions with explicit human consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path uses unpinned remote installers whose resolved code was not included in the reviewed artifact.

Mitigation: Install only from the trusted deepseekoracle publisher, prefer a pinned version or verified digest, inspect the resolved OpenClaw plugin before enabling it, and use a least-privileged or isolated environment.

Risk: Live chart write workflows could have excessive agency if enabled without a separate approval gate.

Mitigation: Require readiness and star chart gate checks to pass, then proceed only with explicit human consent through the dedicated chart skill.

Risk: Stack-bound tools may read from an untrusted local stack path.

Mitigation: Set LYGO_STACK_ROOT only to a trusted local clone before running stack-bound tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-lattice-pulse)
- [LYGO Protocol Stack Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [SECURITY.md](references/SECURITY.md)
- [SKILLSPECTOR_AUDIT.md](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plugin tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python or Python 3 for the bundled self-check; stack-bound tools should use a trusted LYGO_STACK_ROOT.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
