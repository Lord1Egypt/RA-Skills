## Description: <br>
Manage and query a persistent SQLite-based graph of people and their relationships for personal CRM, org charts, mentorship, and collaboration mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makkzone](https://clawhub.ai/user/makkzone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, operators, and developers use this skill to maintain a local people relationship database, track professional contacts, map organizations, and export relationship graphs for analysis or visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores people, relationships, character notes, and other contact details in a local database that may be private or sensitive. <br>
Mitigation: Collect only necessary details, protect people.db and exported JSON files, and review exports before sharing them. <br>
Risk: Delete commands can remove people and cascade relationship records without built-in confirmation or recovery. <br>
Mitigation: Make backups before delete operations and verify identifiers before running deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/makkzone/people-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/makkzone) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, Python API usage, and JSON graph output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores people and relationship records in a local SQLite database and can export the graph as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
