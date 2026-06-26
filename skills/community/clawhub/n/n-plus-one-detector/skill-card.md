## Description: <br>
Detect N+1 query problems in application code and ORM usage. Analyze database query patterns, find loops that generate excessive queries, and recommend fixes using eager loading, joins, batch fetching, and DataLoader patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find N+1 database query patterns in ORM-backed code, measure query counts in development or test environments, and produce prioritized recommendations for eager loading, batching, joins, or DataLoader fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime query-count examples can expose SQL and project-specific details or affect live traffic if run in production. <br>
Mitigation: Run runtime examples only in development or test environments and review generated reports before sharing them. <br>
Risk: Generated tests or middleware may not match the project's conventions, performance thresholds, or deployment model. <br>
Mitigation: Review and adapt generated code before committing or deploying it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and guidance with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL, file paths, query counts, generated test assertions, and middleware examples for review before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
