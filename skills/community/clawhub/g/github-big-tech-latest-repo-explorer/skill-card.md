## Description:

Finds a recently created repository with more than 1,000 stars from a curated set of major technology organizations and summarizes its purpose and approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to discover a recent, popular repository from its curated organization list and get a concise explanation of what it does, the problem it addresses, and how it works.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently reuse a GitHub token from the OpenClaw secrets file beyond the authentication setup it documents.

Mitigation: Remove the automatic ~/.openclaw/.env fallback, provide a dedicated GitHub token with minimal permissions explicitly, and keep the host secrets file inaccessible to the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengzuo613/skills/github-big-tech-latest-repo-explorer)
- [Curated organization list](artifact/references/organizations.json)
- [Repository summary output template](artifact/assets/output_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown repository summary saved as a dated history file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects one repository by default; supports configurable result count and selection strategy.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
