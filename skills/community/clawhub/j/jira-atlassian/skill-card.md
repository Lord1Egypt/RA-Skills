## Description: <br>
Full-featured Atlassian Jira Cloud REST API v3 skill for managing issues, sprints, boards, epics, projects, users, and related Jira resources through direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to automate Jira Cloud work such as creating and updating issues, running JQL searches, managing boards and sprints, and calling Jira Software, build, deployment, DevOps, and security APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Jira API credentials can authorize access to project data and state-changing Jira actions if exposed or used in the wrong environment. <br>
Mitigation: Store credentials outside prompts and source files, prefer least-privilege or test credentials, and intentionally choose production credentials only when production access is required. <br>
Risk: The skill documents endpoints that can create, update, move, transition, notify, or delete Jira resources. <br>
Mitigation: Review the proposed HTTP method, endpoint, target issue or project, and request body before executing calls against Jira. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeffersonling1217-png/jira-atlassian) <br>
- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Code] <br>
**Output Format:** [Markdown with REST endpoint paths, HTTP methods, JSON request bodies, and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_DOMAIN; some DevOps integration endpoints may require OAuth or Connect JWT credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
