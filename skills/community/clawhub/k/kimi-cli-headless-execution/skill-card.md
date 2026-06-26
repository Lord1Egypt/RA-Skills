## Description: <br>
教 OpenClaw 在自动化脚本、后台任务、CI/CD、无 TTY 环境等非交互场景中，正确使用 Kimi Code CLI 的 `-p/--prompt`、`--print`、`--quiet`、`--wire` 等参数完成无头执行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to construct, run, and handle Kimi CLI headless commands in scripts, background jobs, CI/CD pipelines, and other non-interactive environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Headless Kimi CLI execution can automatically modify files or run shell commands when `--yolo` is enabled. <br>
Mitigation: Require explicit user confirmation before enabling automatic approval, avoid critical system directories, and set a narrow `--work-dir` for project-scoped tasks. <br>
Risk: The skill may require Kimi authentication or API credentials to run commands successfully. <br>
Mitigation: Grant only the credentials needed for Kimi CLI use and verify authentication with `kimi --version`, `which kimi`, or login/configuration checks before execution. <br>
Risk: Non-interactive output can be incomplete, noisy, or difficult to parse when the wrong mode is selected. <br>
Mitigation: Choose `--quiet`, `--print`, or `--print --output-format stream-json` based on the task, check the exit code, and fall back to a simpler output mode when parsing fails. <br>


## Reference(s): <br>
- [Source skill definition](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/aiyouwolegequ/kimi-cli-headless-execution) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash code blocks and structured result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include constructed_command, execution_result, exit_code, warnings, and next_steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
