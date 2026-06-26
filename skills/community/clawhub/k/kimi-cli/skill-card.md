## Description: <br>
Kimi Code CLI helps agents delegate complex coding tasks to the Kimi Code CLI for large code generation, refactoring, debugging, research implementation, and long-running interactive development work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Walkman1W](https://clawhub.ai/user/Walkman1W) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run Kimi Code CLI in quick or interactive modes for multi-file implementation, refactoring, debugging, and technical proof-of-concept tasks. It is intended for workflows where the calling agent plans and reviews while Kimi Code CLI performs code-producing work in a specified workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can turn crafted task or workdir text into unintended shell commands. <br>
Mitigation: Avoid untrusted task text or paths, use a disposable or version-controlled workdir, and review generated commands before execution. <br>
Risk: The skill runs an external logged-in Kimi CLI against user code. <br>
Mitigation: Install only when the external kimi-cli package is trusted, review all diffs, and terminate background sessions when work is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Walkman1W/kimi-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Walkman1W) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start foreground or background PTY sessions and may produce code or file changes through the external Kimi CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
