## Description:

Scans codebases to discover environment variable usage, generate a documented .env.example, detect missing variables, and flag common secret-handling risks across Node.js, Python, Go, Ruby, and shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit project environment-variable usage, compare discovered variables against .env and .env.example files, and produce a report with missing, undocumented, orphaned, or risky secret-handling findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans project source and env-related files, which may expose sensitive variable names, secret values, or configuration details in the generated report.

Mitigation: Run it only in repositories you trust and review the report before sharing it outside the project team.

Risk: The artifact includes shell snippets that use fixed /tmp file paths for intermediate env-var lists.

Mitigation: Use a private mktemp directory when executing or adapting those snippets directly.

## Reference(s):

- [Phy Env Doctor on ClawHub](https://clawhub.ai/phy041/skills/phy-env-doctor)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, inline shell commands, and generated .env.example content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include discovered environment-variable names, file references, inferred descriptions, security findings, and remediation commands.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
