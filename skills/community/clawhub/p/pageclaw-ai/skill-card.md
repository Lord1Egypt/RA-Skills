## Description:

AI skills for managing Facebook business pages, including auto-reply, content posting, bookings, reviews, and lead capture across 9 industries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proship1](https://clawhub.ai/user/proship1)

### License/Terms of Use:

MIT-0

## Use Case:

External business page operators and their agents use PageClaw to manage Facebook Pages through the Graph API, including customer replies, content posting, review handling, booking support, lead capture, and analytics summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful Facebook Page access token and artifact examples place the token in query-string parameters, which could expose it through logged URLs.

Mitigation: Review before installation, use a minimally scoped Page token, prefer header-based authorization, and require operator confirmation before posting or replying.

## Reference(s):

- [PageClaw](https://pageclaw.onechat.ai)
- [OneChat.ai](https://onechat.ai)
- [Facebook Graph API](https://graph.facebook.com)
- [ClawHub Skill Page](https://clawhub.ai/proship1/skills/pageclaw-ai)
- [ClawHub Publisher Profile](https://clawhub.ai/user/proship1)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline HTTP request examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAGECLAW_PAGE_ID, PAGECLAW_PAGE_TOKEN, and PAGECLAW_NICHE environment variables.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
