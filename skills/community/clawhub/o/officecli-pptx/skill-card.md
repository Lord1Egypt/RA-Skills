## Description: <br>
Use this skill when a .pptx file is involved, including creating, reading, extracting from, editing, combining, splitting, or updating presentation decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other agent users use this skill to create, inspect, edit, validate, and QA PowerPoint presentations through officecli commands and presentation-specific workflow guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to download and run installer or updater scripts before using officecli. <br>
Mitigation: Review the installer path before deployment, prefer a trusted pinned installation of officecli, and disable automatic curl/bash or PowerShell updater execution unless explicitly approved. <br>
Risk: Remote URL fetching and raw XML edits can introduce unintended content or corrupt important presentations. <br>
Mitigation: Use local image files where possible, approve remote fetching intentionally, and work on copies of important decks before raw XML operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iceyliu/officecli-pptx) <br>
- [Publisher profile](https://clawhub.ai/user/iceyliu) <br>
- [Creating presentations guide](artifact/creating.md) <br>
- [Editing presentations guide](artifact/editing.md) <br>
- [OfficeCLI releases endpoint](https://api.github.com/repos/iOfficeAI/OfficeCLI/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and officecli command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify .pptx files through officecli when an agent follows the guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
