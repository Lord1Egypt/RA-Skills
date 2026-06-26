## Description: <br>
Searches for movie torrents through Jackett, submits downloads to qBittorrent, and supports SMB-based subtitle retrieval for NAS-stored videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roger0808](https://clawhub.ai/user/Roger0808) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate movie torrent search, qBittorrent download submission, NAS storage workflows, and subtitle retrieval through SMB-connected storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled credentials and API keys may expose NAS, Jackett, qBittorrent, or subtitle-service access. <br>
Mitigation: Remove bundled secrets before installation, rotate any exposed credentials, and replace them with least-privilege accounts managed outside the skill files. <br>
Risk: The skill can broadly modify NAS content and qBittorrent state, including archive workflows and delete behavior. <br>
Mitigation: Run only in a controlled environment after reviewing SMB mount helpers, archive scripts, --all subtitle workflows, and qBittorrent deletion paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Roger0808/nas-movie-download) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Roger0808) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in NAS file writes, subtitle files, qBittorrent actions, and download-management status from the bundled scripts.] <br>

## Skill Version(s): <br>
3.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
