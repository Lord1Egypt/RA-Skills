## Description:

Hik-Connect Team Skill helps agents guide developers through Hik-Connect for Teams device management workflows including resource discovery, access control, image capture, video streaming, and alarm push configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hikconnectteam](https://clawhub.ai/user/hikconnectteam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage Hik-Connect for Teams devices, retrieve device and media resources, configure alarm webhooks, and run guarded access-control workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Hik-Connect credentials and high-impact device access.

Mitigation: Review credential handling before installation, rotate or verify app credentials, use least-privilege HCT credentials, and avoid main account credentials.

Risk: Token caching may expose access tokens if the runtime environment or cache location is not adequately protected.

Mitigation: Disable token caching for high-security use or move cached tokens to a private secure store with restricted permissions.

Risk: OpenAPI calls may send tokens to an unsafe or unexpected Hik-Connect area domain.

Mitigation: Validate Hik-Connect area domains before sending tokens or device requests.

Risk: Door-control, webhook, tunnel, and event-subscription actions can affect physical access or external connectivity.

Mitigation: Require explicit operator confirmation before these actions and confirm site safety before access-control operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hikconnectteam/skills/hik-connect-team-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/hikconnectteam)
- [README](README.md)
- [Root skill definition](SKILL.md)
- [Token manager documentation](lib/README_TOKEN_MANAGER.md)
- [Alarm event codes](modules/Hik-Connect_Team_Alarm/EVENT_CODES.md)
- [Resource management module](modules/Hik-Connect_Team_Resource/SKILL.md)
- [Access control module](modules/Hik-Connect_Team_ACS/SKILL.md)
- [Capture module](modules/Hik-Connect_Team_Capture/SKILL.md)
- [Video module](modules/Hik-Connect_Team_Video/SKILL.md)
- [Alarm module](modules/Hik-Connect_Team_Alarm/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of Python and Node.js helper scripts that call Hik-Connect OpenAPI services and return tabular or JSON results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
