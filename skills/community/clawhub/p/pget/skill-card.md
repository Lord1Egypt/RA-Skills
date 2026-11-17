## Description:

Pget guides agents to use the pget CLI for high-throughput parallel downloads, multifile manifests, and optional tar extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelvincai522](https://clawhub.ai/user/kelvincai522)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when they need an agent to propose pget commands for faster large-file downloads, multifile batch downloads, or download-and-extract workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified latest-release binary with sudo into a system-wide directory can expose the environment to supply-chain or privilege risk.

Mitigation: Prefer a pinned and verified pget release or a trusted package manager, and avoid running the download step with sudo when a user-local install path is sufficient.

Risk: Using --force or archive extraction with an incorrect destination path can overwrite files or place extracted content somewhere unintended.

Mitigation: Review destination paths before execution, avoid --force unless overwrite is intended, and extract archives into a controlled directory.

## Reference(s):

- [pget CLI reference](artifact/references/pget.md)
- [ClawHub skill page](https://clawhub.ai/kelvincai522/skills/pget)
- [Publisher profile](https://clawhub.ai/user/kelvincai522)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination paths, concurrency settings, retry settings, overwrite flags, manifest usage, and archive extraction options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
