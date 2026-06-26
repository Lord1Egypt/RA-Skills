## Description: <br>
Bidirectional sync between Obsidian PKM notes and a structured ontology graph, with extraction of entities and relationships plus feedback to improve note structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shi8103312](https://clawhub.ai/user/shi8103312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-work users use this skill to convert selected Obsidian markdown folders into a local ontology graph, run analytics, and generate feedback about missing fields or relationship gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly convert private Obsidian notes about contacts, clients, teams, and work behavior into durable local graph and feedback files. <br>
Mitigation: Install only when that conversion is intended; run dry-run mode first, review input and output paths, and exclude sensitive folders or fields where possible. <br>
Risk: Scheduled sync can preserve sensitive extracted data over time in generated ontology and feedback outputs. <br>
Mitigation: Before enabling cron, use a narrow configuration and protect or periodically delete generated graph and feedback files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shi8103312/obsidian-ontology-sync-1-0-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration examples, JSONL graph records, and feedback reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append extracted entities and relationships to local graph.jsonl files and write dated markdown feedback reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
