## Description: <br>
openclaw观测平台 - 基于 Apache Doris 的日志分析与监控 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[never112](https://clawhub.ai/user/never112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install the opsrobot observability platform with Docker Compose and configure OpenClaw log and OpenTelemetry metrics collection into Apache Doris. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostics configuration can store full prompts, messages, and system context in the observability backend. <br>
Mitigation: Enable includePrompt, includeMessages, or includeSystem only when that collection is intentional, protected by trusted transport and restricted access, and governed by retention and redaction controls. <br>
Risk: The setup requires running a Docker Compose repository referenced by the skill. <br>
Mitigation: Review the repository and compose configuration before running the services. <br>
Risk: The skill includes an unrelated request to star the upstream GitHub repository. <br>
Mitigation: Treat the star request as optional promotion and ignore it unless the user independently chooses to do it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/never112/opsrobot) <br>
- [opsrobot GitHub repository](https://github.com/opsrobot-ai/opsrobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker Compose commands, Vector configuration guidance, and OpenClaw diagnostics configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
