## Description: <br>
Gmail, Contacts, Calendar, Drive (with comments), Docs, and Sheets for OpenClaw agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panthrocorp](https://clawhub.ai/user/panthrocorp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to let agents access selected Google Workspace data and perform opt-in Calendar, Drive comment, Docs, and Sheets write operations through configured Google OAuth scopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the skill suspicious because setup handles sensitive Google Workspace access and may weaken account protections. <br>
Mitigation: Review the trust boundary before installation, prefer a dedicated low-privilege Google account or Workspace project, and keep services off or readonly unless writes are required. <br>
Risk: The security guidance notes risk from installing an unpinned executable. <br>
Mitigation: Pin and verify the release binary before placing it in the OpenClaw bin directory. <br>
Risk: Advanced Protection accounts may require temporary unenrollment to complete OAuth setup. <br>
Mitigation: Avoid using this skill with Advanced Protection accounts when unenrollment is unacceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panthrocorp/panthrocorp-google-workspace) <br>
- [Skill homepage](https://github.com/PanthroCorp-Limited/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration] <br>
**Output Format:** [JSON by default, with plain text output where supported and shell command examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials and a google-workspace binary available to the OpenClaw environment.] <br>

## Skill Version(s): <br>
0.5.2 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
