## Description: <br>
Controls the LX Music desktop app to search and play songs, manage playback and volume, read current status and lyrics, modify favorites or dislikes, and query local playlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly14sh](https://clawhub.ai/user/ly14sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
LX Music desktop users use this skill to let an agent control local playback, search or play requested music, inspect currently playing status and lyrics, and work with local playlists through the bundled CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playlist commands can pass user-controlled playlist IDs through shell command strings. <br>
Mitigation: Avoid untrusted playlist IDs and prefer a version that replaces shell strings with argument-safe process calls. <br>
Risk: The skill can control LX Music, read current song and lyrics, read local playlist names and songs, and modify favorites or dislike state. <br>
Mitigation: Install only when this local control is acceptable, keep the LX Music API bound to localhost, and review actions before allowing playlist or library changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ly14sh/lx-music-assistant) <br>
- [LX Music CLI Commands Reference](references/commands.md) <br>
- [LX Music Open API Reference](references/open-api.md) <br>
- [LX Music Scheme URL Reference](references/scheme-url.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status reports and guidance with shell commands for the bundled Node.js and Python CLI tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local LX Music control commands, reads player status and lyrics, and may read local playlist names and songs from the LX Music desktop database.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
