## Description:

Helps agents work with Palantir Foundry using the pltr CLI to query datasets, manage orchestration builds, work with ontologies, run SQL queries, manage folders, spaces, projects, copy datasets, and perform admin operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjor](https://clawhub.ai/user/anjor)

### License/Terms of Use:


## Use Case:

Developers and data/platform engineers use this skill for guidance on constructing and reviewing pltr CLI commands for Palantir Foundry operations, including datasets, SQL, ontologies, orchestration, filesystem resources, connectivity, admin tasks, streams, AIP agents, and model registry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers powerful live Foundry workflows, including admin actions, deletion, permission changes, imports, stream publishing, ontology actions, and schedule changes.

Mitigation: Use least-privilege Foundry credentials and require explicit human approval before commands that delete data, change access, execute imports, publish streams, invoke ontology actions, alter schedules, or use force/confirmation flags.

Risk: Commands may expose secrets or sensitive Foundry data through arguments, exports, profiles, or local output files.

Mitigation: Avoid pasting secrets into command arguments, prefer secure credential handling, avoid production profiles unless necessary, and review exported files before writing or sharing them.

Risk: The security evidence notes weak safety guidance around live data and admin operations.

Mitigation: Pin and verify the pltr-cli package, review generated commands before execution, and supervise all data and admin workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anjor/skills/pltr-cli)
- [Quick Start & Authentication](reference/quick-start.md)
- [Dataset Commands](reference/dataset-commands.md)
- [SQL Commands](reference/sql-commands.md)
- [Orchestration Commands](reference/orchestration-commands.md)
- [Ontology Commands](reference/ontology-commands.md)
- [Admin Commands](reference/admin-commands.md)
- [Filesystem Commands](reference/filesystem-commands.md)
- [Connectivity Commands](reference/connectivity-commands.md)
- [MediaSets Commands](reference/mediasets-commands.md)
- [Language Models Commands](reference/language-models-commands.md)
- [Streams Commands](reference/streams-commands.md)
- [Functions Commands](reference/functions-commands.md)
- [AIP Agents Commands](reference/aip-agents-commands.md)
- [Models Commands](reference/models-commands.md)
- [Data Analysis Workflows](workflows/data-analysis.md)
- [Data Pipeline Workflows](workflows/data-pipeline.md)
- [Permission Management Workflows](workflows/permission-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that operate on live Foundry data, permissions, schedules, streams, imports, or local exports.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
