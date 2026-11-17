## Description:

Windows LYGO PC audit map for lattice alignment, secret hygiene, Ollama army sentinel checks, and ClawHub security review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and operators use this skill to review Windows LYGO operator machines before hardening, USB CLAW, or mesh-node work. It provides advisory checklists and commands while keeping firewall, registry, publish, and other host changes human-approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installer commands can introduce supply-chain uncertainty.

Mitigation: Use a pinned ClawHub installer version or another verified installation workflow before installing.

Risk: Hardening recommendations could affect firewall, registry, or operating-system settings if applied without review.

Mitigation: Treat output as advisory and approve each host change step by step before execution.

Risk: Secrets could be exposed if audit output includes API keys, tokens, or private keys.

Mitigation: Do not store or print API keys, tokens, or private keys in skill output.

## Reference(s):

- [Security guidance](references/SECURITY.md)
- [SkillSpector audit](references/SKILLSPECTOR_AUDIT.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-pc-lattice-hardening)
- [Project homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; host changes require explicit human approval.]

## Skill Version(s):

1.1.0 (source: frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
