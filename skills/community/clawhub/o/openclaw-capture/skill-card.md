## Description: <br>
Wrap a local openclaw_capture_workflow checkout as an OpenClaw/ClawHub skill that captures links, text, images, and videos, routes STT by platform, and fans results out to Telegram and Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Etherstrings](https://clawhub.ai/user/Etherstrings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to dispatch URL, pasted text, image, video, or mixed capture payloads into a local OpenClaw workflow while selecting speech-to-text and notification routing through environment settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured content, transcripts, or summaries may be sent to configured backend, model, Telegram, or Feishu services. <br>
Mitigation: Use only trusted service endpoints and destinations, configure dedicated low-privilege credentials, and avoid submitting sensitive content unless those services are approved for it. <br>
Risk: A configured local STT command can execute local software during transcription. <br>
Mitigation: Set OPENCLAW_CAPTURE_LOCAL_STT_COMMAND only to a trusted executable or leave it unset to avoid local command execution. <br>
Risk: Implicit invocation is enabled, so capture dispatch may run with less explicit user confirmation. <br>
Mitigation: Prefer explicit invocation for deployments that handle sensitive content or route results to external notification channels. <br>


## Reference(s): <br>
- [Runtime Profiles](references/runtime-profiles.md) <br>
- [Module Matrix](references/module-matrix.md) <br>
- [Payload Contract](references/payload-contract.md) <br>
- [OpenClaw Capture on ClawHub](https://clawhub.ai/Etherstrings/openclaw-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash snippets and JSON payloads; runtime output is a JSON job object plus text or Markdown summaries sent to configured destinations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires environment configuration for the local workflow, backend mode, model provider, STT routing, and Telegram or Feishu notification destinations.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
