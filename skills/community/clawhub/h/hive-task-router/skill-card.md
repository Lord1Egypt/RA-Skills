## Description:

Hive Task Router identifies task types such as web, code, data, documentation, and chat, then recommends an appropriate model and execution mode for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiongqiongcaocao](https://clawhub.ai/user/qiongqiongcaocao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill in OpenClaw environments to classify user tasks and generate recommended model and session commands for code, research, data, documentation, chat, and batch work. It is intended for configurable routing across multiple AI model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router loads a writable model validation cache as shell code.

Mitigation: Keep HIVE_CACHE_DIR private and trusted, and review or patch cache loading to parse key-value data without source execution before automated deployment.

Risk: The router prints copyable OpenClaw commands containing unescaped task and model values.

Mitigation: Do not execute printed commands automatically; shell-escape generated values or invoke OpenClaw through argument arrays.

Risk: Automatic subagent routing can delegate sensitive or high-impact tasks without additional review.

Mitigation: Treat subagent routing as opt-in for sensitive work and require a human review step before running generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiongqiongcaocao/skills/hive-task-router)
- [Publisher profile](https://clawhub.ai/user/qiongqiongcaocao)
- [Configuration guide](artifact/config.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text with shell command examples and Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes one task description at a time; batch usage repeats the same routing pattern for parallel subagent commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
