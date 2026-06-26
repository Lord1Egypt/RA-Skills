## Description: <br>
Guides an OpenClaw agent in coordinating user-confirmed OpenCode tasks, launching them through callback helper scripts, and reporting asynchronous results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangning823-arch](https://clawhub.ai/user/wangning823-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route code analysis, code changes, operations, and testing requests to specialized agents after user confirmation. It emphasizes asynchronous OpenCode execution with callbacks, local result capture, and concise user-facing status reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release installs executable helper scripts into ~/.openclaw/scripts. <br>
Mitigation: Review the installed scripts before use and keep execute permissions limited to trusted local operators. <br>
Risk: Task metadata and results are stored locally under ~/.openclaw/task-results and may be sent through OpenClaw callbacks. <br>
Mitigation: Avoid placing secrets in task prompts, review callback destinations, and periodically clean stored task results. <br>
Risk: The wrapper script accepts a broad shell command string for callback execution. <br>
Mitigation: Prefer opencode-auto-callback.sh for normal use and reserve the wrapper for reviewed commands from trusted users. <br>
Risk: Example session keys in documentation may be copied into unintended executions. <br>
Mitigation: Replace examples with the current intended session key before running any callback command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangning823-arch/opencode-guide) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenCode callback script documentation](artifact/scripts/README-opencode-callback.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may direct agents to create local task files, run helper scripts, and review locally stored task logs and result files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
