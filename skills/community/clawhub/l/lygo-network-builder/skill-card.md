## Description:

Helps agents load LYGO network anchors, run local verification, and report alignment status without simulating probe results or publishing automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to locate LYGO network anchors, run the required stack verification scripts, and answer with verified anchor status and failure IDs when checks do not pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification depends on a user-selected lygo-protocol-stack checkout and mutable external installer/source state.

Mitigation: Install only from trusted ClawHub installer sources, prefer pinned installer versions, and verify the stack revision before running wrapper scripts.

Risk: Verifier scripts execute with the user's normal local permissions and write a verification artifact.

Mitigation: Review the stack checkout before execution and limit use to the documented read path, write path, subprocesses, and public anchor HTTP probes.

Risk: The skill can produce misleading alignment claims if probe results are fabricated or verification is skipped.

Mitigation: Run the documented verification scripts before declaring LATTICE ALIGNED and report failed anchor IDs when required checks fail.

Risk: Anchor metadata may contain operator-local paths that are not suitable for public output.

Mitigation: Use stack-relative documentation paths in public responses and avoid exposing admin-only filesystem paths.

## Reference(s):

- [LYGO Network Builder ClawHub Page](https://clawhub.ai/deepseekoracle/skills/lygo-network-builder)
- [lygo-protocol-stack GitHub Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [lygo-protocol-stack Pages](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [AGENT_CONTRACT.md](references/AGENT_CONTRACT.md)
- [SECURITY.md](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and verification tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report anchor IDs, pass/fail verdicts, warnings, and required local setup values.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
