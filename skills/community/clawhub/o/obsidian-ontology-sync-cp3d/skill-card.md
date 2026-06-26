## Description: <br>
Bidirectional sync between Obsidian PKM notes and a structured ontology graph, extracting entities and relationships from Markdown, maintaining the graph, and providing feedback to improve note structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to sync Obsidian Markdown notes into an ontology graph for queryable contacts, clients, projects, team status, analytics, and feedback about missing or inconsistent note data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ontology graphs and feedback reports may centralize sensitive contact details, team relationships, business context, and behavioral notes. <br>
Mitigation: Store graph.jsonl and feedback reports securely, restrict access to the output directory, and review retention expectations before regular use. <br>
Risk: Incorrect vault, source, or output paths could process unintended notes or write generated data to unexpected locations. <br>
Mitigation: Edit config.yaml before running, start with --dry-run, review the generated graph and feedback files, and enable cron only after confirming the paths and outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cp3d1455926-svg/obsidian-ontology-sync-cp3d) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration, and JSON/JSONL ontology examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ontology graph updates and feedback reports when run against a configured vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
