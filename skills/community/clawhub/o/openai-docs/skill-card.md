## Description: <br>
Query the OpenAI developer documentation via the OpenAI Docs MCP server using CLI (curl/jq). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical agents use this skill to search and fetch official OpenAI documentation for API, SDK, ChatGPT Apps SDK, Codex, MCP integration, endpoint schema, parameter, limit, and migration questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper makes documentation queries over the network. <br>
Mitigation: Keep the default OpenAI MCP endpoint unless an override is trusted. <br>
Risk: Search or fetch queries could disclose sensitive project details. <br>
Mitigation: Do not include secrets or private project data in documentation queries. <br>
Risk: The wrapper depends on local curl and jq binaries. <br>
Mitigation: Confirm curl and jq are installed before using the skill. <br>


## Reference(s): <br>
- [OpenAI Docs MCP endpoint](https://developers.openai.com/mcp) <br>
- [Migrate to the Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with sourced documentation summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses network queries to the OpenAI Docs MCP endpoint through curl and jq; MCP_URL can override the default endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
