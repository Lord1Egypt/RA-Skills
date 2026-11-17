## Description:

Guides personal OpenClaw users through a minimal PowerMem long-term memory setup that reuses their existing OpenClaw conversation model and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teingi](https://clawhub.ai/user/teingi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and verify PowerMem-backed long-term memory for OpenClaw with minimal configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended one-line installer can execute changing third-party code on the user's machine.

Mitigation: Download and inspect the installer before execution, pin it to a reviewed commit or release, and avoid running it from a privileged shell.

Risk: Unpinned Python package installation can pull newer dependency versions than those reviewed.

Mitigation: Use a virtual environment and install version-pinned or hash-pinned Python dependencies from trusted package sources.

## Reference(s):

- [memory-powermem repository](https://github.com/ob-labs/memory-powermem)
- [memory-powermem installer script](https://raw.githubusercontent.com/ob-labs/memory-powermem/main/install.sh)
- [ClawHub skill page](https://clawhub.ai/teingi/skills/install-powermem-memory-minimal)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides step-by-step installation, verification, and troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
