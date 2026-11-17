## Description:

Safely review and install third-party OpenClaw Skills by downloading to a temporary directory, running a 7-point security audit, generating a human-readable report, and installing only when safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanggqm](https://clawhub.ai/user/shanggqm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to review third-party skills before installation. It guides the agent through isolated download, file inventory, security checklist review, report generation, install-or-reject decisions, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch third-party repositories or npm packages and install files persistently into the user's OpenClaw skills directory.

Mitigation: Require explicit user confirmation before any download or persistent install, and keep review and installation as separate decisions.

Risk: Source strings and local skill names may be under-validated before shell commands or filesystem writes are proposed.

Mitigation: Validate source URLs, package names, and derived directory names before running shell commands or copying files.

Risk: The security scanner verdict is suspicious because the skill combines review guidance with installation behavior.

Mitigation: Treat the generated review report as advisory and inspect the proposed commands and install destination before allowing execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanggqm/skills/guomeiqing-safe-install)
- [README.en.md](artifact/README.en.md)
- [SKILL.en.md](artifact/SKILL.en.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell command blocks and structured security review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose downloads, scans, file copies, and cleanup actions through the agent's shell tool; installation should depend on the generated review outcome.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
