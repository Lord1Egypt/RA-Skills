## Description:

Google Cloud Identity: Manage identity groups and memberships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Google Workspace administrators and operations engineers use this skill to ask an agent for Google Cloud Identity CLI guidance covering groups, memberships, devices, policies, and SSO resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide device wipe, device delete, group patch, SSO profile, and SSO assignment changes with high administrative impact.

Mitigation: Require explicit human confirmation and administrator review before executing wipe, delete, patch, or assignment-changing commands.

Risk: The short description emphasizes groups and memberships while the artifact also covers device administration and SSO configuration.

Mitigation: Install only in environments where agents are authorized to assist with the full Cloud Identity scope documented by the skill.

Risk: Incorrect parameters for Cloud Identity methods could affect production identity, device, or SSO state.

Mitigation: Use gws schema inspection before constructing commands and review generated parameters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-cloudidentity)
- [Google API resource names](https://cloud.google.com/apis/design/resource_names)
- [Google Workspace multi-party approval for sensitive actions](https://support.google.com/a/answer/13790448)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include gws cloudidentity commands and gws schema inspection guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
