## Description:

Query Mixpanel product analytics for events, funnels, retention, user profiles, cohorts, and raw event exports through Mixpanel APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and product teams use this skill to retrieve Mixpanel metrics, inspect funnels and retention, debug user profiles, and generate operational analytics reports from an authorized Mixpanel project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mixpanel event exports and user profile lookups may expose sensitive user or internal analytics data.

Mitigation: Install only for authorized users, limit raw exports, and avoid placing returned profile or event data in contexts where it should not appear.

Risk: Broad or legacy Mixpanel API credentials may allow access beyond the agent's immediate task.

Mitigation: Use a least-privilege Mixpanel service account for the target project and avoid legacy broad API secrets where possible.

## Reference(s):

- [Mixpanel Analytics skill page](https://clawhub.ai/fr3kstyle/skills/mixpanel-analytics)
- [Publisher profile: fr3kstyle](https://clawhub.ai/user/fr3kstyle)
- [Mixpanel US Data Export API endpoint](https://data.mixpanel.com/api/2.0)
- [Mixpanel EU Data Export API endpoint](https://data-eu.mixpanel.com/api/2.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text or JSON-derived API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event counts, unique user totals, funnel conversion summaries, retention cohorts, user profile fields, or capped raw event exports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
