## Description:

Query HashiCorp Nomad clusters. List jobs, nodes, allocations, evaluations, and services. Read-only operations for monitoring and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danfedick](https://clawhub.ai/user/danfedick)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query HashiCorp Nomad cluster status, jobs, allocations, nodes, evaluations, services, variables, and logs for monitoring and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nomad variable values and allocation logs can expose secrets or sensitive operational data.

Mitigation: Use least-privilege Nomad ACL tokens, retrieve variables or raw logs only when needed, and redact secrets before sharing command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danfedick/skills/nomad)
- [Publisher profile](https://clawhub.ai/user/danfedick)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nomad CLI commands may return JSON when the -json flag is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
