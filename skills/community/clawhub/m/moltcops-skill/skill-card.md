## Description:

Pre-install security scanner for AI agent skills. Detects malicious patterns before you trust code. Local-first -- code never leaves your machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamthompson33](https://clawhub.ai/user/adamthompson33)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to scan AI agent skills before installation or execution and review PASS, WARN, or BLOCK verdicts for suspicious patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MoltCops presents clean scan results as safe while scan coverage can miss unsupported file types such as JSON, YAML, TOML, PowerShell, batch, module files, or extensionless scripts.

Mitigation: Treat the scan as a lightweight helper and manually review the full package or use another scanner before trusting a skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamthompson33/skills/moltcops-skill)
- [MoltCops Web Scanner](https://scan.moltcops.com)
- [MoltCops Website](https://moltcops.com)
- [MoltCops Moltbook Profile](https://moltbook.com/u/MoltCops)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal report with findings, summary counts, PASS/WARN/BLOCK verdict, and process exit code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 indicates PASS, 1 indicates WARN, and 2 indicates BLOCK.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
