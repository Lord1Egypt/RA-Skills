## Description: <br>
Image Vision uses local Ollama vision models to turn image files or screenshots into text descriptions that text-only coding assistants can reason over. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duchenyu](https://clawhub.ai/user/duchenyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze screenshots, UI mockups, document scans, charts, and code images inside text-only assistant workflows. It is intended for local image understanding through Ollama when users explicitly request image analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README includes an Ollama install command that pipes a remote script into the shell. <br>
Mitigation: Use an official installer or trusted package manager, or inspect the downloaded install script before executing it. <br>
Risk: Images analyzed by the skill are read from disk and sent to a local Ollama service. <br>
Mitigation: Run the skill only against images appropriate for local processing and confirm the Ollama endpoint is the intended local service. <br>
Risk: The optional clipboard helper can save clipboard screenshots locally and copy saved paths to the clipboard. <br>
Mitigation: Review or delete saved screenshots when they contain sensitive content, and use the no-clipboard option when path copying is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duchenyu/skills/image-vision-bridge) <br>
- [Ollama](https://ollama.com) <br>
- [qwen3.5 model library](https://ollama.com/library/qwen3.5) <br>
- [Python](https://python.org) <br>
- [DeepSeek](https://deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text image descriptions with optional Markdown and shell-command guidance from the assistant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads an image path and optional model or prompt arguments; output quality depends on the selected local vision model.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
