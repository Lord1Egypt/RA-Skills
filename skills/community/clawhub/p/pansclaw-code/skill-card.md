## Description: <br>
PansClaw Code helps agents use the PansClaw Code CLI for AI-assisted coding tasks, interactive REPL sessions, and local or cloud model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding, refactoring, debugging, and code explanation tasks to the PansClaw Code CLI. It is most suitable when the user explicitly wants PansClaw/Claw execution rather than direct edits by the host agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can normalize permission-skipping or full-access coding-agent runs. <br>
Mitigation: Prefer read-only or workspace-write permission modes, and use permission-skipping only in isolated disposable projects where broad local changes are intentionally accepted. <br>
Risk: The skill builds and runs an external local PansClaw source tree outside the reviewed package. <br>
Mitigation: Install only after verifying that external source tree and rebuild from trusted sources before linking the local binary. <br>
Risk: Cloud provider use may require OAuth or API credentials. <br>
Mitigation: Prefer local Ollama where appropriate and keep provider credentials scoped, rotated, and out of shared logs or files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pansclaw-code) <br>
- [Quickstart](references/quickstart.md) <br>
- [CLI commands](references/commands.md) <br>
- [Model support](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local CLI that can read or modify workspace files depending on the selected permission mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
