## Description:

Detects physical conflicts such as fighting, shoving, and scuffling from one or more RTSP camera streams or local video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, facility operators, and security teams use this skill to monitor RTSP cameras or test video files for possible physical altercations and route alerts to local output or configured messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected camera frames leave the local environment for Kami conflict analysis.

Mitigation: Use the skill only with approved cameras and environments, review the privacy policy, and confirm that surveillance footage may be sent to the Kami service.

Risk: Snapshots and alert details may be sent to configured third-party channels or public image hosting.

Mitigation: Use private, approved messaging channels and avoid the Feishu sm.ms fallback unless public image hosting is acceptable.

Risk: Configuration and logs can contain sensitive camera URLs, API keys, webhooks, or alert details.

Mitigation: Protect config.json and logs with local access controls, avoid committing them, and use dedicated low-privilege camera credentials.

Risk: Setup downloads dependencies and a model artifact during installation or first run.

Mitigation: Review and pin setup dependencies and model artifacts before deployment in controlled or regulated environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13681882136/skills/kami-conflict-detection)
- [KamiClaw service](https://kamiclaw-skill.kamihome.com)
- [Kami conflict detection model bundle](https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip)
- [uv Python package manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands and JSON alert records; the detector also saves MP4 clips and JPEG snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured camera sources and a Kami API key; alerts can be emitted to stdout, an inbox file, Feishu, Discord, or Telegram.]

## Skill Version(s):

2.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
