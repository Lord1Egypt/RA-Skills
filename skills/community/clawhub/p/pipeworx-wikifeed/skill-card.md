## Description: <br>
Provides curated Wikipedia content including historical events on a date, daily featured articles, most read pages, and picture of the day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query a Pipeworx remote MCP service for curated Wikipedia feed content, including historical date entries, featured articles, most-read pages, and picture-of-the-day metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wikipedia lookup queries are sent to Pipeworx's remote MCP service, and the artifact does not document service logging or retention practices. <br>
Mitigation: Use the skill only for non-sensitive lookup prompts and avoid including private context when calling the remote service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-wikifeed) <br>
- [Pipeworx Wikifeed MCP endpoint](https://gateway.pipeworx.io/wikifeed/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote MCP endpoint for Wikipedia feed lookups; avoid sending private context in lookup prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
