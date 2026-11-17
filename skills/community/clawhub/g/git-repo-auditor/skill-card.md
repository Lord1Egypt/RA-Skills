## Description:

Audit Git repositories for security issues, large files, sensitive data, and repository health metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit local Git repositories for secrets, large files, and repository health before release, compliance review, or CI/CD integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal or JSON reports may include discovered secret values or snippets, which can spread credentials if reports are shared.

Mitigation: Treat reports as sensitive artifacts, avoid publishing or broadly sharing them, rotate any credentials found, and prefer redacting matched values by default.

Risk: The skill audits Git repository history and may expose sensitive project information.

Mitigation: Run it only on repositories the operator is authorized to audit and keep generated reports within the approved security workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/git-repo-auditor)
- [Publisher profile](https://clawhub.ai/user/derick001)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text with optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Git repository and git/python3 in PATH.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
