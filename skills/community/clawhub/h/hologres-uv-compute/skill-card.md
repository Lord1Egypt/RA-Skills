## Description: <br>
Hologres UV/PV computation using Dynamic Tables and RoaringBitmap for real-time deduplication at scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design Hologres UV/PV analytics pipelines with Dynamic Tables, RoaringBitmap aggregation, flexible time-window queries, and text-to-integer UID encoding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SQL examples can create persistent Hologres tables, extensions, Dynamic Tables, refresh jobs, and UID mapping tables in a real database. <br>
Mitigation: Run examples first in a test database or with a least-privileged account, and review every CREATE, CALL, REFRESH, and mapping-table statement before execution. <br>
Risk: UID mapping tables may store user identifier mappings that are subject to privacy and retention requirements. <br>
Mitigation: Apply the organization's privacy, retention, and access-control rules before storing or refreshing user identifier mappings. <br>
Risk: The workflow depends on hologres-cli for SQL execution and Dynamic Table operations. <br>
Mitigation: Verify the hologres-cli package source and installed version before using generated commands against Hologres environments. <br>


## Reference(s): <br>
- [RoaringBitmap Function Reference](references/roaringbitmap-functions.md) <br>
- [Dynamic Table Configuration Patterns for UV](references/dynamic-table-patterns.md) <br>
- [Advanced UV Scenarios](references/advanced-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Hologres table definitions, Dynamic Table refresh examples, RoaringBitmap query patterns, and UID mapping guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION; package.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
