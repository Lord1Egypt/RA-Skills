## Description:

Leveling overlay for OpenClaw Control UI (badge + XP + daily tip + level list + icons).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pureheart](https://clawhub.ai/user/pureheart)

### License/Terms of Use:


## Use Case:

OpenClaw users install this skill to add a game-like leveling badge, XP progress, daily tips, and recommended-skill prompts to the local Control UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies local OpenClaw Control UI assets.

Mitigation: Review the install script and target paths first, set OPENCLAW_UI_ASSETS_DIR when needed, and keep the timestamped backup available before refreshing the UI.

Risk: The install flow creates recurring OpenClaw jobs that run model-backed scheduled commands.

Mitigation: Install only with explicit consent for scheduled execution, review the cron entries after install, and remove or disable them when the overlay is no longer needed.

Risk: The helper tasks read local session, memory, and activity data to compute XP and level metrics.

Mitigation: Use only in environments where reading local OpenClaw activity data is acceptable, and document the data access before sharing the skill with other users.

Risk: Uninstall removes UI assets but may leave scheduled jobs or deployed workspace task files behind.

Mitigation: After uninstall, manually verify and remove PondDepth cron jobs and copied task files from the OpenClaw workspace.

Risk: The overlay renders local status, tip, news, and metrics data into the Control UI.

Mitigation: Keep these JSON sources trusted and sanitize or review rendered fields before deployment.

## Reference(s):

- [Ponddepth Levels on ClawHub](https://clawhub.ai/pureheart/skills/ponddepth-levels)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands plus JSON-backed UI asset files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an OpenClaw Control UI installation; writes local UI assets and helper JSON files when installed.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
