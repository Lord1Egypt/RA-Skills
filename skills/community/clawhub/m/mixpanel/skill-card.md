## Description: <br>
Query Mixpanel analytics with funnels, retention, segmentation, and event tracking via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and analytics users use this skill to query Mixpanel for event counts, funnels, retention cohorts, user segmentation, profile lookups, and raw event exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Mixpanel project analytics through service account credentials. <br>
Mitigation: Use a least-privilege Mixpanel service account and keep MP_SERVICE_ACCOUNT, MP_SERVICE_SECRET, and MP_PROJECT_ID in environment variables. <br>
Risk: Persistent local memory may contain product, customer, query, or analytics context. <br>
Mitigation: Review or clear saved files under ~/mixpanel/ when analytics details should not persist. <br>
Risk: Broad activation could lead the agent to use Mixpanel access in conversations where analytics access was not intended. <br>
Mitigation: Confirm when the skill should activate for metrics or user behavior requests before relying on proactive analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/mixpanel) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/mixpanel) <br>
- [Mixpanel Query API](https://mixpanel.com/api/query) <br>
- [Mixpanel Export API](https://data.mixpanel.com/api/2.0/export) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Markdown, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Mixpanel service account environment variables and may maintain local analytics context under ~/mixpanel/.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
