## Description:

Converts natural language questions into safe executable SQL to query Ascend PyTorch Profiler and msprof databases for performance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to inspect Ascend PyTorch Profiler and msprof databases, analyze operator, communication, and dispatch performance, and look up documented table schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The troubleshooting guide recommends chmod 644, which can expose private profiling data to other local users.

Mitigation: Remove that permission change, preserve private database permissions, and use a read-only database connection.

Risk: The documented query_profiler_db.py command cannot run because that script is missing from the package.

Mitigation: Treat the documented command as unavailable; have any replacement separately reviewed and use a trusted query executor.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ascend-profiler-db-explorer)
- [Profiler DB data format](artifact/references/profiler_db_data_format.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Verification methods](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [SQL code, Performance analysis, Schema guidance]

**Output Format:** [SQL statements with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query guidance; results are organized as Question, Evidence, and Suggestion.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
