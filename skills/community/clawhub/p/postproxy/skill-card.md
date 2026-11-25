## Description:

Create, schedule, and manage social media posts, comments, direct messages, queues, webhooks, and analytics across supported social platforms through the Postproxy API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danbaranov](https://clawhub.ai/user/danbaranov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media teams use this skill to let an agent prepare API calls and guidance for publishing, scheduling, moderating, messaging, queue management, webhook setup, and analytics workflows in Postproxy. It is intended for users who already trust Postproxy with their connected social accounts and API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, schedule, modify, moderate, or delete content on real social media accounts, including irreversible platform deletion.

Mitigation: Require explicit user confirmation of the exact content, media, target profiles or placements, and deletion scope before outward-facing or destructive actions; prefer drafts when intent is ambiguous.

Risk: The skill can read and send direct messages or private replies involving real people.

Mitigation: Only read or send private communications when explicitly requested, confirm recipient and message text before sending, and avoid reusing DM content in public posts or external services without consent.

Risk: Webhook payloads may send private content to a configured URL, and webhook secrets can be used to forge signed requests.

Mitigation: Register only HTTPS endpoints controlled by the user, keep webhook secrets out of chat output, logs, and source control, and verify signatures with timestamp freshness and duplicate-delivery checks.

Risk: The Postproxy API key grants access to connected social accounts through the Postproxy API.

Mitigation: Install only when Postproxy is trusted with the connected accounts, store POSTPROXY_API_KEY as a secret, and avoid printing or committing the key.

Risk: Platform limitations, placement defaults, and asynchronous write failures can produce unexpected posting targets or partial delivery.

Mitigation: Resolve placement-specific targets before posting, respect documented platform constraints, and poll resource status or subscribe to failure webhooks for asynchronous operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danbaranov/skills/postproxy)
- [Publisher Profile](https://clawhub.ai/user/danbaranov)
- [Postproxy Homepage](https://postproxy.dev)
- [Postproxy API Keys](https://app.postproxy.dev/api_keys)
- [Postproxy SDK Documentation](https://postproxy.dev/getting-started/sdks/)
- [Artifact README](artifact/README.md)
- [Posts Rules](artifact/rules/posts.md)
- [Messages Rules](artifact/rules/messages.md)
- [Webhooks Rules](artifact/rules/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl commands, API request examples, JSON payloads, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTPROXY_API_KEY and curl; may reference official SDK packages when generating application code.]

## Skill Version(s):

2.0.2 (source: server release evidence; artifact frontmatter lists 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
