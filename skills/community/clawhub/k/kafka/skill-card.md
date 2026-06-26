## Description: <br>
Produce, consume, and manage Kafka topics with lag monitoring and data export for publishing messages, consuming topics, and monitoring consumer lag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect Kafka clusters, manage topics, produce and consume messages, check consumer group lag, and review offsets from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can consume messages from Kafka topics, which may expose sensitive data. <br>
Mitigation: Use least-privilege Kafka credentials and require explicit review before consuming sensitive topics. <br>
Risk: The skill can produce messages, delete topics, and increase partitions when those commands are invoked. <br>
Mitigation: Point KAFKA_BOOTSTRAP and KAFKA_CONFIG_FILE only at the intended cluster and require explicit production review before mutating Kafka state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/kafka) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>
- [Apache Kafka downloads](https://kafka.apache.org/downloads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kafka CLI tools and caller-provided Kafka connection configuration.] <br>

## Skill Version(s): <br>
3.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
