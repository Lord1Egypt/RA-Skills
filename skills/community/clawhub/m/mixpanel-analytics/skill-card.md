## Description: <br>
Query Mixpanel product analytics for events, funnels, retention, user profiles, cohorts, and raw event exports through Mixpanel APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, growth, and support teams can use this skill through an agent to query Mixpanel metrics, inspect funnels and retention, look up user profiles, and export bounded event data for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Mixpanel credentials to query analytics data, including user profiles and raw event exports. <br>
Mitigation: Use a least-privileged Mixpanel service account and provide credentials only in trusted agent environments. <br>
Risk: Profile and event output may contain sensitive customer or product analytics data that can appear in terminal logs or agent transcripts. <br>
Mitigation: Limit raw exports, avoid unnecessary broad queries, and handle generated output according to the organization's data handling requirements. <br>


## Reference(s): <br>
- [Mixpanel Analytics on ClawHub](https://clawhub.ai/fr3kstyle/mixpanel-analytics) <br>
- [Mixpanel Data Export API](https://data.mixpanel.com/api/2.0) <br>
- [Mixpanel EU Data Export API](https://data-eu.mixpanel.com/api/2.0) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text summaries and JSON-formatted API responses in terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive Mixpanel event and profile data; raw exports should be limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
