## Description: <br>
Windows剪贴板管理器 helps agents manage Windows clipboard content with copy, paste, history, multi-entry storage, search, and formatting utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and Windows users can use this skill to generate clipboard-management code and commands for reading, writing, formatting, searching, and organizing clipboard content. It is suited for data cleanup, batch text transformations, code snippet handling, and cross-application data exchange. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard operations can expose passwords, API keys, financial data, private messages, or other sensitive copied content. <br>
Mitigation: Use the skill only when clipboard access is intended, avoid history or monitoring while copying sensitive data, stop monitoring promptly, and clear stored clipboard history when no longer needed. <br>
Risk: Generated clipboard scripts depend on local Python packages and may behave differently across Windows environments. <br>
Mitigation: Install pyperclip and Pillow from a trusted Python environment, review generated code before execution, and test clipboard behavior with non-sensitive sample data first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-clipboard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include clipboard operation reports, history summaries, slot listings, and dependency installation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata, released 2026-04-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
