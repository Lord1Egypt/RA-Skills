## Description: <br>
Manage oVirt/RHV virtualization infrastructure via MCP with reference guidance for 186 tools covering VMs, hosts, clusters, networks, storage, templates, snapshots, disks, events, RBAC, quotas, and related operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjoey](https://clawhub.ai/user/imjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure administrators use this skill to install, configure, and operate the oVirt MCP Server for oVirt/RHV VM, host, storage, network, template, event, quota, and RBAC workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad oVirt/RHV administration, including delete, force, fence, reinstall, restore, RBAC, network, storage, disk, console, and alert-clearing actions. <br>
Mitigation: Use least-privilege credentials, restrict use to approved environments, and require human confirmation before high-impact operations. <br>
Risk: The MCP server requires oVirt Engine credentials and may be configured with password-bearing environment variables or config files. <br>
Mitigation: Use scoped accounts and secret-managed or ephemeral credentials, and avoid committing credentials in configuration files. <br>
Risk: Incorrect tool parameters can affect live VMs, hosts, storage, or network resources. <br>
Mitigation: Review arguments against the reference docs and test changes in non-production before applying them to production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/imjoey/ovirt-mcp) <br>
- [oVirt MCP Server](https://github.com/imjoey/ovirt-engine-mcp-server) <br>
- [oVirt](https://www.ovirt.org/) <br>
- [ovirtsdk4](https://github.com/oVirt/ovirt-engine-sdk-python) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [VM tool reference](references/vm.md) <br>
- [Host tool reference](references/host.md) <br>
- [Cluster tool reference](references/cluster.md) <br>
- [Storage tool reference](references/storage.md) <br>
- [Disk tool reference](references/disk.md) <br>
- [Network tool reference](references/network.md) <br>
- [Template tool reference](references/template.md) <br>
- [Events tool reference](references/events.md) <br>
- [RBAC tool reference](references/rbac.md) <br>
- [Quota tool reference](references/quota.md) <br>
- [Affinity tool reference](references/affinity.md) <br>
- [Data center tool reference](references/datacenter.md) <br>
- [System tool reference](references/system.md) <br>
- [Instance types tool reference](references/instance-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON snippets] <br>
**Output Format:** [Markdown reference with inline shell, YAML, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tool-domain reference files and operational workflow examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
