## Description: <br>
Search open-access research papers by keyword and retrieve full metadata including title, authors, abstract, and full text by CORE ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to search CORE open-access papers and retrieve paper metadata or full text through a configured MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent through the third-party Pipeworx gateway. <br>
Mitigation: Avoid sending private research topics or sensitive queries unless the MCP provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-core-research) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [CORE API](https://api.core.ac.uk/v3) <br>
- [Pipeworx CORE Research MCP gateway](https://gateway.pipeworx.io/core-research/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with MCP server configuration JSON and research result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paper titles, authors, abstracts, metadata, and full text when available from CORE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
