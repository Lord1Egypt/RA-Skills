## Description: <br>
OpenClaw Diagnostics helps an agent inspect OpenClaw logs and session history to summarize runtime health, inference latency, token usage, tool-call activity, run timelines, Gateway restarts, and recent errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw runtime behavior, performance bottlenecks, token consumption, tool-call activity, errors, and per-agent activity from local logs and session files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw logs and session history, which may contain private prompts, secrets, or operational details. <br>
Mitigation: Install and run it only in OpenClaw environments you operate; prefer summary mode, use agent filters to limit scope, and redact or avoid sharing raw/full output. <br>
Risk: Advanced follow mode can temporarily change diagnostics settings, increase debug logging, and restart the OpenClaw Gateway. <br>
Mitigation: Use -f --advanced only when a Gateway restart and temporary debug logging are acceptable, and restore the original configuration after diagnostics. <br>


## Reference(s): <br>
- [Advanced mode reference](references/advanced-mode.md) <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/openclaw-diag) <br>
- [Publisher profile](https://clawhub.ai/user/wujiaming88) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown diagnostic summaries with shell command output/code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw or chunked diagnostic output from local logs and session files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
