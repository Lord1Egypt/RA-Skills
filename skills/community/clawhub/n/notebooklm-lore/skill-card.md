## Description: <br>
OpenClaw skill wrapper for installing and operating Lore (NotebookLM automation toolkit) via CLI + MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prantikmedhi](https://clawhub.ai/user/prantikmedhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate Lore for NotebookLM automation, including local setup, user-led authentication, verification, and MCP configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs and runs external, unpinned Lore and notebooklm-skill tooling. <br>
Mitigation: Review the Lore repository and notebooklm-skill package before installation, and pin trusted revisions where operational policy requires reproducibility. <br>
Risk: NotebookLM authentication creates local browser session state that may contain sensitive account access. <br>
Mitigation: Complete login manually, keep session files private, never commit cookies or browser profiles, and delete ~/.notebooklm when removing saved sessions. <br>
Risk: NotebookLM source materials handled through Lore may contain private user content. <br>
Mitigation: Keep private source materials out of commits, logs, and shared artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/prantikmedhi/notebooklm-lore) <br>
- [Lore Project Repository](https://github.com/prantikmedhi/lore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to leave NotebookLM authentication under user control and to avoid exposing session files.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
