## Description: <br>
Generates PowerPoint presentations from topics or documents, with support for slide planning, templates, layouts, charts, and basic single-task personal workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create simple PPTX presentations from a topic, source document, or business-report prompt. It is positioned as a free edition for personal daily use and single-task workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write local PPTX files and may overwrite existing outputs if paths are unclear. <br>
Mitigation: Use an explicit output path and review before allowing file writes. <br>
Risk: The skill may require package installation or command execution to generate presentations. <br>
Mitigation: Review dependency installation and shell commands before execution. <br>
Risk: Source documents used for presentation generation may contain sensitive information. <br>
Mitigation: Avoid providing sensitive documents unless the agent environment is trusted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/presentation-gen-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, Python, YAML, and JSON examples; expected generated artifact is a local PPTX file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install Python dependencies and write local presentation files when the agent is granted execution and filesystem access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
