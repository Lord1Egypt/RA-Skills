## Description: <br>
Use when an agent needs to post text, images, or build-in-public updates to LinkedIn through the configured LinkedIn channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david3xu](https://clawhub.ai/user/david3xu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators use this skill to draft and publish LinkedIn feed updates with optional image media through an authenticated LinkedIn channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content publicly through a connected LinkedIn account. <br>
Mitigation: Require explicit approval of the exact account, text, media, timing, and action before any write operation. <br>
Risk: The skill depends on LinkedIn credentials stored in channels.linkedin configuration. <br>
Mitigation: Store credentials only in the trusted agent environment and rotate or revoke tokens when account access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david3xu/linkedin-poster) <br>
- [LinkedIn Post Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and post templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires channels.linkedin configuration with an OAuth access token and LinkedIn person URN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
