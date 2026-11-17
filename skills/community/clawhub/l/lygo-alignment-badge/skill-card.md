## Description:

Verify LYGO node compliance: P0 golden SHA, stack demo, Phase 1 elasticity, Phase 3-4 federation, optional full Grok audit, and lattice checks, emitting JSON or Markdown badge output for community deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide LYGO node alignment checks and surface ALIGNED or NEEDS_FIX badge status after running the referenced verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses an unpinned npx package, so the installed ClawHub client may change over time.

Mitigation: Use a pinned or otherwise verified installer version when tighter supply-chain control is required.

Risk: Badge output from a third-party repository may be misleading if generated from untrusted or modified source.

Mitigation: Run the LYGO verification commands in a quarantined copy of the repository before relying on alignment status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-alignment-badge)
- [LYGO protocol stack documentation](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands and references to JSON or Markdown badge artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to report badge status only after running the verifier and to quarantine untrusted repositories before trusting third-party badge output.]

## Skill Version(s):

1.0.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
