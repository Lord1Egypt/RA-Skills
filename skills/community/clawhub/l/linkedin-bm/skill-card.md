## Description:

LinkedIn automation via browser relay or cookies for messaging, profile viewing, and network actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernhmueller](https://clawhub.ai/user/bernhmueller)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to operate LinkedIn through an attached or isolated browser for messaging, profile viewing, people search, notifications, and connection actions with explicit confirmation for outbound actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback cookie workflow can expose a live LinkedIn session credential.

Mitigation: Prefer the browser relay or isolated browser flow; do not copy the li_at cookie into chat, files, terminals, or logs, and revoke LinkedIn sessions if exposure is suspected.

Risk: Automated outbound messages or connection actions can affect a user's LinkedIn account or contacts.

Mitigation: Require explicit user confirmation before every outbound message, connection request, or connection acceptance.

Risk: Rapid automated LinkedIn activity can trigger rate limits or account challenges.

Mitigation: Keep activity slow, follow the skill's recommended rate limit, pause after rate limiting, and require manual CAPTCHA completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bernhmueller/skills/linkedin-bm)
- [LinkedIn](https://linkedin.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with browser command examples and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for user-reviewed browser automation steps; outbound messages and connection actions require manual confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
