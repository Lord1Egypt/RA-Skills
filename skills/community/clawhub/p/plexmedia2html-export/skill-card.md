## Description: <br>
Exports Plex Media Library movies and TV shows as static HTML pages with multilingual output, machine-bound token obfuscation, genre filtering, and detail popups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kesuek](https://clawhub.ai/user/Kesuek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Plex server users use this skill to export a Plex media library into browsable static HTML pages with local cover images and metadata. It supports first-run configuration for server URL, token, language, and export path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved Plex tokens and exported Plex metadata may be private even when stored locally. <br>
Mitigation: Protect the config and export folders, keep the config file owner-readable only, and rotate the Plex token if the config may have been exposed. <br>
Risk: The token is obfuscated with a machine-bound key, not strongly encrypted. <br>
Mitigation: Use the obfuscation only to prevent casual snooping; consider stronger secret storage or manual token entry for higher-sensitivity environments. <br>
Risk: Using insecure mode disables SSL certificate verification. <br>
Mitigation: Avoid insecure mode except for trusted local or self-signed Plex setups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kesuek/plexmedia2html-export) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration, Shell commands] <br>
**Output Format:** [Static HTML files with local image assets, JSON configuration, and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports are saved locally; Plex token handling relies on machine-bound obfuscation rather than encryption.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
