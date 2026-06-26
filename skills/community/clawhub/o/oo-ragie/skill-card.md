## Description: <br>
Ragie lets an agent inspect schemas and run Ragie connector actions through the oo CLI for reading, creating, updating, retrieving, and deleting Ragie data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage Ragie RAG resources from an OOMOL-connected account, including document ingestion, retrieval, metadata updates, partition management, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents may be sent to Ragie for cloud indexing. <br>
Mitigation: Only ingest data approved for Ragie, and avoid secrets, private files, regulated data, or confidential documents unless upload has been explicitly authorized. <br>
Risk: Write and destructive actions can modify or delete Ragie documents, partitions, metadata, or limits. <br>
Mitigation: Confirm the exact action, target IDs, payload, and expected effect before running write or destructive commands. <br>
Risk: The skill requires an OAuth-backed connection and sensitive credentials managed through OOMOL. <br>
Mitigation: Use only intended connected accounts, do not expose raw credentials, and reconnect or adjust scopes only when an auth or connection error requires it. <br>


## Reference(s): <br>
- [ClawHub Ragie Skill](https://clawhub.ai/oomol/oo-ragie) <br>
- [Ragie Homepage](https://www.ragie.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include a data object and meta.executionId when actions run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
