## Description: <br>
Manage and control a Mopidy music service on a NAS, including playback, volume, playlists, and local music scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Users who run Mopidy on a NAS use this skill to check player status, open the Iris web UI, control playback and volume, review playlists, and scan a local music library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes environment-specific Mopidy URLs, container names, and NAS music paths that may not match the user's setup. <br>
Mitigation: Update the Mopidy URL, public URL, Docker container or service name, and music path before use. <br>
Risk: Some suggested actions can restart containers, scan the music library, or change file permissions. <br>
Mitigation: Require explicit user confirmation and review command targets before running Docker, scan, or permission-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jesson1222-ship-it/lu-music-player) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mopidy URLs, Docker commands, local music paths, and service-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, _meta.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
