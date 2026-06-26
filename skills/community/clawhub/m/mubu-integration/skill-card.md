## Description: <br>
Mubu Integration helps an agent authenticate to Mubu, manage documents and folders, and export outline content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a Mubu account for listing, creating, saving, moving, deleting, and exporting outline notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Mubu account credentials and cache an authentication token locally. <br>
Mitigation: Protect MUBU_PHONE, MUBU_PASSWORD, any .env file, and ~/.mubu_token; rotate credentials if those files are exposed. <br>
Risk: The skill can create, overwrite, move, or delete remote Mubu notes. <br>
Mitigation: Use explicit Mubu commands and confirm delete, move, and overwrite targets before execution. <br>
Risk: The integration uses non-official Mubu Web API behavior that may change. <br>
Mitigation: Review failures before retrying and avoid high-frequency calls that could trigger service limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboacean/mubu-integration) <br>
- [Mubu website](https://mubu.com) <br>
- [Mubu API base URL](https://api2.mubu.com/v3/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON API output, and Markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mubu credentials and may read, create, save, move, or delete remote notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
