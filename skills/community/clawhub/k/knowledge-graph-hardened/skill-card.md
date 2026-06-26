## Description: <br>
Maintain Clawdbot's compounding knowledge graph under life/areas/** by adding/superseding atomic facts (items.json), regenerating entity summaries (summary.md), and keeping IDs consistent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain a local file-based knowledge graph by adding atomic facts, superseding outdated facts, and regenerating entity summaries without hand-editing JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and edit personal knowledge-base files stored locally. <br>
Mitigation: Install only for intended knowledge-base files, keep backups or version control, and review proposed edits before applying them. <br>
Risk: Sensitive personal information could be stored without the data subject's explicit consent. <br>
Mitigation: Do not store sensitive personal information about any person unless that individual has explicitly consented to that specific data category. <br>
Risk: Superseding a fact changes the active knowledge graph state and is treated as effectively irreversible by the skill guidance. <br>
Mitigation: Confirm the exact fact ID and replacement text with the user before running supersede commands. <br>
Risk: Knowledge graph contents may contain personal data that should not leave the local machine through agent-generated commands. <br>
Mitigation: Do not pipe kg.py output or knowledge graph file contents to network-transmitting commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/knowledge-graph-hardened) <br>
- [Faberlens knowledge-graph safety evaluation](https://faberlens.ai/explore/knowledge-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands; local JSON and Markdown file updates when commands are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem updates under life/areas/**; no network transfer is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
