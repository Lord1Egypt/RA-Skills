## Description: <br>
Hologres Slow Query Analysis helps diagnose slow and failed queries, query performance issues, and log management in Alibaba Cloud Hologres. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators and data platform engineers use this skill to inspect Hologres query logs, identify slow or failed SQL, compare resource-heavy query patterns, and adjust logging configuration during troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest broad database privileges such as SUPERUSER for log access. <br>
Mitigation: Prefer narrowly scoped read permissions and require database administrator approval before granting elevated access. <br>
Risk: Exported query logs can contain sensitive operational data. <br>
Mitigation: Treat query logs as sensitive data and confirm destination, retention, and access controls before exporting them. <br>
Risk: Database-level logging and retention changes can affect production behavior. <br>
Mitigation: Review ALTER DATABASE, retention, and external export steps before running them in a production environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wenbingyu/hologres-slow-query-analysis) <br>
- [Configuration reference](references/configuration.md) <br>
- [Diagnostic queries](references/diagnostic-queries.md) <br>
- [Log export guide](references/log-export.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL snippets for Hologres query-log inspection, permission checks, log export, and logging configuration.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
