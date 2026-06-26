## Description: <br>
Local-first CRM for managing leads, deals, follow-ups, and pipelines through a SQLite-backed command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and operators use this skill to manage local CRM records, track deal stages, schedule follow-ups, search contacts and deals, and produce pipeline reports without relying on external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CRM Markdown files may expose contacts, deal details, follow-up notes, or other CRM data to local agents or synced workspaces. <br>
Mitigation: Keep the workspace private and exclude interchange files from public sync or source control. <br>
Risk: Backup and restore commands can write or replace persistent CRM database files. <br>
Mitigation: Run backup and restore only with explicit, reviewed paths and verify backup files before restoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frank-bot07/openclaw-crm) <br>
- [Publisher profile](https://clawhub.ai/user/frank-bot07) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and generated Markdown interchange files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists CRM state in local SQLite files and can create or restore database backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
