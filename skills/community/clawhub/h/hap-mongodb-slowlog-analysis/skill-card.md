## Description:

Analyzes MongoDB 4.4 slow logs directly in conversation, groups repeated query shapes by namespace, and returns evidence-backed query, index, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1447443432](https://clawhub.ai/user/1447443432)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to analyze pasted or uploaded MongoDB slow logs, identify repeated slow query patterns, and produce practical query rewrites, index candidates, Mongo shell commands, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slow logs can contain sensitive collection names, query values, or business data.

Mitigation: Provide only logs you are comfortable sharing with the agent, and redact sensitive values when possible.

Risk: Generated createIndex commands or query rewrites may be inappropriate for a production database if applied without validation.

Mitigation: Review recommendations against MongoDB execution evidence and test changes before running commands against production.

## Reference(s):

- [MongoDB 4.4 Slowlog Guidelines](artifact/references/mongodb-4.4-slowlog-guidelines.md)
- [MongoDB 慢查询优化](https://docs-pd.mingdao.com/deployment/components/mongodb/slowQueryOptimization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with formatted JSON snippets and optional HTML content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mongo shell createIndex commands that should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
