## Description: <br>
Single-file Bash CLI for the *arr media stack that lets agents manage Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Tdarr from the terminal on the same machine as the services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and homelab operators use this skill to let an agent inspect and control a local media automation stack, including media search, library status, download monitoring, and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local media-stack commands that add media, pause downloads, remove torrents, refresh libraries, or delete files. <br>
Mitigation: Require explicit user confirmation before any destructive or state-changing command is executed. <br>
Risk: The install flow depends on an external Bash script referenced by the artifact. <br>
Mitigation: Review the script before installation and pin it to a trusted commit or release when possible. <br>
Risk: The setup stores service URLs and API keys in a local configuration file. <br>
Mitigation: Protect the generated config file, keep restrictive permissions, and avoid exposing it to untrusted agents or users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/media-cli-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target local media services and may require user confirmation for state-changing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
