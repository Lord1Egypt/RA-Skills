## Description: <br>
Word definitions, phonetics, usage examples, synonyms, and antonyms from the Free Dictionary API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writing assistants, and education tools use this skill to look up English word definitions, phonetics, usage examples, synonyms, and antonyms through the Pipeworx dictionary service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dictionary lookup terms are sent to Pipeworx's remote gateway. <br>
Mitigation: Use the skill only when remote dictionary queries are acceptable for the words being requested. <br>
Risk: The MCP configuration fetches mcp-remote from npm through npx. <br>
Mitigation: Review and approve the npm package execution path before deploying the MCP configuration in managed environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-dictionary) <br>
- [Pipeworx Dictionary Pack](https://pipeworx.io/packs/dictionary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; dictionary tool results are returned as structured text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to the Pipeworx remote dictionary gateway; MCP configuration fetches mcp-remote from npm through npx.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
