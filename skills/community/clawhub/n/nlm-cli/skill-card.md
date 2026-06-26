## Description: <br>
NLM CLI helps agents operate NotebookLM through Jacob Brown's `notebooklm-mcp-cli`, covering notebooks, sources, Studio generation, research, sharing, MCP setup, and content downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FelixHsp](https://clawhub.ai/user/FelixHsp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need NotebookLM automation through the `nlm` command, including notebook and source management, Studio artifact generation, sharing, MCP setup, and downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapped NotebookLM CLI can change or share notebook content through the user's active NotebookLM or Google session. <br>
Mitigation: Verify the active profile, target notebook, recipients, and sharing status before running share, invite, delete, source import or sync, download, MCP setup, or skill install commands. <br>
Risk: The skill depends on the external `notebooklm-mcp-cli` package and the local `nlm` executable resolved by the wrapper. <br>
Mitigation: Install only if the package is trusted in the target environment, and confirm `NLM_BIN`, local virtual environment, or PATH resolution before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FelixHsp/nlm-cli) <br>
- [CLI command reference](references/cli-commands.md) <br>
- [Install and authentication guide](references/install-and-auth.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide execution of NotebookLM CLI commands that create, modify, share, delete, or download notebook content.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
