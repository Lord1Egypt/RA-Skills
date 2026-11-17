## Description:

Control Nest smart home devices (thermostat, cameras, doorbell) via the Device Access API. Use when asked to check or adjust home temperature, view camera feeds, check who's at the door, monitor rooms, or set up temperature schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amogower](https://clawhub.ai/user/amogower)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect and control Nest thermostats, cameras, and doorbells through Google's Smart Device Management API. It also supports setup guidance for real-time Nest events, including doorbell and person alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose an always-on Nest event webhook through Cloudflare.

Mitigation: Require authenticated Pub/Sub push validation and restrict the endpoint before enabling external delivery.

Risk: Doorbell and person events can send camera snapshots and activity alerts to Telegram.

Mitigation: Use explicit opt-in for camera and third-party alerting paths, and confirm the recipient chat and bot token before deployment.

Risk: The workflows depend on long-lived credentials and tokens for Nest, Clawdbot, Telegram, and 1Password.

Mitigation: Store secrets in restricted secret files or systemd credentials, rotate them when exposed, and avoid passing the full environment to subprocesses.

Risk: The setup downloads cloudflared from a latest-release URL.

Mitigation: Pin the intended cloudflared version and verify the downloaded binary before installing or running it as a persistent service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amogower/skills/nest-devices)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Nest Device Access Console](https://console.nest.google.com/device-access)
- [Cloudflare cloudflared Download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, Python, YAML, and systemd snippets; operational scripts emit JSON for device commands and status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Google Smart Device Management APIs, 1Password, Cloudflare Tunnel, Clawdbot hooks, Telegram, and ffmpeg depending on the selected workflow.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
