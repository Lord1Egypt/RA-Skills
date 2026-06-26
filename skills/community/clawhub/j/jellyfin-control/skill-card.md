## Description: <br>
Control Jellyfin media server and TV. Search content, resume playback, manage sessions, control TV power and apps. Supports Home Assistant and direct WebOS backends. One command to turn on TV, launch Jellyfin, and play content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Titunito](https://clawhub.ai/user/Titunito) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to control Jellyfin playback, search media, resume content, manage playback sessions, and coordinate supported TV power or app-launch actions from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Android TV ADB backend can allow crafted app or device values to run shell commands on the host. <br>
Mitigation: Avoid or patch the direct ADB backend, keep ADB enabled only on trusted networks, and do not pass arbitrary app IDs or device values into TV launch commands. <br>
Risk: Jellyfin and Home Assistant credentials can grant media-server, smart-home, or admin capabilities. <br>
Mitigation: Use least-privilege Jellyfin and Home Assistant credentials, avoid admin Jellyfin keys unless scan or history operations are required, and keep credentials in environment configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Titunito/jellyfin-control) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local Jellyfin, Home Assistant, WebOS, or Android TV connectivity.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata, SKILL.md metadata, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
