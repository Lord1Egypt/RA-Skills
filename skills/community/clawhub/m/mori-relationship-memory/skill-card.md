## Description:

Helps real estate and referral-driven professionals search their private Mori relationship memory and draft cited recommendations after explicit activation and data-scope confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate agents, brokers, and other referral-driven professionals use this skill to look up account-private contacts and provenance-backed facts and prepare cited referral recommendations for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private contact, email, thread, or SMS context may be exposed beyond the account holder's intended scope.

Mitigation: Activate only at the account holder's request, confirm the data category for each task, and access only the minimum necessary account data.

Risk: A leaked API key could allow unauthorized access to private relationship data.

Mitigation: Keep the narrowly scoped, revocable key in a secret store or environment variable; never include it in prompts, source files, or chat.

Risk: An inaccurate recommendation could misrepresent a contact or be shared without review.

Mitigation: Report confidence and cited contacts, avoid inventing answers when confidence is low, and have the account holder review drafts before sharing.

## Reference(s):

- [Mori Relationship Memory on ClawHub](https://clawhub.ai/kiwi-phantomworks/skills/mori-relationship-memory)
- [Mori website](https://www.heymori.ai)
- [Mori app](https://app.heymori.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with cited contacts and confidence where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human-reviewed drafts only; no automatic outreach or record changes.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
