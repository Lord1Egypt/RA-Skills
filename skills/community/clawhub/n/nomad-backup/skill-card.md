## Description:

Query HashiCorp Nomad clusters to list jobs, nodes, allocations, evaluations, and services for read-only monitoring and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macdesire](https://clawhub.ai/user/macdesire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect HashiCorp Nomad cluster state, retrieve allocation logs, and troubleshoot jobs without submitting or modifying workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nomad variable reads can expose sensitive values if the agent is given broad ACL permissions.

Mitigation: Use a least-privilege Nomad ACL token, avoid granting variable-read access unless needed, and do not paste or display secret variable values in chat.

Risk: Shell examples that interpolate job or allocation identifiers can be unsafe when identifiers come from untrusted input.

Mitigation: Validate or safely quote identifiers before running command examples.

Risk: Read-only cluster status and allocation logs can still reveal operational details or sensitive application output.

Mitigation: Limit token scope to the namespaces and resources needed for troubleshooting and avoid sharing sensitive logs in agent conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/macdesire/skills/nomad-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Nomad CLI commands and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nomad CLI and Nomad environment variables such as NOMAD_ADDR and, when ACLs are enabled, NOMAD_TOKEN.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
