## Description: <br>
MySQL Master-Slave Setup & Troubleshooting SOP. Covers replication setup, Percona XtraBackup large-volume migration, replica lag investigation, and cross-cloud database acceleration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and DBAs use this skill as a MySQL operations runbook for replication setup, Percona XtraBackup migration, replica lag diagnosis, memory investigation, and cross-server migration planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runbook includes production DBA actions such as stopping MySQL, resetting replication, restoring backups, and clearing data directories. <br>
Mitigation: Require explicit human approval, verify target hostnames, IPs, database names, and data paths, and take backups or snapshots before running destructive or service-impacting commands. <br>
Risk: Examples include placeholder credentials, hostnames, and replication positions that could be copied without environment-specific review. <br>
Mitigation: Replace all placeholders with approved values, use managed secrets for credentials, and validate binlog file and position against the source database before applying replication changes. <br>
Risk: Migration and cross-cloud acceleration steps can expose database connectivity if security groups or accelerator backends are too broad. <br>
Mitigation: Limit database access to required sources, review security group rules, and test connectivity without widening production database exposure. <br>


## Reference(s): <br>
- [Percona Release Package](https://repo.percona.com/yum/percona-release-latest.noarch.rpm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, SQL, and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checklists, command examples, configuration snippets, and troubleshooting tables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
