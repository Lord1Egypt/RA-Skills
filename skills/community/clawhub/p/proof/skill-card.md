## Description:

Proof is a local-first cryptographic toolkit for zero-knowledge proof generation, circuit compilation with local toolchains, and formal verification analysis on local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticio](https://clawhub.ai/user/agenticio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Proof to generate local proof artifacts, compile circuits, run formal checks, and audit project files without transmitting data to cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cryptographic and analysis tools may inspect user-selected files and write generated proof artifacts in the local workspace.

Mitigation: Run the skill only on intended files and review local toolchain commands before enabling SnarkJS, ZoKrates, or Solidity analyzers.

Risk: Proof generation and formal checks depend on the locally installed toolchain and project configuration.

Mitigation: Validate local toolchain versions and review generated proof artifacts or analyzer output before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agenticio/skills/proof)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with code and shell command snippets, plus local artifact paths when tools generate files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated proof artifacts under ~/.openclaw/workspace/proof; no cloud transmission is disclosed in the evidence.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
