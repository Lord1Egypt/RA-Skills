## Description:

Summarizes existing Amazon negative-review alerts and low-star reviews for specified ASINs into a prioritized action list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and account operators use this skill to review existing account alerts and low-star reviews for specified products, group recurring issues by severity, and prepare a follow-up list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The locally stored ARI API key could expose account access if disclosed.

Mitigation: Keep the key private; authorize through the browser setup flow and do not request or display the key in chat.

Risk: The mark-read option marks all current account alerts as read, which could hide unread items from the inbox view.

Mitigation: Use it only when the user explicitly requests marking all alerts read, and clarify that this does not resolve the underlying review issues.

## Reference(s):

- [ARI account and authorization portal](https://ari.funewa.com)
- [Negative Review Inbox on ClawHub](https://clawhub.ai/funewa/skills/negative-inbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Prioritized alert and review summary with brief supporting excerpts and ASIN, marketplace, and time-window context.]

**Output Parameters:** [Varies by selected ASIN, marketplace, rating, and time window.]

**Other Properties Related to Output:** [Uses successfully returned data only; review samples are not presented as overall return rates. Alerts are marked read only when explicitly requested.]

## Skill Version(s):

1.5.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
