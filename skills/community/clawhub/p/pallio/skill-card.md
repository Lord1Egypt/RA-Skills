## Description: <br>
Chat with Pallio AI knowledge-base personas. Ask questions against curated document collections with RAG-powered citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayx-cloud](https://clawhub.ai/user/jayx-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to chat with a configured Pallio AI persona, ask questions against curated document collections, and receive RAG-powered answers with document citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and relevant chat history are sent to Pallio's hosted service. <br>
Mitigation: Avoid entering secrets, regulated data, or sensitive personal information unless Pallio's handling of that content is acceptable for the user's environment. <br>
Risk: Free widget sessions have message limits, session expiry, and rate limits that can interrupt use. <br>
Mitigation: Handle expired or limited sessions by re-initializing when allowed, showing signup guidance when required, or using Pallio API access for higher limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayx-cloud/pallio) <br>
- [Pallio AI](https://pallioai.com) <br>
- [Pallio community personas](https://pallioai.com/community) <br>
- [Pallio API documentation](https://pallioai.com/api-docs) <br>
- [Pallio MCP Server](https://www.npmjs.com/package/@pallio/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API request examples, chat responses, and citation lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PALLIO_PERSONA_ID; widget sessions use temporary tokens, message limits, and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
