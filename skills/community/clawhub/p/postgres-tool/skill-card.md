## Description: <br>
PostgreSQL database management tool for querying databases, exporting results, inspecting schemas, and safely performing UPDATE/DELETE operations with automatic backup and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuzongwen](https://clawhub.ai/user/liuzongwen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and operations teams use this skill to inspect PostgreSQL databases, run SELECT queries, export results, and perform controlled UPDATE, DELETE, and restore workflows with backups and confirmations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete PostgreSQL data. <br>
Mitigation: Review every SQL statement manually, use a least-privilege database account, keep confirmation prompts enabled, and verify backups before executing UPDATE or DELETE operations. <br>
Risk: Bundled database configuration contains placeholder credentials that may be unsafe if reused. <br>
Mitigation: Replace the bundled database config before use and store real credentials according to the deployment environment's secrets policy. <br>
Risk: Backup and export files may contain sensitive database records. <br>
Mitigation: Treat generated backup, metadata, CSV, and Excel files as sensitive data and apply access controls, retention limits, and secure deletion procedures. <br>
Risk: The security scan warns not to rely on --dry-run for UPDATE or DELETE unless the implementation is fixed. <br>
Mitigation: Use --dry-run only for restore preview workflows, and validate UPDATE or DELETE behavior in a non-production database before automation. <br>
Risk: The --force option skips interactive confirmation. <br>
Mitigation: Avoid --force except for intentionally automated, tested operations with separate backup and rollback controls. <br>


## Reference(s): <br>
- [postgres-tool release page](https://clawhub.ai/liuzongwen/postgres-tool) <br>
- [EXAMPLES.md](references/EXAMPLES.md) <br>
- [SAFETY_GUIDE.md](references/SAFETY_GUIDE.md) <br>
- [OFFLINE_DEPLOYMENT_GUIDE.md](references/OFFLINE_DEPLOYMENT_GUIDE.md) <br>
- [QUICK_REFERENCE.md](references/QUICK_REFERENCE.md) <br>
- [scripts README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, tabular query output, and CSV or Excel export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PostgreSQL backup, metadata, CSV, and Excel files during database administration workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
