## Description: <br>
Google Workspace Enterprise License Manager: Manage product licenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Google Workspace administrators and automation engineers use this skill to inspect and run gws licensing commands for assigning, revoking, listing, and updating user product licenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable account-impacting Google Workspace license assignment, revocation, or reassignment without built-in confirmation or scoping safeguards. <br>
Mitigation: Use least-privilege credentials, verify the active tenant and account before each command, and require clear human confirmation before any license assignment, revocation, or reassignment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and shared Google Workspace authentication prerequisites.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
