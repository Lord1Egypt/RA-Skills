## Description:

Connects to Codacy through the user's OOMOL account to retrieve organization, repository analysis, language, and code-pattern data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to read Codacy account, organization, repository analysis, supported language, and code-pattern information through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a remote installer that was unavailable for inspection.

Mitigation: Install a verified oo CLI version yourself and require approval before any installer runs.

Risk: The skill accesses Codacy through the user's connected OOMOL account.

Mitigation: Confirm the connected account and its Codacy access are appropriate before use.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Codacy](https://www.codacy.com)
- [Codacy API documentation](https://api.codacy.com/api/api-docs)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Guidance]

**Output Format:** [JSON responses and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves Codacy data using supported read actions.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
