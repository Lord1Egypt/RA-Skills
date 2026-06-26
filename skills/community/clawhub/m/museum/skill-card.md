## Description: <br>
Museum Data Manager helps agents query, manage, validate, and export records from a MySQL-backed museum database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackandking](https://clawhub.ai/user/jackandking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data collection teams, researchers, and agents use this skill to inspect museum records, track collection progress, find incomplete data, run SQL queries, and export datasets for reporting or backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrestricted SQL execution could change or delete museum database records. <br>
Mitigation: Use a least-privilege MySQL account, prefer read-only access unless writes are required, and review every custom SQL statement before execution. <br>
Risk: Misconfigured database credentials could expose broader data than the skill needs. <br>
Mitigation: Avoid root or GRANT ALL credentials and scope the account to only the intended museum database. <br>
Risk: Exports may write sensitive or unwanted data to user-selected paths. <br>
Mitigation: Choose export paths deliberately, keep backups, and review exported files before sharing or automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackandking/museum) <br>
- [Publisher profile](https://clawhub.ai/user/jackandking) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output and exported JSON, CSV, or SQL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MySQL connection settings and may write export files to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
