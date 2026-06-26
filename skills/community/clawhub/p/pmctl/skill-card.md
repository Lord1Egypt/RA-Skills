## Description: <br>
Browse and inspect Postman collections, requests, and environments from the terminal using pmctl to discover API endpoints, look up request details, resolve environment variables, and construct curl commands from Postman data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbingli](https://clawhub.ai/user/wbingli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Postman workspaces from the terminal, discover API endpoints, resolve environment-backed URLs, and prepare curl commands without opening the Postman GUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Postman environment output can reveal secrets or sensitive endpoint details. <br>
Mitigation: Use least-privileged Postman API keys, avoid sharing full environment output unless necessary, and do not paste secret values into chats or logs. <br>
Risk: The skill requires installing and running the external pmctl package. <br>
Mitigation: Verify the pmctl package and version before installation, and review commands before execution. <br>


## Reference(s): <br>
- [pmctl source repository](https://github.com/wbingli/pmctl) <br>
- [Postman API key settings](https://go.postman.co/settings/me/api-keys) <br>
- [ClawHub pmctl release page](https://clawhub.ai/wbingli/pmctl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pmctl commands and JSON-processing examples for Postman data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
