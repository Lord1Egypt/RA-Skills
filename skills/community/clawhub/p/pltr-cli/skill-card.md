## Description: <br>
Helps agents guide Palantir Foundry CLI work for querying datasets, running SQL, managing builds, ontologies, projects, users, streams, AI agents, and ML models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anjor](https://clawhub.ai/user/anjor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and Foundry administrators use this skill to ask an agent for pltr CLI commands and workflow guidance for Palantir Foundry operations. It supports data exploration, dataset and filesystem work, SQL queries, orchestration, ontology tasks, access control, streaming, AI agents, and model registry tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands for powerful Foundry admin, data, and pipeline operations. <br>
Mitigation: Require explicit user approval before delete, --force, --yes, --confirm, --execute, role-management, user/group, stream-reset, and production schedule commands. <br>
Risk: Commands may target the wrong Foundry resource or environment if a RID or profile is incorrect. <br>
Mitigation: Verify every RID and profile before execution and prefer least-privilege development profiles when possible. <br>
Risk: Authentication tokens or client secrets could be exposed through chat or shell history. <br>
Mitigation: Do not paste real tokens or client secrets into chat or shell history; use secure profile and environment handling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anjor/pltr-cli) <br>
- [Quick Start & Authentication](reference/quick-start.md) <br>
- [Dataset Commands](reference/dataset-commands.md) <br>
- [SQL Commands](reference/sql-commands.md) <br>
- [Orchestration Commands](reference/orchestration-commands.md) <br>
- [Ontology Commands](reference/ontology-commands.md) <br>
- [Admin Commands](reference/admin-commands.md) <br>
- [Filesystem Commands](reference/filesystem-commands.md) <br>
- [Connectivity Commands](reference/connectivity-commands.md) <br>
- [MediaSets Commands](reference/mediasets-commands.md) <br>
- [Language Models Commands](reference/language-models-commands.md) <br>
- [Streams Commands](reference/streams-commands.md) <br>
- [Functions Commands](reference/functions-commands.md) <br>
- [AIP Agents Commands](reference/aip-agents-commands.md) <br>
- [Models Commands](reference/models-commands.md) <br>
- [Data Analysis Workflows](workflows/data-analysis.md) <br>
- [Data Pipeline Workflows](workflows/data-pipeline.md) <br>
- [Permission Management Workflows](workflows/permission-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides guidance and command examples; execution remains under the user's control.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
