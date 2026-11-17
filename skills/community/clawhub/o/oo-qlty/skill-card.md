## Description:

Use Qlty through an OOMOL-connected account to read workspace, project, issue, metric, and account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to query Qlty workspaces, projects, issues, metrics, and account status through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup provides online installer commands without a clear approval step, creating a risk of running an unverified installer.

Mitigation: Prefer a verified oo CLI release and require user approval before the agent installs software.

Risk: Connecting Qlty authorizes OOMOL to mediate account access.

Mitigation: Connect only the intended Qlty account and review the connection before use.

## Reference(s):

- [Qlty](https://qlty.sh)
- [Qlty API documentation](https://docs.qlty.sh/api-reference/user/get-authenticated-user)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Structured JSON results and Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented Qlty actions read account and project data; the skill produces no files.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
