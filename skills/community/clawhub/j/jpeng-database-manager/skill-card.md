## Description: <br>
Database management skill supporting PostgreSQL, MySQL, SQLite, and MongoDB. Query, migrate, backup, and manage databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query, migrate, back up, restore, import, export, and manage PostgreSQL, MySQL or MariaDB, SQLite, and MongoDB databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database write, restore, import, or migration commands can change data or schema state. <br>
Mitigation: Review every write-capable command before execution, prefer read-only credentials when possible, and use non-production databases unless production access is explicitly intended. <br>
Risk: Backups and exports can contain sensitive records. <br>
Mitigation: Protect exported files and backups with appropriate access controls, storage locations, and retention practices. <br>
Risk: Database connection settings and credentials can expose privileged access. <br>
Mitigation: Use least-privileged credentials, keep secrets out of shared logs and files, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Database operations may produce files such as backups, migration outputs, exports, or query result summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
