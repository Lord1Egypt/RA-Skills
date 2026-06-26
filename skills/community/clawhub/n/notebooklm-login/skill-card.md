## Description: <br>
Login to Google NotebookLM via Chrome DevTools Protocol and save auth cookies for notebooklm-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ou-rock](https://clawhub.ai/user/ou-rock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to authenticate NotebookLM MCP when normal CLI login is missing, expired, or fails in a non-standard environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores reusable Google session cookies in a local NotebookLM MCP profile. <br>
Mitigation: Run it only on a trusted machine and protect or delete ~/.notebooklm-mcp-cli/profiles/default/ when the reusable profile is no longer needed. <br>
Risk: A debug-enabled Chromium session exposes browser automation while the login window is open. <br>
Mitigation: Avoid shared environments during login, then close or kill Chromium after authentication completes. <br>
Risk: The documented uv installation command fetches and executes a remote installer. <br>
Mitigation: Prefer a verified uv installation method before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ou-rock/notebooklm-login) <br>
- [uv installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell commands and a Python helper script that creates local profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local NotebookLM MCP profile containing cookies.json and metadata.json after user login.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
