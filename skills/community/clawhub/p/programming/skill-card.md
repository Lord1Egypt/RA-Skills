## Description: <br>
Provides programming guidance, including coding workflow, code review, optimization, and technical decision support based on task description and context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leowing](https://clawhub.ai/user/leowing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to retrieve programming workflow, Claude CLI usage, and code review guidance for development, debugging, optimization, project design, and technical decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples show piping local files or prompts to an external AI command-line service, which can expose secrets, credentials, private customer data, or proprietary code if used without review. <br>
Mitigation: Confirm organizational approval before sending local content to external AI services, and avoid including sensitive data in prompts or piped file content. <br>
Risk: Generated code or optimization suggestions may be incorrect, insecure, or unsuitable for the target project. <br>
Mitigation: Write generated code to a temporary file, review changes before replacing existing files, and run the project's tests and security checks before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leowing/programming) <br>
- [Programming Skill](artifact/SKILL.md) <br>
- [Claude CLI Programming Guide](artifact/claude_cli_guide.md) <br>
- [Programming Workflow Guide](artifact/workflow_guide.md) <br>
- [Code Review and Optimization Guidance](artifact/code_review_optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns bundled reference guidance selected by command mode; no external dependencies are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
