## Description:

Hologres UV/PV computation using Dynamic Tables and RoaringBitmap for real-time deduplication at scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design Hologres Dynamic Table pipelines for near-real-time UV/PV aggregation, bitmap-based deduplication, flexible time-range queries, and text UID encoding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL examples create, refresh, and overwrite Hologres database objects and can affect production data if executed directly.

Mitigation: Use least-privilege Hologres credentials and test CREATE, REFRESH, and OVERWRITE examples outside production before applying them to real data.

Risk: The skill depends on hologres-cli and Hologres features such as Dynamic Tables, RoaringBitmap, and hg_id_encoding_int4.

Mitigation: Install a pinned reviewed hologres-cli version and confirm the target Hologres version supports required features before using the examples.

## Reference(s):

- [Hologres Uv Compute ClawHub Page](https://clawhub.ai/wenbingyu/skills/hologres-uv-compute)
- [Publisher Profile](https://clawhub.ai/user/wenbingyu)
- [RoaringBitmap Function Reference](references/roaringbitmap-functions.md)
- [Dynamic Table Configuration Patterns for UV](references/dynamic-table-patterns.md)
- [Advanced UV Scenarios](references/advanced-scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides database setup, Dynamic Table configuration, query templates, and operational guidance.]

## Skill Version(s):

0.2.0 (source: server release metadata and VERSION; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
