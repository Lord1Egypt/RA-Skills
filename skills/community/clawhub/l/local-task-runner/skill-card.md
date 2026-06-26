## Description: <br>
Executes local Node.js snippets or scripts with task logging, cleanup, and configurable timeouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d-wwei](https://clawhub.ai/user/d-wwei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run local utility code, calculations, or scripts when spawning a full subagent is unavailable or unnecessary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local Node.js code execution power on the host machine. <br>
Mitigation: Install only when local execution is intended; review code before each invocation, use trusted inputs, require confirmation, and prefer a sandboxed or disposable environment without sensitive files or secrets. <br>
Risk: Long-running or faulty snippets can consume local resources or leave temporary task files behind if cleanup fails. <br>
Mitigation: Use short timeouts appropriate to the task, inspect failures, and remove leftover files from the skill's task directory when cleanup warnings appear. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/d-wwei/local-task-runner) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text task logs with stdout, stderr, errors, and timing sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Timeout is configurable and defaults to 30000 ms; command output is capped at 5 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
