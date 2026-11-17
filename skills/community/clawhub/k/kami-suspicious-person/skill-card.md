## Description:

Detects unregistered faces loitering in sensitive areas across one or many RTSP cameras using shared ONNX face detection and recognition models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to configure and run continuous camera monitoring for unknown-face loitering events in sensitive areas. It helps produce alerts, face snapshot files, and optional push notifications when an unregistered person remains in view beyond the configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Biometric snapshots and camera feed details may expose sensitive personal information.

Mitigation: Review privacy requirements before use, restrict access to alert images and logs, and retain snapshots only for an approved operational purpose.

Risk: Configuration values and logs may contain camera URLs, bot tokens, webhook URLs, or other secrets.

Mitigation: Protect config.json and runtime logs as secrets, use dedicated low-privilege camera and bot credentials, and rotate credentials if exposure is suspected.

Risk: Installer, dependency, and model downloads introduce supply-chain risk.

Mitigation: Prefer pinned and verified installers, Python dependencies, and model files before production deployment.

Risk: Feishu image fallback can upload face snapshots to a public image host.

Mitigation: Avoid enabling Feishu unless the public image-host fallback is removed or explicitly disabled, or use approved inline image upload credentials only.

Risk: Background monitoring can continue collecting alerts beyond the operator's immediate attention.

Mitigation: Run the detector under an accountable operator, document the monitoring scope, and periodically confirm that the process, cameras, and alert destinations remain intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/13681882136/skills/kami-suspicious-person)
- [ClawHub Publisher Profile](https://clawhub.ai/user/13681882136)
- [Model Archive](https://publicfiles.xiaoyi.com/kami-suspicious-person-model.zip)
- [uv Project](https://github.com/astral-sh/uv)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Discord Developer Portal](https://discord.com/developers/applications)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell commands, configuration updates, JSON alert records, and saved face snapshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs continuously when launched; alerts are written to stdout and an inbox JSONL file, with optional Feishu, Discord, or Telegram push delivery.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
