## Description: <br>
Automates initialization of Gitea research project repositories by collecting repository details, creating the repository, writing a standard directory structure and Markdown documents, assigning collaborators, opening startup issues, and sending email notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and project coordinators use this skill to standardize new Gitea research repositories with starter documentation, collaboration rules, member profiles, repository permissions, startup issues, and notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill administers a Gitea organization using a powerful personal access token. <br>
Mitigation: Use a least-privilege bot token scoped only to the intended organization and install the skill only where repository administration is expected. <br>
Risk: The sample configuration uses a non-HTTPS Gitea endpoint and the setup flow stores the token locally in plaintext. <br>
Mitigation: Change GITEA_URL to a trusted HTTPS endpoint before configuration and protect the local environment file; the setup script sets file permissions to 600. <br>
Risk: The skill can call an external email skill through EMAIL_SKILL_PATH. <br>
Mitigation: Review EMAIL_SKILL_PATH before use and point it only to a trusted email skill configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/project-init123) <br>
- [Publisher profile](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration] <br>
**Output Format:** [Conversational text plus generated Markdown repository files, member profile files, and issue content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Gitea API calls and an external email skill when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
