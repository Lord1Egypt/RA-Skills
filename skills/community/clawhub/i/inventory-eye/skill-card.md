## Description:

库存慧眼 is a Chinese-language inventory management agent for importing CSV inventory data, monitoring stock and expiry alerts, managing inbound and outbound changes, and generating reorder and turnover analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Small retailers, restaurants, warehouse operators, and e-commerce sellers use this agent to track local inventory, identify low-stock or expiring items, and generate replenishment or turnover guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change business inventory records through import, add, update, delete, inbound, and outbound actions.

Mitigation: Require explicit confirmation before record-changing actions and keep backups of the dedicated inventory data directory.

Risk: The skill can export inventory data to arbitrary writable file paths.

Mitigation: Restrict exports to approved locations and avoid user-supplied paths outside a sandboxed work area.

Risk: The skill may run with access to important local files or production inventory records.

Mitigation: Run it with a dedicated IE_DATA_DIR and sandboxed file access when possible.

## Reference(s):

- [库存管理指南](references/inventory-guide.md)
- [Inventory Eye release page](https://clawhub.ai/hanjing5024064/skills/inventory-eye)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown with tables, JSON command outputs, and occasional Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local CSV inputs and local JSON inventory and transaction records; paid-tier workflows gate advanced recommendations and reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
