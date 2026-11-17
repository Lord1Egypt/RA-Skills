## Description:

Fetch public Maoyan Show data from show.maoyan.com, including event lists, event details, ticket prices, sessions, venues, city IDs, and crawler workflows, while excluding login, orders, payment, real-name verification, ticket verification, favorites, comments, and user account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onewilk](https://clawhub.ai/user/onewilk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents in querying and summarizing public Maoyan Show event, venue, price, session, city, recommendation, search, and list data. It is intended for public show-data lookup and API documentation workflows, not private account or transaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent use could drift from public show-data lookup into login, order, payment, real-name, ticket-verification, or account workflows.

Mitigation: Use only documented public endpoints; refuse private-flow requests and do not provide login tokens, account cookies, order details, payment data, or identity data.

Risk: City, category, keyword, and date filters on list-style endpoints may be advisory or unstable.

Mitigation: Ask for city or cityId when needed, validate returned city, category, date, and keyword fields locally, and discard mismatched results.

Risk: High-volume scraping can stress public services or trigger anti-abuse controls.

Mitigation: Keep request volume and concurrency modest, avoid bypassing login, CAPTCHA, risk-control, order, inventory-locking, or payment flows, and reuse generated request values only within the same task.

Risk: Returned detail and ticket-note fields may contain HTML.

Mitigation: Clean HTML before display, storage, or downstream processing.

## Reference(s):

- [Maoyan Show H5 API Usage Guide](artifact/references/api.md)
- [ClawHub Maoyan Show Skill Page](https://clawhub.ai/onewilk/skills/maoyan-show)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown or plain text with normalized fields and optional API request examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include normalized event, price, venue, and API usage fields; excludes private account, order, payment, identity, and ticket-verification data.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
