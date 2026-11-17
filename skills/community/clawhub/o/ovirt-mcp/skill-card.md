## Description:

Manage oVirt/RHV virtualization infrastructure via MCP with reference coverage for VMs, hosts, clusters, networks, storage, templates, snapshots, disks, events, RBAC, quotas, and related operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjoey](https://clawhub.ai/user/imjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to help agents install, configure, and operate an oVirt/RHV MCP server and choose the right tools for virtualization administration workflows. It is intended for VM lifecycle, host, storage, network, template, event, RBAC, quota, and affinity-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact oVirt/RHV infrastructure administration, including delete, force, fence, install, export, migration, storage, network, and RBAC-changing operations.

Mitigation: Require explicit human confirmation before high-impact operations and run the MCP server under a restricted account instead of broad administrative credentials.

Risk: Installation guidance references third-party MCP server packages without a pinned and verified release.

Mitigation: Use a pinned, verified MCP server release before installing or running the server in an environment with access to infrastructure.

Risk: Credential examples include an oVirt password and a broad admin-style user.

Mitigation: Store the oVirt password in a protected secret mechanism and avoid broad admin credentials where possible.

## Reference(s):

- [VM Tool Reference](references/vm.md)
- [Host Tool Reference](references/host.md)
- [Cluster Tool Reference](references/cluster.md)
- [Data Center Tool Reference](references/datacenter.md)
- [Storage Tool Reference](references/storage.md)
- [Disk Tool Reference](references/disk.md)
- [Network Tool Reference](references/network.md)
- [Template Tool Reference](references/template.md)
- [System Tool Reference](references/system.md)
- [Events Tool Reference](references/events.md)
- [RBAC Tool Reference](references/rbac.md)
- [Quota Tool Reference](references/quota.md)
- [Affinity Tool Reference](references/affinity.md)
- [Instance Types Tool Reference](references/instance-types.md)
- [oVirt MCP Server](https://github.com/imjoey/ovirt-engine-mcp-server)
- [oVirt](https://www.ovirt.org/)
- [ovirtsdk4](https://github.com/oVirt/ovirt-engine-sdk-python)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, YAML snippets, and tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for agent use; the referenced MCP tools can perform high-impact infrastructure changes when connected to an oVirt/RHV environment.]

## Skill Version(s):

0.1.0 (source: server release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
