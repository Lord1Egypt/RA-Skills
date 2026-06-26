## Description: <br>
Accounting is a local AI assistant for recording income and expenses, querying transactions, generating reports, and analyzing statistics with offline local data storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuhemiao](https://clawhub.ai/user/chuhemiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and small-business users can use this skill to record income and expense transactions in natural language, query financial history, and generate summaries or reports from locally stored accounting data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local accounting data may include sensitive income and expense history. <br>
Mitigation: Keep the configured data directory private, maintain backups, and install the skill only when local JSON storage is acceptable. <br>
Risk: Edit and delete operations can modify or remove local financial records. <br>
Mitigation: Query records first, verify record IDs before editing or deleting, and keep backups to recover from accidental changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuhemiao/openclaw-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Natural-language text and markdown reports, with local JSON accounting records created or updated by the skill's tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transaction summaries, filtered query results, category statistics, report exports, and record IDs for later update or deletion.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
