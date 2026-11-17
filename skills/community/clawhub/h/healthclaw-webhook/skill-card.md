## Description:

Streams Apple Health data through a self-hosted webhook so OpenClaw agents can analyze health trends, calculate recovery scores, detect anomalies, and send alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crxiaobailiu-gif](https://clawhub.ai/user/crxiaobailiu-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use HealthClaw to connect iPhone and Apple Watch health metrics to a local webhook, then configure agents to query health logs, compute daily recovery scores, and send anomaly alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health data may be exposed if the webhook service, admin routes, or remote tunnel are made publicly reachable without strong safeguards.

Mitigation: Use a pinned, verified server release, require a strong ADMIN_TOKEN, restrict public tunnels, and avoid exposing admin routes.

Risk: Local health records can be sensitive if the data directory is readable by unintended users or processes.

Mitigation: Protect the local health-data directory and use isolated per-user data directories when configuring multiple users or devices.

Risk: Discord alerts or recurring jobs may disclose health-derived details outside the local environment.

Mitigation: Enable Discord alerts and recurring jobs only after reviewing what details will be shared and who can access the notification channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crxiaobailiu-gif/skills/healthclaw-webhook)
- [Artifact metadata homepage](https://github.com/sprausliu/healthclaw)
- [Recovery score example](artifact/examples/recovery-score.md)
- [Health alerts example](artifact/examples/health-alerts.md)
- [Tailscale Funnel documentation](https://tailscale.com/download)
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [HealthClaw TestFlight beta](https://testflight.apple.com/join/SXDjT6vC)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce recovery-score summaries, alert messages, OpenClaw cron configuration, and setup commands based on local health data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
