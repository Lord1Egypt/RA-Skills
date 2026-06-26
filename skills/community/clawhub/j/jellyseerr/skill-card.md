## Description: <br>
Request movies and TV shows through Jellyseerr. Use when the user wants to add media to their Plex/Jellyfin server, search for content availability, or manage media requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EricRosenberg](https://clawhub.ai/user/EricRosenberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and media server operators use this skill to search Jellyseerr, submit movie and TV requests, and monitor when requested content becomes available in Plex or Jellyfin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow stores a Jellyseerr API key in ~/.config/jellyseerr/config.json. <br>
Mitigation: Use the skill only on trusted machines, keep the config file private, and rotate the Jellyseerr API key if the host or file may have been exposed. <br>
Risk: The optional webhook setup can create a persistent unauthenticated listener on port 8384. <br>
Mitigation: Restrict the port to Jellyseerr or localhost, avoid broad firewall exposure, and add a shared secret or reverse proxy authentication before enabling webhooks. <br>
Risk: The optional installer creates background jobs or a systemd service that continue running after setup. <br>
Mitigation: Review the installer before running it with sudo, install the service only when persistent notification handling is needed, and monitor or disable the service if no longer required. <br>


## Reference(s): <br>
- [Jellyseerr Webhook Setup Guide](references/WEBHOOK_SETUP.md) <br>
- [Jellyseerr API Reference](references/api.md) <br>
- [Jellyseerr project documentation](https://github.com/Fallenbagel/jellyseerr) <br>
- [ClawHub Jellyseerr release page](https://clawhub.ai/EricRosenberg/jellyseerr) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/EricRosenberg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and cache files under ~/.config/jellyseerr and ~/.cache/jellyseerr when the user runs bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
