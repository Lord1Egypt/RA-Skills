## Description: <br>
Manage tasks and projects via Locu's Public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsmorais](https://clawhub.ai/user/davidsmorais) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Locu to retrieve workspace user details, task lists, and project lists through Locu's Public API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a user-provided Locu token to api.locu.app and can expose workspace task or project data in an agent conversation. <br>
Mitigation: Use a least-privilege, revocable Locu token and confirm api.locu.app is the intended trusted endpoint before use. <br>
Risk: Task and project responses may include native Locu data and Linear or Jira-integrated work items. <br>
Mitigation: Review returned JSON before sharing, storing, or acting on sensitive workspace details. <br>


## Reference(s): <br>
- [Locu API user info endpoint](https://api.locu.app/api/v1/me) <br>
- [Locu API tasks endpoint](https://api.locu.app/api/v1/tasks) <br>
- [Locu API projects endpoint](https://api.locu.app/api/v1/projects) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON response handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOCU_API_TOKEN and returns Locu API JSON for the agent to parse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
