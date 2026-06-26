## Description: <br>
Interactive setup wizard for the OpenClaw Prediction Market Trading Stack that detects installed skills, walks through API key configuration, creates cron jobs for automated scanning and alerts, enables heartbeat for ambient awareness, and tests iMessage delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prediction-market operators use this skill to configure the OpenClaw prediction-market stack, validate required APIs, schedule automated scans, and route alerts to iMessage. It is intended for users who want a connected trading-intelligence workflow from installed stack skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures persistent automated prediction-market monitoring, scheduled scans, heartbeat checks, and phone alerts. <br>
Mitigation: Review cron and heartbeat schedules before enabling them, tune alert thresholds, and confirm each iMessage recipient before sending alerts. <br>
Risk: The setup flow stores trading and API credentials, including Kalshi keys, Anthropic keys, and BlueBubbles delivery credentials. <br>
Mitigation: Use revocable least-privilege API keys, keep private-key files under secure permissions such as chmod 600, and secure the ~/.openclaw configuration directory. <br>
Risk: Verbose diagnostics and troubleshooting commands can reveal raw configuration values or live secrets. <br>
Mitigation: Avoid sharing raw diagnostic output, redact secrets from logs and screenshots, and do not run diagnostics that print full live configuration unless output is controlled. <br>


## Reference(s): <br>
- [Prediction Stack Setup README](README.md) <br>
- [Validation Troubleshooting Guide](references/validation-troubleshooting.md) <br>
- [Configuration Template](config.example.yaml) <br>
- [OpenClaw Prediction Market Trading Stack](https://github.com/kingmadellc/openclaw-prediction-stack) <br>
- [Kalshi](https://kalshi.com) <br>
- [BlueBubbles](https://bluebubbles.app) <br>
- [Polygon.io](https://polygon.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML configuration examples and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation output guidance, cron setup commands, heartbeat configuration, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
