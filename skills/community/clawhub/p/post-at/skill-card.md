## Description: <br>
Manage Austrian Post (post.at) deliveries - list packages, check delivery status, set delivery place preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrauseFx](https://clawhub.ai/user/KrauseFx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation agents use this skill to check post.at delivery status, inspect package details, and prepare delivery-place commands for Austrian Post shipments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires post.at account credentials to use the external CLI. <br>
Mitigation: Keep credentials in environment variables or approved secret storage, and avoid sharing usernames or passwords in chat logs. <br>
Risk: Delivery-place commands can change where packages are left. <br>
Mitigation: Require explicit user approval before running routing place commands, especially when applying changes to multiple deliveries. <br>


## Reference(s): <br>
- [Post.at Tracking on ClawHub](https://clawhub.ai/KrauseFx/post-at) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output command variants for scripting workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
