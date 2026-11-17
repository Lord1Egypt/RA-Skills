## Description:

Search and download movies via Jackett and qBittorrent, with automatic subtitle download support using SMB integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger0808](https://clawhub.ai/user/roger0808)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search torrent indexers through Jackett, add selected movie downloads to qBittorrent, and fetch or upload subtitles to NAS storage over SMB. Users are responsible for ensuring downloads are authorized and lawful in their deployment context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled real-looking credentials may expose SMB, Jackett, or qBittorrent access.

Mitigation: Remove bundled credentials before installation, rotate any exposed secrets, and require users to provide credentials through a private environment file or secret store.

Risk: Plain HTTP service URLs for Jackett and qBittorrent can expose credentials or control traffic on untrusted networks.

Mitigation: Use HTTPS where supported, or restrict access to a trusted isolated network or VPN.

Risk: Privileged mount workflows and destructive torrent or file operations can damage local or NAS data.

Mitigation: Disable sudo mount flows by default and require exact, confirmed, reversible deletion or archive behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roger0808/skills/nas-movie-download)
- [Publisher profile](https://clawhub.ai/user/roger0808)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration notes, and script-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that interact with Jackett, qBittorrent, SMB shares, local files, and subtitle download tools.]

## Skill Version(s):

3.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
