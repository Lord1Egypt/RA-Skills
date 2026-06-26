## Description: <br>
Guides agents through OpenClaw data warehouse DDL creation for DWS, DWD, DIM, ADS, and ODS tables, covering workspace selection, table naming, field definitions, partitioning, storage format, and lifecycle settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiangYan0722](https://clawhub.ai/user/JiangYan0722) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to draft OpenClaw data warehouse DDL with consistent table names, fields, comments, partitions, storage formats, and TTL settings before reviewing and executing SQL in the target workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDL can target the wrong workspace, table name, partitioning, TTL, or storage settings if the requested database context is incomplete. <br>
Mitigation: Verify the target workspace, table name, partitioning, TTL, and storage settings before executing any generated SQL, especially for production databases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JiangYan0722/openclawsh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft SQL and checklist-style recommendations for review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
