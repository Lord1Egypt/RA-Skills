## Description:

Summarizes public service details, announcements, and city-specific information from Hellobike's official pages without accessing user accounts or orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to organize public Hellobike service, announcement, news, pricing, and city-coverage information into concise summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misapplied to account, order, payment, or private user-data workflows that are outside its intended scope.

Mitigation: Use it only for public Hellobike pages and reject tasks requiring login, order actions, payment operations, permission bypass, or private user data.

Risk: Summaries of dynamic public pages may become incomplete or stale if page content changes or loading is not complete.

Mitigation: Wait for pages to load, include source links and collection time where relevant, and ask users to verify time-sensitive service, price, or city-coverage details before acting on them.

Risk: The artifact is written in Chinese, which may not match every user's preferred output language.

Mitigation: Ask the agent for output in the user's preferred language when summaries need to be localized.

## Reference(s):

- [Hellobike official website](https://www.hellobike.com/)
- [ClawHub skill page](https://clawhub.ai/codenova58/skills/hellobike)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and structured text lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be limited to public-page information and exclude account, order, payment, or private user-data workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
