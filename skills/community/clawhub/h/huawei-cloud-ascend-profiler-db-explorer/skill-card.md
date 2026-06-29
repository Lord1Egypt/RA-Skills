## Description: <br>
Converts natural language questions into safe SQL for querying Ascend PyTorch Profiler and msprof databases about operator time, communication, dispatch, and related performance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to inspect Ascend profiling databases, generate bounded SQL queries, analyze operator and communication bottlenecks, and look up profiler table schemas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language and SQL execution guidance can lead to unintended profiler database access. <br>
Mitigation: Require explicit user confirmation and a specific database target before executing any SQL, and prefer read-only database access. <br>
Risk: Generated SQL can return excessive data or run expensive scans. <br>
Mitigation: Review generated SQL before execution and enforce aggregation or ORDER BY with LIMIT as described by the skill's acceptance criteria. <br>
Risk: Schema assumptions can be wrong across profiler database versions. <br>
Mitigation: Use the bundled schema helper and compare documented tables with the actual database before relying on table or column names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-ascend-profiler-db-explorer) <br>
- [Profiler DB Data Format](references/profiler_db_data_format.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include the generated SQL, row counts or result previews when queries run, and concise analysis in a question-evidence-suggestion structure.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
