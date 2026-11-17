## Description: <br>
PPT 中文工具基础版 helps agents create and edit Chinese PowerPoint presentations, including Chinese layout optimization, localized templates, content checks, and font or spacing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to direct an agent through lightweight Chinese presentation creation, editing, layout review, and localized formatting tasks for individual PowerPoint workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local presentation files, run local commands, use API keys, and contact external APIs. <br>
Mitigation: Install only in an agent environment where those capabilities are expected, scoped, and reviewable before execution. <br>
Risk: The artifact includes local-only privacy claims while the security evidence reports external API or network behavior. <br>
Mitigation: Treat privacy claims as unverified until the publisher clarifies which actions are local and which may send content over the network. <br>
Risk: Broad command-capable instructions can affect local files or environment configuration. <br>
Mitigation: Review proposed commands, file reads, and configuration changes before allowing the agent to execute them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pptx-cn-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets; task results may be returned as structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to read local presentation files, run local commands, use API keys, and contact external APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
