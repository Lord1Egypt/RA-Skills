## Description: <br>
Creates and edits PowerPoint presentations with AI-assisted workflows for layout fidelity, placeholder matching, theme preservation, and content and visual quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users and lightweight teams use this skill to create, edit, and inspect PowerPoint presentations while preserving layouts, placeholders, themes, and content quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and local presentation-file access for PowerPoint work. <br>
Mitigation: Review proposed commands before execution and run the skill only in a workspace containing presentation files intended for processing. <br>
Risk: The security summary notes command and network capabilities that are broader and less clearly scoped than the documentation suggests. <br>
Mitigation: Avoid confidential presentations and API keys unless you first confirm whether processing stays local and when external APIs, callbacks, or network access are used. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/pptx-v101-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return structured status, result data, execution timing, metadata, logs, and error fields for PowerPoint processing tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
