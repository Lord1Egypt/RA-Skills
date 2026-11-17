## Description:

Query ad platform data (Meta, Google, LinkedIn, Reddit) using the Hopkin CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nemo](https://clawhub.ai/user/nemo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and advertising operators use this skill to query ad accounts, campaigns, ads, and performance data across supported paid advertising platforms. It is intended for read-only reporting, inspection, and cross-platform comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Hopkin API key and advertising account access, which can expose sensitive advertising credentials if pasted into normal chat or shell history.

Mitigation: Use a narrowly scoped Hopkin API key, avoid pasting secrets into chat or shell commands, and rotate any key that may have been logged.

Risk: The skill instructs agents to install or update a global CLI from npm, including latest-version updates.

Mitigation: Prefer a pinned or locally reviewed Hopkin CLI install before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nemo/skills/hopkin-paid-ads)
- [Hopkin API Keys](https://app.hopkin.ai/settings/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides read-only Hopkin CLI queries and recommends JSON, CSV, or TSV output formats.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
