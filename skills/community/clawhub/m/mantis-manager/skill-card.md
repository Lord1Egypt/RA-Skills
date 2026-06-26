## Description: <br>
MantisBT Manager helps agents manage Mantis Bug Tracker issues, projects, users, filters, configuration, and related resources through the official Mantis REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willykinfoussia](https://clawhub.ai/user/willykinfoussia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and operations teams use this skill to administer MantisBT instances, manage tickets and projects, and switch between client, staging, and production instances through configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact MantisBT administration actions such as deleting resources, resetting passwords, creating tokens, impersonating users, changing configuration, and operating across instances. <br>
Mitigation: Use a least-privilege API token and require explicit human confirmation before deletes, password resets, token creation, impersonation, configuration changes, or cross-instance actions. <br>
Risk: The skill handles MantisBT API tokens and supports temporary or session-scoped token overrides. <br>
Mitigation: Keep tokens in environment or runtime context, avoid broad administrator tokens where possible, and do not ask the agent to reveal token values. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/willykinfoussia/mantis-manager) <br>
- [MantisBT Homepage](https://www.mantisbt.org/) <br>
- [MantisBT Documentation](https://mantisbt.org/documentation.php) <br>
- [MantisBT GitHub Repository](https://github.com/mantisbt/mantisbt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with REST API request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MANTIS_BASE_URL and MANTIS_API_TOKEN; may use temporary or session-scoped base URL and token context.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
