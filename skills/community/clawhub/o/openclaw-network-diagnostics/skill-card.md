## Description: <br>
Standalone advanced network diagnostics for OpenClaw to continuously test end-to-end connectivity from OpenClaw agent to Telegram Bot API and approximate delivery to a personal Telegram client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h8kxrfp68z-lgtm](https://clawhub.ai/user/h8kxrfp68z-lgtm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run continuous OpenClaw-to-Telegram connectivity checks, collect rotating JSON diagnostics, and investigate DNS, TCP/TLS, packet loss, latency, route, MTU, timeout, and Telegram rate-limit issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens, chat identifiers, and diagnostic logs may be exposed through validation output, runtime config files, or shared log files. <br>
Mitigation: Use a dedicated Telegram test bot and chat, keep redaction enabled, protect config and log files, avoid sharing logs without masking identifiers, and avoid running validate-config on real credentials in logged terminals or CI. <br>
Risk: Continuous probes can send Telegram messages and run local network tools repeatedly. <br>
Mitigation: Review the configuration before starting the worker, keep intervals and retry settings conservative, and use the documented external-process mode for isolation from the main OpenClaw runtime. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h8kxrfp68z-lgtm/openclaw-network-diagnostics) <br>
- [Configuration example](references/config.example.json) <br>
- [OpenClaw integration options](references/openclaw-integration.md) <br>
- [AI log analysis workflow](references/ai-log-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, rotating JSONL diagnostic logs, and JSON run summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python diagnostic worker that can emit log files, summary files, and terminal status output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
