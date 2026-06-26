## Description: <br>
Bidirectional sync between Obsidian PKM notes and a structured ontology graph, with extraction, analysis, and feedback for improving note structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parthpandya1729](https://clawhub.ai/user/parthpandya1729) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge-management users can use this skill to scan selected Obsidian vault folders, extract entities and relationships into ontology storage, analyze graph quality, and generate feedback for improving notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan Obsidian notes and persist sensitive personal or business content into ontology data. <br>
Mitigation: Configure narrow vault and output paths, exclude private folders where possible, and review generated graph and feedback files before relying on them. <br>
Risk: Scheduled syncing can repeatedly extract new note content after initial setup. <br>
Mitigation: Avoid enabling cron until the scanned paths and disable process are understood and verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parthpandya1729/obsidian-ontology-sync) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSONL ontology or Markdown feedback files when run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Obsidian vault and ontology paths selected by the user or default configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
