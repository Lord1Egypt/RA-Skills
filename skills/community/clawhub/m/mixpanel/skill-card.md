## Description:

Query Mixpanel analytics with funnels, retention, segmentation, and event tracking via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Mixpanel product analytics, including event counts, funnels, retention cohorts, segmentation, user profiles, and raw event exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Mixpanel through a service account and may query sensitive product analytics.

Mitigation: Use a least-privileged Mixpanel service account, keep credentials in environment variables, and avoid broad raw exports unless they are necessary.

Risk: The skill asks to save future activation preferences and analytics context in memory.

Mitigation: Review or disable memory behavior that would activate the skill on broad future discussions about metrics or user behavior.

Risk: Query results and product context may be persisted locally under ~/mixpanel/.

Mitigation: Review local Mixpanel memory and saved-query files before storing sensitive event names, profile data, or business insights.

## Reference(s):

- [ClawHub Mixpanel skill page](https://clawhub.ai/ivangdavila/skills/mixpanel)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Mixpanel Query API](https://mixpanel.com/api/query)
- [Mixpanel Engage API endpoint](https://mixpanel.com/api/query/engage)
- [Mixpanel Export API endpoint](https://data.mixpanel.com/api/2.0/export)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls using curl and jq, create local Mixpanel memory files, and summarize Mixpanel analytics results.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
