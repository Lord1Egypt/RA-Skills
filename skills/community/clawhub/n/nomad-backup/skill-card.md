## Description: <br>
Query HashiCorp Nomad clusters. List jobs, nodes, allocations, evaluations, and services. Read-only operations for monitoring and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macdesire](https://clawhub.ai/user/macdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect HashiCorp Nomad cluster state, troubleshoot jobs and allocations, view logs, and check nodes, services, namespaces, variables, and evaluations with read-only Nomad CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cluster logs, Nomad variables, and Nomad tokens may expose sensitive operational data in the agent conversation. <br>
Mitigation: Use a read-only scoped Nomad ACL token and avoid requesting full allocation logs or variable values unless that data is acceptable to disclose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macdesire/nomad-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Nomad CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nomad CLI and Nomad environment variables; commands are intended to be read-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
