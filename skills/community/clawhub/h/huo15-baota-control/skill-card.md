## Description:

Helps an agent operate BT-Panel servers through the BT-Panel HTTP API for system status, memory, disk, load, website controls, databases, SSL certificates, scheduled tasks, Docker, and raw BT-Panel endpoint calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and administer BT-Panel-managed servers from an agent workflow. It is suited to structured operations such as checking system health, listing sites and databases, managing site state, working with certificates and scheduled tasks, and calling documented BT-Panel endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad administrative control over BT-Panel-managed servers, including raw endpoint access and write-capable operations.

Mitigation: Require explicit human confirmation for every write, file, task, Docker, certificate, database, or site-changing action, and restrict or remove raw mode where it is not needed.

Risk: The BT-Panel token is the primary protection for exposed panel access, and public tunnel configurations can collapse callers to 127.0.0.1.

Mitigation: Keep tokens out of transcripts and logs, store credentials only in locked-down local configuration, rotate exposed tokens, and avoid or tightly gate public tunnels.

Risk: The API wrapper disables normal TLS certificate verification.

Mitigation: Enable standard TLS verification before production use or otherwise constrain network access to trusted paths.

## Reference(s):

- [BT-Panel API control research](artifact/README.md)
- [BT-Panel endpoint reference](artifact/references/endpoints.md)
- [Release changelog](artifact/docs/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [BT-Panel API responses are JSON; the skill instructs the agent to summarize key fields for the user rather than returning full raw payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
