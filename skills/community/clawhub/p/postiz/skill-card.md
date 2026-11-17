## Description:

Postiz helps agents schedule, manage, upload media for, and analyze social media and chat posts across 28+ connected channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevo-david](https://clawhub.ai/user/nevo-david)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to authenticate with Postiz, discover connected integrations, prepare media, schedule or draft posts across social and chat channels, and review platform or post analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to publish, delete, or bulk schedule content on connected social, chat, or business accounts.

Mitigation: Require explicit human approval before running posts:create, posts:delete, or bulk automation against production accounts.

Risk: API keys and OAuth credentials could be exposed through shell history, shell profile files, or command output.

Mitigation: Use OAuth or a managed secret store, avoid printing tokens, and do not persist API keys directly in shared shell profiles.

Risk: Installing an unpinned external CLI or using a custom API URL can route posting actions through an unexpected implementation or endpoint.

Mitigation: Pin and verify the CLI version before use, and keep separate credentials for custom or self-hosted API URLs.

## Reference(s):

- [Postiz Public API Introduction](https://docs.postiz.com/public-api/introduction)
- [Postiz npm Package](https://www.npmjs.com/package/postiz)
- [Postiz Website](https://postiz.com)
- [ClawHub Skill Page](https://clawhub.ai/nevo-david/skills/postiz)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nevo-david)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Postiz authentication through OAuth or POSTIZ_API_KEY; POSTIZ_API_URL is optional for custom or self-hosted API endpoints.]

## Skill Version(s):

1.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
