## Description:

Skill for the Meta Business CLI. Complete WhatsApp, Instagram, Facebook Pages, and Messenger automation via the Graph API. Supports messaging, media, templates, analytics, webhooks, and systemd service management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adolago](https://clawhub.ai/user/adolago)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run Meta Business CLI workflows for Graph API automation across WhatsApp, Instagram, Facebook Pages, and Messenger. It helps agents configure credentials, send and manage messages and media, inspect analytics, handle webhooks, run diagnostics, and manage a systemd webhook service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unaudited CLI code that can access Meta business assets.

Mitigation: Install only when the publisher is trusted, and prefer a pinned, reviewed release or verified source commit.

Risk: The CLI handles powerful Meta credentials and may expose secrets through shared terminals, logs, or weak local file permissions.

Mitigation: Avoid entering production secrets in shared terminals or logs, and review permissions on `~/.meta-cli/config.json`.

Risk: Webhook forwarding and systemd service use can process message data through a long-running service.

Mitigation: Enable webhook forwarding or the service only after reviewing what data will be sent and how to stop or uninstall the service.

## Reference(s):

- [Meta Business CLI ClawHub skill](https://clawhub.ai/adolago/skills/meta-business)
- [Meta CLI source repository from install metadata](https://github.com/adolago/meta-cli.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, setup steps, configuration keys, and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill recommends structured JSON output from CLI commands when automating.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
