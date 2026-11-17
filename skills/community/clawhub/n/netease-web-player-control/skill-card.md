## Description:

Control NetEase Cloud Music Web in a browser. Use to (1) search and play a song by keyword, preferably artist + title, or (2) open My Music and play one of the user's own created playlists by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyunzhao](https://clawhub.ai/user/yangyunzhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide an agent in controlling the NetEase Cloud Music web player for song search playback and logged-in My Music playlist playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may operate an already logged-in NetEase Cloud Music web session and view playlist names needed to choose what to play.

Mitigation: Install only when this access is acceptable, and keep the browser session limited to the account context intended for playback.

Risk: Ambiguous short song names or similar playlist names may lead to unintended playback.

Mitigation: Confirm ambiguous matches before playback and verify that the bottom player switched to the intended song before reporting success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyunzhao/skills/netease-web-player-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance for browser-control actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an already logged-in NetEase Cloud Music web session for My Music playlist playback.]

## Skill Version(s):

0.1.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
