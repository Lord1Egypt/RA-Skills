## Description:

Guides agents in managing Google Play apps, subscriptions, in-app products, purchases, and reviews through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app operators use this skill to query and manage Google Play commerce, reviews, and app data through their authorized account. It also describes optional scheduled or event-triggered automation of approved actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized writes can change live app commerce and review data.

Mitigation: Start with read-only calls and confirm each write and new connection with the user.

Risk: Automations and destinations can repeatedly act on or forward account data.

Mitigation: Review functions, triggers, destinations, and forwarded fields before enabling them; know how to disable or delete them.

Risk: Long-lived API keys can expose account access if mishandled.

Mitigation: Prefer OAuth; never expose credentials in logs, commands, or destination settings.

## Reference(s):

- [ClawHub Google Play skill](https://clawhub.ai/byungkyu/skills/google-play)
- [Android Publisher API overview](https://developers.google.com/android-publisher)
- [Google Play subscriptions API](https://developers.google.com/android-publisher/api-ref/rest/v3/monetization.subscriptions)
- [Google Play reviews API](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Google Play API responses depend on the authorized account and requested operation.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
