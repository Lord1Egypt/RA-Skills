## Description:

Produce, consume, and manage Kafka topics with lag monitoring and data export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Kafka CLI workflows for topic management, message production and consumption, consumer group lag checks, cluster status review, and offset inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read topic data and expose messages or offsets from Kafka clusters.

Mitigation: Use least-privilege Kafka credentials and avoid consuming production topics unless authorized.

Risk: Administrative commands can change cluster state, including topic creation, topic deletion, and partition increases.

Mitigation: Review administrative commands before execution; confirm destructive operations and treat partition increases as irreversible.

## Reference(s):

- [BytesAgain](https://bytesagain.com)
- [Apache Kafka Downloads](https://kafka.apache.org/downloads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of local Kafka CLI commands against the configured Kafka bootstrap server.]

## Skill Version(s):

3.0.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
