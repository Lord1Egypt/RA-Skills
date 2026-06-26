## Description: <br>
Docker volume backup and restore for self-hosted Langfuse instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up and restore local Docker volumes for self-hosted Langfuse, including Postgres and MinIO data with optional ClickHouse handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore operations can overwrite current Langfuse database and MinIO data. <br>
Mitigation: Verify the backup date, stop the active Langfuse stack, and take a fresh snapshot of current data before restoring. <br>
Risk: Local backup files may contain sensitive Langfuse traces, scores, evaluations, and uploaded blobs. <br>
Mitigation: Store backups in a protected or encrypted directory with access limited to trusted operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/langfuse-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Docker containers and a user-selected local backup directory; no outbound network access is declared.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
