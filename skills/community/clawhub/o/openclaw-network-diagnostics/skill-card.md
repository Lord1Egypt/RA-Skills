## Description:

Standalone advanced network diagnostics for OpenClaw to continuously test end-to-end connectivity from OpenClaw agent to Telegram Bot API and approximate delivery to a personal Telegram client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h8kxrfp68z-lgtm](https://clawhub.ai/user/h8kxrfp68z-lgtm)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run an isolated OpenClaw-to-Telegram diagnostic worker for investigating latency spikes, packet loss, DNS instability, TCP/TLS failures, route changes, MTU shifts, retry behavior, timeout behavior, and Telegram rate limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot credentials or chat identifiers can be exposed through configuration, validation output, runtime configuration files, or logs.

Mitigation: Use only controlled bot and chat credentials, keep redaction enabled, protect or minimize log files, and rotate the bot token if validation output or runtime config files may have exposed it.

Risk: The worker sends live Telegram Bot API requests and diagnostic messages.

Mitigation: Run it only against Telegram bots and chats you control, and keep telegram_api_host set to api.telegram.org unless another endpoint is intentionally trusted.

Risk: The background mode can run as a persistent network worker.

Mitigation: Prefer foreground mode for testing, verify pid-file lifecycle handling before background deployment, and stop the worker when diagnostics are complete.

Risk: Proxy overrides can create plaintext runtime configuration behavior.

Mitigation: Avoid --proxy until that behavior is fixed, or use it only in a controlled environment with protected runtime configuration files.

## Reference(s):

- [Configuration Example](artifact/references/config.example.json)
- [OpenClaw Integration Options](artifact/references/openclaw-integration.md)
- [AI Log Analysis](artifact/references/ai-log-analysis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration, and JSON/JSONL diagnostic artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The diagnostic worker can emit rotating JSONL logs and a summary JSON file.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
