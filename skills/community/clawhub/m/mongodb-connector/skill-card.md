## Description: <br>
MongoDB Connector connects an agent to a user's cloud-hosted MongoDB instance to run 24 permission-gated database operations, including queries, CSV or JSON export, aggregation pipelines, and Atlas vector search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to query, export, aggregate, mutate, index, and administer cloud-hosted MongoDB databases through AgentPMT-hosted remote tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can give agents broad database mutation, deletion, export, and command authority. <br>
Mitigation: Install only for tightly permissioned AgentPMT groups and MongoDB users; prefer read-only credentials unless mutation is required. <br>
Risk: Delete, drop, bulk write, and run_command workflows can cause destructive or high-impact database changes. <br>
Mitigation: Require human confirmation before delete, drop, bulk_write, and run_command actions. <br>
Risk: Exports may expose sensitive fields from connected databases. <br>
Mitigation: Review every export for sensitive fields and keep tool inputs scoped to the minimum content needed for the task. <br>


## Reference(s): <br>
- [MongoDB Connector schema](artifact/schema.md) <br>
- [MongoDB Connector marketplace page](https://www.agentpmt.com/marketplace/mongodb-connector) <br>
- [MongoDB Connector ClawHub page](https://clawhub.ai/agentpmt/mongodb-connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and optional CSV or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Find and aggregate actions cap inline results at 1000 documents; CSV or JSON export can be requested for supported read workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
