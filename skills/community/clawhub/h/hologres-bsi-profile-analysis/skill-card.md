## Description: <br>
Hologres BSI profile analysis helps agents guide user profile and tag calculation workflows in Hologres, including BSI table design, data import, audience selection, GMV analysis, distribution statistics, Top K queries, and bucketed parallel computation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design and operate Hologres BSI and Roaring Bitmap profile-analysis patterns for behavioral and attribute tag analysis. It is useful for generating SQL guidance, CLI commands, schema patterns, and query examples for audience selection and aggregate behavior analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose Hologres commands that modify database state, including extension installation, table creation, UID dictionary initialization, and data import. <br>
Mitigation: Review every command using `hologres sql run --write`, confirm the target instance and schema, and run write operations only with appropriate DDL or DML authorization. <br>
Risk: Generated UID dictionary, bitmap, and BSI tables can contain sensitive user-profile or behavioral data. <br>
Mitigation: Protect generated tables according to data-governance rules and limit access to approved operators and workloads. <br>
Risk: Incorrect source table names, bucket choices, or incremental maintenance assumptions can produce incomplete or misleading analysis results. <br>
Mitigation: Require users to provide source table names, validate bucket strategy against data volume and cluster size, and define an explicit maintenance process for incremental updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenbingyu/hologres-bsi-profile-analysis) <br>
- [Alibaba Cloud Hologres BSI profile analysis documentation](https://help.aliyun.com/zh/hologres/use-cases/profile-analysis-bsi-optimization-beta) <br>
- [BSI Function Reference](references/bsi-functions.md) <br>
- [BSI Table Design Patterns](references/table-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Hologres DDL, DML, read-only query examples, table design notes, and operational caveats.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
