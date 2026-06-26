## Description: <br>
Clone and analyze GitHub project code quality using DeepSeek AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woaim65](https://clawhub.ai/user/woaim65) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect public GitHub repositories for project structure, code quality, possible bugs, security issues, and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a user-supplied repository URL through a shell command. <br>
Mitigation: Use only trusted public repository URLs in a disposable environment, and revise the skill to use argument-based git execution with strict GitHub URL validation. <br>
Risk: Sampled source code and project structure may be sent to an external AI endpoint. <br>
Mitigation: Confirm user consent before remote AI submission, redact secrets before analysis, and disclose the external provider clearly to users. <br>
Risk: The security review verdict is suspicious. <br>
Mitigation: Review before installing and apply the security guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woaim65/github-code-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown analysis with repository structure, code quality notes, possible bug and security findings, and improvement suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a public GitHub repository URL and optional model name; samples repository files and can fall back to structure-only output if AI analysis fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
