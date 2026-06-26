## Description: <br>
Control Google Nest devices such as thermostats, cameras, and doorbells through the Google Smart Device Management API using curl and jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mitchellbernstein](https://clawhub.ai/user/mitchellbernstein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and smart-home operators use this skill to configure Google Smart Device Management access and produce CLI or direct API commands for Nest thermostats, cameras, doorbells, speakers, and displays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Google OAuth credentials and may give an agent access to sensitive smart-home devices. <br>
Mitigation: Store tokens outside shared repositories, restrict configuration file permissions, revoke tokens when no longer needed, and require explicit confirmation before camera access or device changes. <br>
Risk: The artifact documents a global symlink command and helper commands that should be reviewed before execution. <br>
Mitigation: Review the referenced helper script before linking or running it, and avoid global installation unless the local script path is present and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mitchellbernstein/google-home) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Nest Device Access registration](https://nests.google.com/frame/register-user) <br>
- [Google OAuth token endpoint](https://www.googleapis.com/oauth2/v4/token) <br>
- [Google Smart Device Management devices endpoint](https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, Google OAuth credentials, and Google Smart Device Management API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
