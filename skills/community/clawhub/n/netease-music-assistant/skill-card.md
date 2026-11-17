## Description:

A NetEase Cloud Music assistant that analyzes user listening preferences, plans searches, recommends playlists, albums, and tracks, controls playback, schedules recommendation pushes, sends results through IM channels such as Feishu via OpenClaw, and can create or update playlists through ncm-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junfengl](https://clawhub.ai/user/junfengl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation agents use this skill to analyze NetEase Cloud Music preferences and produce actionable music recommendations, playback actions, scheduled pushes, and playlist-management steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled recommendation pushes can create persistent cron or plist jobs.

Mitigation: Review every scheduled job before enabling it, keep a clear list of active jobs, and provide disable and delete controls so users can revoke scheduling.

Risk: The assistant stores music preference, recommendation-history, and schedule files under the user's local configuration directory.

Mitigation: Tell users what files are created, avoid storing unnecessary personal data, and support deletion or refresh of cached preference and history data.

Risk: Recommendation content may be sent to configured IM channels such as Feishu.

Mitigation: Confirm the destination channel before pushing recommendations and let users disable IM delivery separately from local recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junfengl/skills/netease-music-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with NetEase Cloud Music links, recommendation scores and reasons, optional cover links, confirmation messages, and inline shell/configuration steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local preference, recommendation-history, and schedule JSON files; scheduled pushes may register persistent cron or plist jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
