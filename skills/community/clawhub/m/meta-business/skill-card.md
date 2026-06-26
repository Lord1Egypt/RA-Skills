## Description: <br>
Skill for the Meta Business CLI. Complete WhatsApp, Instagram, Facebook Pages, and Messenger automation via the Graph API. Supports messaging, media, templates, analytics, webhooks, and systemd service management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adolago](https://clawhub.ai/user/adolago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents in configuring and running the Meta Business CLI for WhatsApp, Instagram, Facebook Pages, Messenger, webhooks, analytics, and service management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful Meta business account actions, including sends, posts, deletes, moderation actions, webhook forwarding, and service installation. <br>
Mitigation: Use least-privilege Meta scopes and manually confirm sends, posts, deletes, moderation actions, webhook destinations, and service installation before execution. <br>
Risk: Stored credentials and local configuration can expose Meta app secrets, access tokens, phone number IDs, and webhook settings. <br>
Mitigation: Protect ~/.meta-cli/config.json, avoid unnecessary token sharing, and verify configuration before running automated workflows. <br>
Risk: Webhook forwarding can send inbound message data to an unintended or untrusted endpoint. <br>
Mitigation: Use HTTPS endpoints you control and verify webhook.forwardUrl destinations before enabling forwarding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adolago/meta-business) <br>
- [Publisher profile](https://clawhub.ai/user/adolago) <br>
- [Meta CLI source repository](https://github.com/adolago/meta-cli.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages JSON output from CLI commands for scripting and agent use.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
