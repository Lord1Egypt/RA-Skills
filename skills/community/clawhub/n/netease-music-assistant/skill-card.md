## Description: <br>
A NetEase Cloud Music assistant that analyzes listening preferences, plans search strategies, recommends playlists, albums, and songs, manages playback and scheduled recommendations, and can push results to IM channels through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JunfengL](https://clawhub.ai/user/JunfengL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get personalized NetEase Cloud Music recommendations, preference analysis, playback guidance, playlist creation assistance, and optional scheduled recommendation delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduling workflow can create persistent cron jobs for recommendation pushes. <br>
Mitigation: Inspect the exact crontab entry and script path before enabling scheduled pushes, confirm the IM destination, and keep removal steps documented for the user. <br>
Risk: The assistant may access NetEase Music listening preferences and local files under ~/.config/ncm. <br>
Mitigation: Install only when the user accepts that local preference, history, and schedule files may be read or updated for recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JunfengL/netease-music-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with links, ratings, rationale, optional cover URLs, and inline shell commands or JSON configuration when scheduling is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local NetEase Music preference, history, and schedule files under ~/.config/ncm; scheduled delivery may require cron registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
