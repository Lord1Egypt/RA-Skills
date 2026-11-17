## Description:

MongoDB Connector lets agents connect to cloud-hosted MongoDB instances to query, export, aggregate, search, and manage database resources through permission-gated AgentPMT remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let agents work with cloud-hosted MongoDB databases for reads, writes, exports, aggregation pipelines, search indexes, and administrative database tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad database-changing and administrative authority.

Mitigation: Restrict the connected MongoDB account and platform permissions to the minimum needed, and avoid delete or admin permissions for production data unless required.

Risk: Live remote instructions or schemas may change after installation.

Mitigation: Review live instructions and schemas before production use, and reinstall the skill when freshness guidance says the local copy is stale.

Risk: Exported database results may contain sensitive data.

Mitigation: Treat CSV and JSON exports as sensitive files and scope queries to the minimum data needed.

## Reference(s):

- [MongoDB Connector marketplace page](https://www.agentpmt.com/marketplace/mongodb-connector)
- [MongoDB Connector ClawHub listing](https://clawhub.ai/agentpmt/skills/mongodb-connector)
- [MongoDB Connector generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, JSON, Files]

**Output Format:** [Markdown instructions with JSON tool-call examples and optional CSV or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 24 permission-gated remote actions; find and aggregate calls cap inline results at 1000 documents.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
