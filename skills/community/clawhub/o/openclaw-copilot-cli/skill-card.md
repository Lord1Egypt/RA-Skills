## Description: <br>
Run GitHub Copilot CLI through OpenClaw exec workflows to generate code, edit files, and automate shell tasks with advanced AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binotaliu](https://clawhub.ai/user/binotaliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to invoke GitHub Copilot CLI for code generation, file edits, and shell task automation from OpenClaw exec workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage broad autonomous local file, tool, and URL access through Copilot CLI options such as --allow-all or --yolo. <br>
Mitigation: Prefer narrower --allow-tool, --allow-url, and path-scoped permissions, and avoid broad access on sensitive repositories. <br>
Risk: Generated code, file edits, or shell commands may be incorrect, unsafe, or broader than intended. <br>
Mitigation: Review Copilot output, proposed edits, and commands before execution or commit. <br>
Risk: Copilot logs or shared session files may contain sensitive repository or prompt data. <br>
Mitigation: Inspect and redact logs or session files before sharing, storing, or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binotaliu/openclaw-copilot-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and generated code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable commands and file modifications depending on the prompt and granted Copilot CLI permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
