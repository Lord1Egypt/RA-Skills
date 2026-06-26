## Description: <br>
Use Plane project management through its API to create and update issues, track progress, and manage agent tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Plane so it can list projects, create or update issues, and track project-management work through API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plane credentials stored in ~/.config/plane/credentials.json can allow access to or modification of Plane data. <br>
Mitigation: Use a least-privilege Plane API token, avoid storing a plaintext Plane password, and restrict permissions on the credentials file. <br>
Risk: API calls can create or update Plane projects and issues. <br>
Mitigation: Review proposed requests before execution and use credentials scoped to only the intended workspace and projects. <br>
Risk: Using a non-local Plane server over plain HTTP can expose credentials or project data in transit. <br>
Mitigation: Use HTTPS for any non-local Plane server. <br>


## Reference(s): <br>
- [Plane API examples](references/api-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/plane-project-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Plane API request guidance; actions require a configured Plane URL and API token or credentials file.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
