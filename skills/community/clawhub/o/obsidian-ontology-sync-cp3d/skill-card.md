## Description:

Bidirectional sync between Obsidian PKM (human-friendly notes) and structured ontology (machine-queryable graph). Automatically extracts entities and relationships from markdown, maintains ontology graph, and provides feedback to improve note structure. Run sync every few hours via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-work teams use this skill to extract entities and relationships from Obsidian notes into a local ontology, then generate analysis and feedback reports for note quality, contact tracking, team management, and business intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background processing may index sensitive personal or business notes into a local ontology.

Mitigation: Use only with a vault intended for indexing, review configured source folders and output paths, and run the dry-run before enabling scheduled jobs.

Risk: Cron setup is advertised, but helper scripts referenced for setup are not present in the inspected files.

Mitigation: Avoid enabling cron until the exact commands, schedules, and disable procedure are reviewed and verified.

Risk: Bidirectional note updates are advertised, but the inspected script only supports extract, analyze, and feedback actions.

Mitigation: Treat note modification claims as unsupported unless a reviewed implementation is added; keep backups before using any future write-back behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/obsidian-ontology-sync-cp3d)
- [ClawHub publisher profile](https://clawhub.ai/user/cp3d1455926-svg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, YAML configuration, JSONL ontology records, and markdown feedback reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ontology updates and feedback files when executed with the provided Python sync script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
