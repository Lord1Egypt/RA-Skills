## Description:

Detects codebase bloat via dead code, duplication, complexity, and doc bloat scans

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find dead or stale code, duplication, complexity, documentation and dependency bloat, and growth trends during maintenance or before a release. It organizes findings into confidence-ranked analysis and remediation guidance for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional package registry checks may disclose dependency names.

Mitigation: Run only the checks needed for the task, and skip registry lookups when that disclosure is unacceptable.

Risk: Some commands are reported as posing file-overwrite risk, and the security scan could not resolve some local references.

Mitigation: Inspect commands and target paths before running them; use dry-run options and backups for file-changing cleanup, and review referenced components when needed.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-bloat-detector)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON findings with optional shell commands for analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tiered findings include confidence and prioritization; remediation proposals are reviewed by the user before changes.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
