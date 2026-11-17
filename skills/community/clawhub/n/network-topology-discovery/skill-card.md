## Description:

Discovers network topology iteratively using CDP/LLDP neighbor protocols, ARP/MAC table correlation, and routing table analysis across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and security teams use this skill to map or validate network topology from an authorized seed device. It supports inventory, incident response, pre-change impact analysis, migration planning, and documentation audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled read-only, but some troubleshooting guidance recommends configuration-changing actions.

Mitigation: Treat the skill as an authorized discovery playbook; use read-only accounts and perform any configuration changes only through a separate approved change process.

Risk: Topology reports can expose sensitive infrastructure details, including devices, links, subnets, VRFs, and management addresses.

Mitigation: Define a written discovery scope before use and protect generated reports as sensitive infrastructure data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/network-topology-discovery)
- [CLI reference](artifact/references/cli-reference.md)
- [Discovery workflow](artifact/references/discovery-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with vendor-specific CLI command blocks, topology data templates, decision trees, and report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewed topology discovery notes, adjacency and inventory models, Mermaid or CSV/JSON-ready topology representations, and audit report content.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
