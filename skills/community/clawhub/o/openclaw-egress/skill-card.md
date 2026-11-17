## Description:

Network DLP for agent workspaces that scans skills and files for outbound URLs, data exfiltration endpoints, suspicious domains, and network function calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to inspect agent skills and workspace files for external connections, suspicious endpoints, and possible data exfiltration before installation or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutation commands can rename skill directories or rewrite source files.

Mitigation: Use scan, status, domains, and scan --skills-only before any mutation command; keep backups and review exactly which files will change before using protect, block, or quarantine.

Risk: Path-scoping weaknesses may affect unintended files when untrusted paths or skill names are supplied.

Mitigation: Use trusted workspace paths and skill names only, and do not pass untrusted user input to mutation commands.

## Reference(s):

- [Openclaw Egress ClawHub page](https://clawhub.ai/atlaspa/skills/openclaw-egress)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal reports with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 standard library only; command exit codes distinguish clean, review-needed, and action-needed scan outcomes.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-02-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
