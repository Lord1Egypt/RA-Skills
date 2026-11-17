## Description:

My Work Profile Cross Agent maintains a local, cross-agent work profile and domain knowledge base so agents can reuse relevant work context and extract durable new knowledge after conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jshxemail](https://clawhub.ai/user/jshxemail)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to give agents persistent context about their role, responsibilities, preferences, and business-domain knowledge across agent clients. It is useful when repeated work conversations should reuse durable, non-sensitive profile and domain knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to silently retaining and reusing conversation-derived profile knowledge across agents.

Mitigation: Review the skill before installation, consider setting autoUpdate=off, and periodically inspect or delete stored profile files and logs.

Risk: Persistent local profile and domain records may be inappropriate for chats involving sensitive business, personal, credential, or third-party information.

Mitigation: Avoid using the skill in sensitive chats and remove any stored files or logs that should not be retained.

## Reference(s):

- [Knowledge Record Format Specification](references/format-spec.md)
- [Extraction Examples and Scenario Demonstrations](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Markdown responses plus local Markdown and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local profile, domain, changelog, config, execution log, and error-record files under the user's home directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
