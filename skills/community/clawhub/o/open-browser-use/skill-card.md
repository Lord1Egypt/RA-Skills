## Description: <br>
Platform-neutral guidance for using Open Browser Use, the open-source Chrome automation stack for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifuryst](https://clawhub.ai/user/ifuryst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install, configure, verify, troubleshoot, and operate Open Browser Use for Chrome automation through the CLI, MCP server, SDKs, and JSON-RPC methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents that can operate a real Chrome profile, including tabs, history, downloads, clipboard, file choosers, forms, purchases, and other externally visible browser actions. <br>
Mitigation: Use a chosen Chrome profile, require explicit user approval for sensitive actions, and keep browser-control access limited to trusted agent runtimes. <br>
Risk: The local MCP or browser-control interface can expose high-privilege browser actions if made available to untrusted tools or sessions. <br>
Mitigation: Avoid exposing the interface to untrusted runtimes, use task-unique session IDs, select the intended profile explicitly, and finalize or release tabs at the end of each task. <br>


## Reference(s): <br>
- [Open Browser Use Installation](references/installation.md) <br>
- [Open Browser Use SDK And Protocol](references/sdk-and-protocol.md) <br>
- [Open Browser Use Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with CLI, TOML, JavaScript, Python, and Go snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety guidance for Chrome profile selection, user approvals, session scoping, and tab cleanup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
