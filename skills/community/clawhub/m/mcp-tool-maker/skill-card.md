## Description: <br>
MCP Tool Maker helps agents scan Python files for functions and generate MCP tool registration code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to convert top-level Python functions into MCP tool wrappers, optionally writing generated registration code for integration with an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integration code can add broad local import paths or wrap unintended local modules. <br>
Mitigation: Review generated files and destination paths before writes, and use the skill only with an explicit allowlist of source files. <br>
Risk: Generated MCP wrappers may expose functions that were not intended to become agent-accessible tools. <br>
Mitigation: Inspect the discovered function list and generated wrappers before adding them to an MCP server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/mcp-tool-maker) <br>
- [Bilibili Tool Use and MCP reference](https://www.bilibili.com/video/BV1vhV36ZEFu) <br>
- [Bilibili MCP agent reference](https://www.bilibili.com/video/BV1aQPrzYEhJ) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated Python files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
