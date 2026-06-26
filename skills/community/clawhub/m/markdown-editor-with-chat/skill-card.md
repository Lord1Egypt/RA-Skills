## Description: <br>
Lightweight markdown editor with optional OpenClaw gateway chat that serves files from a local directory without a database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and note authors use this skill to launch a local markdown editor for browsing, editing, previewing, and optionally discussing markdown files through an OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local editor can expose or modify more markdown content than users may expect. <br>
Mitigation: Install it only for a dedicated, non-sensitive markdown folder and keep the host bound to 127.0.0.1. <br>
Risk: Gateway chat can send the current document to the configured gateway. <br>
Mitigation: Enable gateway chat only when sending that document to the gateway is acceptable, and avoid using it with private notes or secrets. <br>
Risk: The security guidance calls out path boundary, markdown link sanitization, and chat disclosure/minimization work before sensitive use. <br>
Mitigation: Fix and review those areas before using the skill with private notes, credentials, or other sensitive markdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/musketyr/markdown-editor-with-chat) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, text, and local file edits through a browser-based editor] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a configured MARKDOWN_DIR; optional OpenClaw gateway settings enable chat.] <br>

## Skill Version(s): <br>
1.1.2 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
