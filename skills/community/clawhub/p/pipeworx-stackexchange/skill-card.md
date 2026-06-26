## Description: <br>
Search and retrieve questions and answers from any StackExchange site, including StackOverflow, ServerFault, SuperUser, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search StackExchange sites and retrieve question or answer content for technical research, troubleshooting, and Q&A context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Pipeworx's gateway rather than directly to StackExchange. <br>
Mitigation: Avoid sending private or sensitive queries through the service. <br>
Risk: Returned Q&A HTML is untrusted reference content. <br>
Mitigation: Review returned content before acting on it and verify important answers against the linked source posts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-stackexchange) <br>
- [Pipeworx StackExchange MCP endpoint](https://gateway.pipeworx.io/stackexchange/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with StackExchange question and answer fields, plus optional MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned question and answer bodies may include HTML and should be treated as untrusted reference content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
