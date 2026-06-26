## Description: <br>
Controls the JoyCode CLI from the shell for code generation, code review, interactive programming conversations, automated coding tasks, session management, and login workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangzhixing](https://clawhub.ai/user/kangzhixing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to invoke JoyCode CLI workflows for coding help, code review, automated task execution, interactive terminal programming, and session recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-auto mode may edit project files without step-by-step approval. <br>
Mitigation: Use version control, review diffs after each session, and avoid full-auto on sensitive repositories unless autonomous code changes are acceptable. <br>
Risk: Generated code or review guidance may be incorrect or inappropriate for the project. <br>
Mitigation: Treat JoyCode output as assistant-generated suggestions and validate changes with project tests and human review before deployment. <br>
Risk: The skill includes login support for JoyCode account workflows. <br>
Mitigation: Use approved account practices and avoid entering credentials in untrusted terminal sessions. <br>


## Reference(s): <br>
- [Joycode ClawHub listing](https://clawhub.ai/kangzhixing/joycode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run JoyCode CLI commands that start interactive sessions, execute automated coding tasks, inspect diffs, review code, manage sessions, or log in.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
