## Description:

Knowledge Chat helps agents connect to knowledge-base APIs for semantic search, contextual chat, multimodal document and image understanding, and source-aware answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franksteinwen007-git](https://clawhub.ai/user/franksteinwen007-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-work teams use this skill to connect agents to knowledge-base services, run semantic search, and support contextual chat over domain documents, images, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, images, chat history, and API keys may be sent to external or user-configured endpoints.

Mitigation: Use only organization-approved HTTPS endpoints, avoid confidential inputs unless approved, and provide credentials through scoped secrets or environment variables.

Risk: The advertised upload, login, and data-handling controls require deployment review before users rely on them.

Mitigation: Review the deployed application controls, dependency versions, and file-handling paths before production use.

## Reference(s):

- [Knowledge Base API Integration Guide](references/api_patterns.md)
- [Knowledge Chat Connector Example](references/kb_connector.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, connector code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include requests to user-configured knowledge-base and AI endpoints using user-provided credentials.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
