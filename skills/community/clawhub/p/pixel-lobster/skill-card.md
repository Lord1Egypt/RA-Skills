## Description:

Pixel art desktop lobster that lip-syncs to OpenClaw TTS speech and guides users through installing, configuring, and launching the bundled Electron desktop overlay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeproai](https://clawhub.ai/user/joeproai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add a desktop avatar that animates during local TTS speech. The skill provides setup, configuration, and launch guidance for the bundled Electron app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional system-audio mode can monitor all system playback and grants media permissions for capture.

Mitigation: Keep the default tts mode unless system-wide audio reaction is required, and enable system mode only after reviewing the behavior and permissions.

Risk: The helper script installs npm dependencies before launch when node_modules is absent.

Mitigation: Review and pin npm dependencies before running npm install or the helper script in managed environments.

## Reference(s):

- [Pixel Lobster Skill on ClawHub](https://clawhub.ai/joeproai/skills/pixel-lobster)
- [JoeProAI Publisher Profile](https://clawhub.ai/user/joeproai)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation and launch of a bundled Electron desktop overlay.]

## Skill Version(s):

1.2.1 (source: server release metadata; bundled app/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
