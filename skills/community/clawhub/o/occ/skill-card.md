## Description: <br>
Control OpenCode to execute development tasks and manage OpenCode sessions through a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongxh13](https://clawhub.ai/user/gongxh13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query, create, and continue OpenCode development sessions from command-line workflows or external automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may automatically run npm dependency installation under the user's account. <br>
Mitigation: Install only when the publisher and local npm environment are trusted, and review package installation effects before using the skill in sensitive environments. <br>
Risk: OpenCode sessions operate in the directory where the command is run and may change project files. <br>
Mitigation: Run commands only from the intended project directory, keep version control available, and review resulting code changes before accepting them. <br>


## Reference(s): <br>
- [OCC ClawHub Release](https://clawhub.ai/gongxh13/occ) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; command output is JSON or text from OpenCode sessions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local OpenCode server and create or continue sessions in the current working directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
