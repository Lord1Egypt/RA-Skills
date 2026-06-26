## Description: <br>
NotebookLM CLI for listing notebooks, creating notebooks, adding sources, querying notebooks, generating studio artifacts, downloading outputs, sharing notebooks, setting up MCP integrations, and diagnosing auth/install issues when working with the `nlm` command or automating NotebookLM from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsuper](https://clawhub.ai/user/lsuper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Google NotebookLM from a terminal: set up authentication, manage notebooks and sources, query notebooks, generate or download studio artifacts, configure MCP integrations, and troubleshoot install/auth issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploading local files, pasted text, URLs, or Drive sources can expose sensitive content to NotebookLM. <br>
Mitigation: Confirm each source is appropriate for NotebookLM before upload or sync. <br>
Risk: Public links, editor invitations, or the wrong active profile can expose notebook content or grant unintended access. <br>
Mitigation: Check the active profile and notebook sharing state before enabling public links or inviting collaborators. <br>
Risk: Browser-session authentication and MCP setup can let other agents act through the connected NotebookLM account. <br>
Mitigation: Install only trusted packages, verify the active account session, and add MCP access only for agents that should use that account. <br>


## Reference(s): <br>
- [NotebookLM MCP CLI project homepage](https://github.com/jacob-bd/notebooklm-mcp-cli) <br>
- [ClawHub nlm skill page](https://clawhub.ai/lsuper/nlm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples for `nlm`, MCP setup, sharing controls, source management, and authentication troubleshooting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
