## Description: <br>
Fetches OpenRouter models, presents an interactive picker, and applies selected primary, enabled, and fallback models to the user's OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ys727469926](https://clawhub.ai/user/ys727469926) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compare available OpenRouter models, select primary, fallback, and enabled models, and hot-apply those choices to local OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unauthenticated localhost apply endpoint can persistently change OpenClaw model configuration while the picker server is running. <br>
Mitigation: Install only if you trust the publisher, keep the picker running only while applying changes, review enabled models before applying, and stop the server or let the idle timeout expire after use. <br>
Risk: The apply workflow can change the primary, fallback, and enabled OpenClaw models based on UI selections. <br>
Mitigation: Review the selected primary, fallback, and enabled model lists before applying, or use the command-line fallback when explicit configuration changes are preferred. <br>
Risk: The current security guidance recommends a stronger version with request protections. <br>
Mitigation: Prefer a future version that adds a per-session token, origin checks, and server-side model allowlist validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ys727469926/openrouter-model-picker) <br>
- [config-server reference](artifact/references/config-server.md) <br>
- [OpenRouter model API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and an interactive HTML picker.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a temporary localhost service and apply OpenClaw model configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
