## Description:

Security audit and credential hardening tool for OpenClaw instances that scans for sensitive files, detects credential exposure, checks gateway configuration, and migrates credentials to environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-big-fish](https://clawhub.ai/user/vincent-big-fish)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to audit OpenClaw installations for exposed credentials, sensitive files, and gateway misconfiguration, then optionally harden credentials by moving them into environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardening mode handles live credentials and writes credential-bearing files.

Mitigation: Run audit.py first, use harden.py with --dry-run before applying changes, and restrict permissions on ~/.openclaw/.env and security-backups.

Risk: Generated set_env.sh or set_env.ps1 scripts modify the user's environment.

Mitigation: Inspect generated setup scripts before running or sourcing them.

Risk: A custom --path can direct the scripts at an unexpected OpenClaw directory.

Mitigation: Use the default ~/.openclaw path or verify any custom --path before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincent-big-fish/skills/openclaw-safe-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON audit reports, environment files, and platform-specific setup scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit mode writes timestamped JSON reports; hardening mode may create backups, .env files, sanitized configuration, and setup scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
