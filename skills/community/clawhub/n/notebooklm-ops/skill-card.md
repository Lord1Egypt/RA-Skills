## Description: <br>
Manage NotebookLM MCP authentication lifecycle on Linux by automating GUI startup, auth refresh, status checks, smoke tests, and cleanup when Google session cookies expire frequently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Spiceman161](https://clawhub.ai/user/Spiceman161) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators managing a Linux-hosted NotebookLM MCP setup use this skill to start and stop the browser GUI stack, refresh Google authentication, and run status or smoke checks when cookies expire frequently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Google browser session through CDP/VNC. <br>
Mitigation: Use a dedicated Chromium profile and preferably a dedicated Google account, and restrict CDP and VNC access to trusted local users only. <br>
Risk: Sensitive work is delegated to host-local helper scripts that are not included in the package. <br>
Mitigation: Inspect and trust the external helper scripts under /home/moltuser/clawd before running the skill. <br>
Risk: The GUI/browser stack may remain active after use. <br>
Mitigation: Run the OFF workflow after use to stop Chromium, x11vnc, Xvfb, openbox, and related leftovers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Spiceman161/notebooklm-ops) <br>
- [Google NotebookLM](https://notebooklm.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational guidance for NotebookLM MCP auth refresh, status checks, smoke tests, and shutdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
