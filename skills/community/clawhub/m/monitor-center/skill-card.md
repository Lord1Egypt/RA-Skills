## Description:

Summarizes an Amazon account’s saved monitoring data, including recent reviews, negative reviews, unread alerts, paused items, and product changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and account operators use this skill to review account-wide monitoring status and recent product changes, including new reviews, negative reviews, unread alerts, and paused items. It summarizes data that has already been collected and does not manage monitoring plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing ARI makes account-wide monitoring data, account details, and credit balance available in the agent session.

Mitigation: Authorize only the intended account and treat the resulting session content as sensitive.

Risk: Exposure of the saved ARI key could allow unauthorized account access.

Mitigation: Protect ~/.ari/config.json from sharing and cloud synchronization, and revoke the key when it is no longer needed.

## Reference(s):

- [Amazon Monitor dashboard](https://ari.funewa.com/zh/monitor)
- [ClawHub release page](https://clawhub.ai/funewa/skills/monitor-center)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown monitoring summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only successfully returned data and calls out missing or incomplete data.]

## Skill Version(s):

1.5.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
