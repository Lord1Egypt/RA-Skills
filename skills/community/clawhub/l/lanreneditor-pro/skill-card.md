## Description:

Lanreneditor Pro helps agents create, format, preview, and submit WeChat public-account content drafts through a SaaS-based content pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lufeng321](https://clawhub.ai/user/lufeng321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to turn source material or WeChat articles into formatted drafts, cover assets, platform-specific copy, previews, and publishing workflows for WeChat public accounts and related distribution channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article drafts, source URLs, images, account identifiers, and API-key authenticated requests may be sent to a configurable external SaaS endpoint.

Mitigation: Install only when the endpoint is trusted, keep apiBaseUrl pinned to the intended HTTPS service, and start with a least-privilege or test API key.

Risk: Publish, distribute, and clear-materials actions can affect external accounts or stored content.

Mitigation: Require explicit human confirmation before publishing, distributing, or clearing materials, and review the selected account and template before execution.

Risk: Generated drafts, platform copy, covers, and article analysis may be inaccurate, inappropriate, or misaligned with the publisher's requirements.

Mitigation: Manually review all generated content and previews before using the publish or distribution flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lufeng321/skills/lanreneditor-pro)
- [SaaS platform](https://open.tyzxwl.cn)
- [Quickstart](artifact/QUICKSTART.md)
- [Integration guide](artifact/INTEGRATION.md)
- [API key management](artifact/APIKEY.md)

## Skill Output:

**Output Type(s):** [text, markdown, html, api calls, configuration, guidance]

**Output Format:** [Markdown and text responses with interactive selections, API-backed status updates, and HTML preview or rendering links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured HTTPS apiBaseUrl and API key; generated or transformed content should be reviewed before publication or distribution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
