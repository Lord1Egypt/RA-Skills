## Description:

Apache ORC columnar storage format reference. File structure with stripes and indexes, schema types with evolution rules, compression codecs (ZLIB/SNAPPY/ZSTD), orc-tools CLI, Python/Java writer APIs, Hive ACID transactions, Spark integration, and performance tuning with bloom filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill as a concise ORC reference for file structure, schema evolution, compression choices, orc-tools usage, Hive ACID behavior, Spark integration, and performance tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied Spark overwrite, Hive UPDATE/DELETE/MERGE, and compaction examples can modify or replace live data.

Mitigation: Test examples on non-production data and verify target paths and tables before using them in real systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/orc)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)
- [Apache ORC tools download referenced by skill](https://dlcdn.apache.org/orc/orc-1.9.2/orc-tools-1.9.2-uber.jar)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, SQL, Python, and Java code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-selected reference text for ORC topics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
