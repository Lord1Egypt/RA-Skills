## Description: <br>
Optimize prompts for clarity and effectiveness, with optional routing to clarification, codebase research, or web research when the prompt needs more context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tolibear](https://clawhub.ai/user/tolibear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, analysts, and agent users use this skill to turn vague or underspecified requests into structured prompts with a clear role, task, constraints, and output format. It can ask clarifying questions, inspect relevant project context, or search current guidance when those paths are selected or auto-detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional codebase research can inspect relevant local project files when +deep is used or auto-detected. <br>
Mitigation: Use codebase research only when the prompt benefits from local context, and review the optimized prompt before sharing it outside the project. <br>
Risk: Optional web research can bring external guidance into the generated prompt. <br>
Mitigation: Review web-informed prompt content for accuracy and fit before using it for implementation decisions. <br>
Risk: The clipboard helper command can overwrite clipboard contents or contain badly quoted shell text. <br>
Mitigation: Inspect the generated pbcopy command before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tolibear/promptify-skill) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with an optimized prompt code block, a clipboard shell command, and a brief explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include context gathered from clarifying questions, local project files, or web research when selected or auto-detected] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
