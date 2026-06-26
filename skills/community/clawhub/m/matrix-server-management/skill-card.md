## Description: <br>
Manage the Tuwunel Matrix Homeserver by registering users, creating rooms, managing room membership, uploading files to the media server, and sending files to the admin when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MontyCN](https://clawhub.ai/user/MontyCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Administrators and operators use this skill for explicit Matrix homeserver administration in a Hiclaw/Tuwunel environment, including user registration, room creation, room messaging, and media upload tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Matrix users, rooms, messages, and permanent media uploads. <br>
Mitigation: Install and use it only in the intended Hiclaw/Tuwunel admin environment with trusted administrators. <br>
Risk: Messages or uploaded files may expose secrets, credentials, private configs, or personal data to room members. <br>
Mitigation: Before sending messages or uploading files, confirm the target server, room membership, recipient, and file contents, and only share sensitive data when every room member is authorized. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Matrix admin environment variables and access to the intended local Tuwunel server endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
