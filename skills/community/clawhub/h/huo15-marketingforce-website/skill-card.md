## Description:

Manages MarketingForce/T云 website content through CMS APIs, including articles, products, media, inquiries, SEO, analytics, plugins, multilingual content, AI tools, and system administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External website operators and developers use this skill to inspect and manage MarketingForce/T云 production website content, settings, SEO data, inquiries, media libraries, templates, and administrative records through an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful MarketingForce session tokens for production website administration.

Mitigation: Keep tokens out of chats and logs, store them only in the local environment file or environment variables, restrict file permissions, and rotate or revoke tokens after use.

Risk: The skill can change, publish, delete, upload, export, back up, restore, or administer website and user/member data.

Mitigation: Require manual review before any save, publish, delete, upload, plugin, backup, restore, export, or user/member action.

Risk: Unsafe edits could affect live website content or introduce problematic HTML.

Mitigation: Back up content before editing, preview changes as drafts before publishing, prefer hiding over deletion, and sanitize user-provided HTML.

## Reference(s):

- [MarketingForce T云 API Reference](references/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-marketingforce-website)
- [MarketingForce Console Login](https://console.marketingforce.com/login/login)
- [MarketingForce Official Site](https://www.marketingforce.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MarketingForce session tokens supplied outside the public skill files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
