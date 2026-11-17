## Description:

Create, update, and manage Glance dashboard widgets for visual tracking, API data display, metrics, stats, and monitored items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acfranzen](https://clawhub.ai/user/acfranzen)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use Glance to create, update, arrange, refresh, and inspect dashboard widgets that surface data from APIs, credentials, local tools, webhooks, or scheduled agent collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled refreshes can give the agent recurring local command execution.

Mitigation: Enable only the refresh schedules you need, review each schedule before use, and disable background services or cron refreshes that are not required.

Risk: Widgets can reuse selected credentials for authenticated API access.

Mitigation: Use least-privilege read-only tokens where possible, avoid sharing broad personal access tokens in chat, and verify credential needs before creating or importing widgets.

Risk: One-line curl-to-bash installation can execute remote installer code.

Mitigation: Prefer manual or verified installation and review installer behavior before running it.

Risk: Imported widget packages can define refresh behavior and credential requirements.

Mitigation: Review imported widget packages before enabling them, especially before accepting refresh schedules or credential requests.

## Reference(s):

- [Glance ClawHub Skill Page](https://clawhub.ai/acfranzen/skills/glance)
- [Glance Homepage](https://github.com/acfranzen/glance)
- [Widget SDK Documentation](artifact/widget-sdk.md)
- [Dashboard Management API](artifact/dashboard-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies, JSX/TSX widget code, curl commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include widget definitions, dashboard API operations, credential setup guidance, refresh schedules, and verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
