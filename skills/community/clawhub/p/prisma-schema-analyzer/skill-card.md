## Description: <br>
Analyze Prisma schemas for performance, relation design, index strategy, migration safety, and query optimization for production readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Prisma schema files, migrations, and related Prisma Client usage for indexing, relation design, query performance, and migration-safety issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect Prisma schemas, migrations, and relevant application source files. <br>
Mitigation: Use it only in repositories where the agent is allowed to read those files, and review findings before applying schema or code changes. <br>
Risk: Prisma CLI commands can interact with project datasource settings or unpinned tooling. <br>
Mitigation: Review each Prisma command before approval, use non-production DATABASE_URL values, and prefer pinned Prisma tooling in controlled environments. <br>


## Reference(s): <br>
- [Prisma Schema Analyzer on ClawHub](https://clawhub.ai/charlie-morrison/prisma-schema-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with issue lists, schema metrics, and suggested Prisma changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, Prisma schema snippets, severity groupings, and command suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
