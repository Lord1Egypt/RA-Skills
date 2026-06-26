## Description: <br>
Safe Exec Wrapper helps agents wrap untrusted shell-command output with UUID-based boundaries to reduce prompt-injection risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmceleney](https://clawhub.ai/user/jmceleney) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when running commands that may return external or user-controlled data, such as API responses, CLI service queries, or untrusted files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper labels command output as untrusted, but it does not sandbox the wrapped command or prevent command side effects. <br>
Mitigation: Review commands before passing them to safe-exec, especially commands that modify files, contact services, or use credentials. <br>
Risk: Predictable or reused boundary identifiers could weaken the prompt-injection boundary model. <br>
Mitigation: Use the default random UUID mode for normal use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jmceleney/openclaw-safe-exec) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed wrapper emits UUID-labeled stdout, stderr, and exit-code boundaries around command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
