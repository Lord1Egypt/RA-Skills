## Description:

Detects codebase bloat via dead code, duplication, complexity, and doc bloat scans

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to inspect a codebase for dead code, duplication, complexity, documentation bloat, dependency issues, and growth trends, then prioritize review or cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional registry or SonarQube access may share project information with external services.

Mitigation: Check which services are enabled and their destinations before scanning; avoid using them on sensitive projects unless that data sharing is acceptable.

Risk: Scan commands may overwrite or delete files in the project directory.

Mitigation: Review the commands before running them, use dry-run or preview options where available, and ensure the project is recoverable from version control or backups.

Risk: The partial security scan missed two referenced local files, so its evidence is incomplete.

Mitigation: Review the missing files and treat the security assessment as incomplete until they are available and assessed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-conserve-bloat-detector)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal findings and Markdown reports, with optional YAML or JSON summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tiered analysis; deeper scans may use optional local tools and Git history.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
