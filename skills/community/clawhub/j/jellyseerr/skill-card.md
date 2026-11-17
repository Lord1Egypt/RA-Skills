## Description:

Request movies and TV shows through Jellyseerr. Use when the user wants to add media to their Plex/Jellyfin server, search for content availability, or manage media requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericrosenberg](https://clawhub.ai/user/ericrosenberg)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Jellyseerr, submit movie and TV requests for Plex or Jellyfin libraries, and monitor requested media availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification setup can install a persistent Jellyseerr webhook service on the host.

Mitigation: Inspect the generated systemd unit before enabling it, run it with least privilege, and install it only on hosts intended to run this integration.

Risk: The webhook listener is unauthenticated and may be reachable on the network.

Mitigation: Bind the service to localhost or a trusted interface, place it behind HTTPS and authentication when exposed, and restrict firewall access to the Jellyseerr server.

Risk: Cron-based polling writes a temporary crontab backup and can add recurring execution.

Mitigation: Prefer the webhook service when appropriate, review crontab changes before applying them, and avoid the /tmp crontab method on shared hosts.

Risk: Automatic approval can submit media requests without manual review.

Mitigation: Keep auto_approve disabled unless automatic media approvals are intended for the deployment.

## Reference(s):

- [Jellyseerr Webhook Setup Guide](references/WEBHOOK_SETUP.md)
- [Jellyseerr API Reference](references/api.md)
- [Jellyseerr project documentation](https://github.com/Fallenbagel/jellyseerr)
- [ClawHub skill page](https://clawhub.ai/ericrosenberg/skills/jellyseerr)
- [Publisher profile](https://clawhub.ai/user/ericrosenberg)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Jellyseerr API requests, local configuration files, cached tracking data, and notification setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
