## Description:

Detects fall events from RTSP camera streams using the KamiClaw cloud API without requiring a local GPU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to configure and run RTSP camera fall monitoring, receive fall alerts, and review saved alarm clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RTSP URLs and camera credentials may expose private camera access if placed directly in config files or logs.

Mitigation: Use camera-owner consent, prefer secret handling that avoids credentials in RTSP URLs when possible, and keep config.json and logs private.

Risk: Alarm clips are sent to the KamiClaw cloud API for fall analysis and may be retained according to the provider policy.

Mitigation: Tell operators that alarm clips leave the local environment, review the provider privacy policy, and disable saved clips when local retention is not needed.

Risk: Configured Feishu, Telegram, or Discord notifications can send fall-event details and optional media to third-party services.

Mitigation: Enable only required channels, restrict webhook and bot access, and confirm recipients before monitoring live cameras.

Risk: The Feishu webhook fallback can upload an image to sm.ms when Feishu app credentials are not configured.

Mitigation: Configure Feishu OpenAPI image upload credentials when inline images are needed, or disable posture image sharing for sensitive deployments.

Risk: The installer may recreate an existing conda environment named kami-fall.

Mitigation: Review the local environment before running setup.sh and preserve any existing kami-fall environment that should not be replaced.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/13681882136/skills/kami-fall-detection)
- [KamiClaw API Registration](https://kamiclaw-skill.kamihome.com)
- [KamiClaw Privacy Policy](https://kamiclaw-skill.kamihome.com/privacy)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, json, markdown]

**Output Format:** [Markdown guidance with configuration edits, shell commands, JSON alarm records, and notification setup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output may include stdout JSON, JSON Lines logs, optional MP4 alarm clips, and Feishu, Telegram, or Discord notifications.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter reports 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
