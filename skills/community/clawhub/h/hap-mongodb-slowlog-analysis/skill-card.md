## Description: <br>
Analyzes MongoDB 4.4 slow logs from pasted text or uploaded log files, groups repeated query patterns, and produces practical optimization advice with evidence-backed index guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1447443432](https://clawhub.ai/user/1447443432) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to inspect MongoDB slow-query evidence, summarize repeated slow-log patterns by namespace and query shape, and decide whether to rewrite queries or test candidate indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MongoDB slow logs can contain business data, query values, collection names, and operational details. <br>
Mitigation: Redact sensitive values before sharing logs and limit reports to the fields needed for performance analysis. <br>
Risk: Generated index commands can affect production performance, storage use, and query plans if executed without review. <br>
Mitigation: Review createIndex commands manually and test them in staging or with explain output before running them on production databases. <br>


## Reference(s): <br>
- [MongoDB 4.4 Slowlog Guidelines](references/mongodb-4.4-slowlog-guidelines.md) <br>
- [MongoDB Slow Query Optimization](https://docs-pd.mingdao.com/deployment/components/mongodb/slowQueryOptimization) <br>
- [ClawHub Skill Page](https://clawhub.ai/1447443432/hap-mongodb-slowlog-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or HTML reports with formatted query JSON and Mongo shell createIndex command blocks when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers Chinese output by default, supports English when requested, and treats DOCX or PDF export as optional local-tool conversion.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
