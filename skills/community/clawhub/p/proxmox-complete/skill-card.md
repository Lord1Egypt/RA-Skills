## Description:

Manage Proxmox VE clusters via REST API, including nodes, VMs, containers, power states, snapshots, backups, storage, tasks, and health status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to inspect and administer Proxmox VE clusters through generated shell commands, Python API calls, and configuration guidance. It supports VM and container status checks, power operations, snapshots, backups, storage inspection, task logs, and node health workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run power, snapshot, rollback, deletion, and backup actions that change Proxmox infrastructure.

Mitigation: Require explicit confirmation for each mutating action and use a least-privilege Proxmox API token.

Risk: TLS verification can be disabled in the documented configuration and Bash helper.

Mitigation: Enable TLS verification with a trusted certificate before production use.

Risk: Credentials may be stored in local files or environment variables, including a Bash-sourced fallback file.

Mitigation: Prefer protected secret storage, restrict credential file permissions, and avoid the Bash fallback credential file.

Risk: The skill depends on external command-line tools and the proxmoxer Python package.

Mitigation: Install only reviewed, pinned dependency versions in the agent runtime.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against a configured Proxmox VE API and may return JSON from the Python helper or formatted shell output from the Bash helper.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter and _meta.json state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
