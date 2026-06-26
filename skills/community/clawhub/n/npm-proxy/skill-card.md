## Description: <br>
Manage Nginx Proxy Manager (NPM) hosts, certificates, and access lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect and administer Nginx Proxy Manager proxy hosts, certificates, and access lists, including host status checks, enable or disable actions, deletion, and SSL setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Nginx Proxy Manager changes, including disabling or deleting proxy hosts. <br>
Mitigation: Review every API request before execution and avoid deleting production hosts unless an independent backup or rollback plan exists. <br>
Risk: NPM administrator credentials and the cached token file can grant control over proxy configuration. <br>
Mitigation: Run the skill only in a trusted environment, protect NPM_URL, NPM_EMAIL, NPM_PASSWORD, and /root/.npm-token.json, and remove or rotate the cached token when the skill is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Nginx Proxy Manager API operations through a Python helper when the required environment variables are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
