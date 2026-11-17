## Description:

Hologres BSI (bit-sliced index) profile analysis helps agents guide user profiling and tag calculation workflows in Hologres, including table design, data import, crowd selection, GMV analysis, tag distribution statistics, Top K queries, and bucketed parallel computation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design and operate Hologres BSI and Roaring Bitmap profile-analysis workflows for user segmentation, behavior-tag analysis, aggregate metrics, distribution statistics, and Top K queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes package installation guidance and Hologres SQL examples that may create extensions, create tables, or insert data when run in write mode.

Mitigation: Use a virtual environment, pin or verify the hologres-cli package, scope the database identity to the task, and review each hologres sql run --write command before execution.

Risk: The workflow depends on user-provided source tables, UID dictionary maintenance, and bucket choices, which can affect correctness and performance.

Mitigation: Confirm source table names, populate and maintain dws_uid_dict before BSI or Roaring Bitmap import, and tune bucketing with domain and cluster-size knowledge.

## Reference(s):

- [Hologres BSI profile analysis documentation](https://help.aliyun.com/zh/hologres/use-cases/profile-analysis-bsi-optimization-beta)
- [BSI Function Reference](references/bsi-functions.md)
- [BSI Table Design Patterns](references/table-design.md)
- [ClawHub skill page](https://clawhub.ai/wenbingyu/skills/hologres-bsi-profile-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include Hologres SQL for read-only analysis and reviewed write-mode setup or import commands.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
