## Description:

OpenClaw Vault helps agents audit credential exposure, detect misconfigured permissions, inventory secrets, and identify stale credentials that may need rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to review workspaces for credential lifecycle issues, including exposed secret files, shell history leaks, git configuration risks, hardcoded credentials, stale credentials, and public-directory exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive user-level files such as shell history and shell configuration while looking for credential exposure.

Mitigation: Run scan-only commands first in a constrained workspace and review reported file paths before broadening scope.

Risk: Remediation commands can change permissions or move files during quarantine and protect flows.

Mitigation: Avoid protect, fix-permissions, quarantine, and unquarantine until behavior is documented and the operator has explicitly consented to file changes.

Risk: Credential findings may include sensitive file locations or masked secret fragments in terminal output.

Mitigation: Treat reports as sensitive security output and avoid pasting them into shared logs or public issue trackers.

## Reference(s):

- [OpenClaw Vault on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-vault)
- [AtlasPA Publisher Profile](https://clawhub.ai/user/atlaspa)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and tabular findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate clean, warning, or critical credential exposure states.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
