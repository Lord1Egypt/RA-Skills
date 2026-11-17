## Description:

LYGO Tools Portal routes users and agents to LYGO public tools, related ClawHub skills, and optional stack CLI entries by reading the bundled tools manifest before building or guessing URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to find existing LYGO tools for BPM, lattice, biometric harness, resonance, music, and related workflows before creating duplicate pages or scripts. Agents can also use it to identify related ClawHub skills and optional stack commands for operator tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers agents toward publisher-controlled ClawHub installs and mutable npx commands.

Mitigation: Require explicit human approval before running install commands, and prefer pinned or otherwise verified package versions.

Risk: Optional local stack or vault access could expose more filesystem content than the manifest-only workflow needs.

Mitigation: Limit routine use to the skill mirror; grant LYGO_STACK_ROOT or LYGO_VAULT_ROOT access only when the operator has reviewed and approved the task.

Risk: Invented or stale canonical URLs could misroute users.

Mitigation: Use references/TOOLS_MANIFEST.json first, then the stack link archive only when a local stack checkout is intentionally available.

Risk: User audio or files could be sent to third-party services if routing guidance is applied carelessly.

Mitigation: Follow the security notes: do not send user audio or files to third parties when pointing at client-side tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-tools-portal)
- [ClawHub publisher profile](https://clawhub.ai/user/deepseekoracle)
- [LYGO Tools Manifest](references/TOOLS_MANIFEST.json)
- [Agent contract](references/AGENT_CONTRACT.md)
- [Security notes](references/SECURITY.md)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO protocol stack index](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [LYGO BPM Finder](https://bpmfinder.ca/)
- [Sovereign Lattice Mesh](https://deepseekoracle.github.io/lygo-protocol-stack/SovereignLatticeMesh.html)
- [Biometric Entropy Harness](https://deepseekoracle.github.io/lygo-protocol-stack/BiometricEntropyHarness.html)
- [LYGO Resonance](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html)
- [HF LYGO Resonance Engine](https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTPS links, JSON resolver output, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a read-only manifest plus optional LYGO_STACK_ROOT link archive lookup when a local stack checkout is explicitly available.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
