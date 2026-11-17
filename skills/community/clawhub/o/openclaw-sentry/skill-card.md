## Description:

OpenClaw Sentry scans local agent workspaces for leaked API keys, tokens, passwords, private keys, credentials, high-risk files, and missing secret-protection patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to check workspaces for exposed secrets before sharing, committing, or continuing automated work. It supports scan, single-file check, and status workflows, with higher-impact commands available for redaction, quarantine, and workspace defense.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact commands can redact, quarantine, unquarantine, defend, or protect workspace files.

Mitigation: Prefer scan, check, and status for routine use; run file-changing commands only on trusted workspace-relative paths after reviewing the intended action.

Risk: Plaintext backups and quarantine contents can retain sensitive material after remediation.

Mitigation: Restrict access to backups and quarantine directories, review their contents before restore or deletion, and rotate any credential that was exposed.

Risk: Weak workspace containment can increase the impact of running commands with an unintended workspace path.

Mitigation: Pass an explicit workspace path, avoid elevated privileges, and confirm the target directory before running redaction, quarantine, defend, or protect operations.

## Reference(s):

- [OpenClaw Sentry on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-sentry)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and no external package dependencies.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
