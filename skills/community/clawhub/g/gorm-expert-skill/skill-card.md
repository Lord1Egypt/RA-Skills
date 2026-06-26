## Description: <br>
Gorm Expert helps agents support GORM v2 development with code review, SQL and model generation, performance analysis, connection-pool sizing, migrations, observability, session safety, sharding, caching, and multi-tenant patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lynnss-ai](https://clawhub.ai/user/lynnss-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to review and improve Go applications that use GORM v2, including query tuning, transaction handling, indexing, migrations, model scaffolding, observability, and multi-tenant data access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Observability examples could expose debug or profiling endpoints if copied directly into production. <br>
Mitigation: Keep pprof and similar debug endpoints bound to localhost or protected behind strong administrator-only access controls. <br>
Risk: Session reuse or multi-tenant query examples may lead to query-isolation mistakes if adopted without validation. <br>
Mitigation: Verify GORM session cloning and tenant-filter behavior against the deployed GORM version with focused tests before production use. <br>
Risk: Bundled helper scripts can generate code, SQL, benchmark templates, and scaffold files. <br>
Mitigation: Run scripts as local developer tools, review generated output before applying it, and use explicit output paths or dry-run modes where available. <br>


## Reference(s): <br>
- [Reference Index](references/README.md) <br>
- [Base Model Pattern](references/base-model-pattern.md) <br>
- [Association Loading](references/association.md) <br>
- [Caching](references/caching.md) <br>
- [Clause and Upsert](references/clause.md) <br>
- [Concurrency](references/concurrency.md) <br>
- [Indexing](references/indexing.md) <br>
- [Migration](references/migration.md) <br>
- [Observability](references/observability.md) <br>
- [Session Safety](references/session.md) <br>
- [Sharding](references/sharding.md) <br>
- [Testing](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples; scripts may also emit JSON, SQL, Go code, or generated files when explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local Python helper scripts for static analysis, model generation, query review, migration SQL, benchmark templates, scope generation, connection-pool advice, and project scaffolding.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
