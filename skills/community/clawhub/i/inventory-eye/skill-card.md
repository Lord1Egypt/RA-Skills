## Description: <br>
库存慧眼 helps small operators import and manage inventory data, monitor stock levels, and generate reorder, slow-moving inventory, and turnover guidance in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External small retailers, restaurants, warehouse operators, and e-commerce sellers use this skill to import CSV inventory records, check low-stock, out-of-stock, and expiry alerts, manage inbound and outbound stock movements, and produce inventory health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change business inventory records from broad natural-language requests without a clear confirmation step. <br>
Mitigation: Require explicit confirmation before every import, inbound, outbound, update, or delete action, and keep backups of the IE_DATA_DIR inventory files. <br>
Risk: Inventory, pricing, and transaction history are stored on local disk. <br>
Mitigation: Use a controlled IE_DATA_DIR with appropriate file permissions and backup handling, and avoid using sensitive CSV data in untrusted sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanjing5024064/inventory-eye) <br>
- [库存管理指南](references/inventory-guide.md) <br>
- [OpenClaw](https://openclaw.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Analysis, Files] <br>
**Output Format:** [Chinese Markdown with tables and inline shell commands; scripts maintain local JSON inventory and transaction files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional IE_SUBSCRIPTION_TIER and IE_DATA_DIR settings; responses are expected to be in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
