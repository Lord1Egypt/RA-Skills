## Description:

Chat with Pallio AI knowledge-base personas. Ask questions against curated document collections with RAG-powered citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayx-cloud](https://clawhub.ai/user/jayx-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to chat with public Pallio AI personas backed by curated document collections and to receive RAG answers with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and conversation history are sent to the external Pallio AI service.

Mitigation: Do not send sensitive, confidential, or regulated information unless Pallio receiving it is acceptable.

Risk: Widget sessions have free-message, session lifetime, and IP rate limits that can interrupt use.

Mitigation: Handle session expiration, message-limit, and rate-limit errors by reinitializing sessions, showing signup guidance, or retrying after the service-provided delay.

## Reference(s):

- [Pallio AI](https://pallioai.com)
- [Community Personas](https://pallioai.com/community)
- [Pallio API Documentation](https://pallioai.com/api-docs)
- [Pallio MCP Server](https://www.npmjs.com/package/@pallio/mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and citation lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may include document source titles and pages; widget sessions are time-limited, message-limited, and rate-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
