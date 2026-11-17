## Description:

Animated pixel-art office where agents appear as characters that walk, sit, and interact with furniture in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanrui](https://clawhub.ai/user/xmanrui)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to launch a local Pixel Office dashboard that visualizes agents and reads OpenClaw configuration, returning local and LAN access URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs mutable remote dashboard code, including dependency installation and development-server startup.

Mitigation: Install only if the publisher and downloaded source are trusted; prefer a pinned, reviewed source revision before dependency installation or execution.

Risk: The skill may stop any process using port 3000 and remove its project directory during update fallback behavior.

Mitigation: Confirm the port and project path before running update or restart steps, especially on shared development machines.

Risk: The dashboard reads local OpenClaw configuration and advertises a LAN URL.

Mitigation: Review local configuration access and LAN exposure before use, and restrict network access when the dashboard should remain local.

## Reference(s):

- [Pixel Office ClawHub Skill Page](https://clawhub.ai/xmanrui/skills/pixel-office)
- [OpenClaw Dashboard Project](https://github.com/xmanrui/OpenClaw-bot-review)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and access URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local and LAN dashboard URLs after startup.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
