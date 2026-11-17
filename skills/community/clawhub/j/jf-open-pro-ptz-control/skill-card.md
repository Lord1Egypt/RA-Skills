## Description:

JFTech PTZ camera control skill for direction movement, zoom and focus, preset management, tour planning, and standby return on supported PTZ cameras.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized camera operators use this skill to issue PTZ camera commands, manage presets, and configure patrol tours for JFTech devices that are online, bound to an open-platform account, and configured with valid credentials.

### Deployment Geography for Use:

China mainland, Asia, Europe, and North America through the documented JFTech regional API endpoints.

## Known Risks and Mitigations:

Risk: The skill controls real cameras using sensitive credentials.

Mitigation: Install only when the publisher is trusted, restrict use to authorized camera operators, and keep credential-bearing environments protected.

Risk: The API endpoint can be redirected through configuration.

Mitigation: Configure JF_ENDPOINT only to official documented hosts such as api-cn.jftechws.com, api-as.jftechws.com, api-eu.jftechws.com, or api-na.jftechws.com.

Risk: Preset and tour clearing actions can change device configuration.

Mitigation: Confirm operator intent outside the skill before running clear-preset or clear-tour actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ptz-control)
- [JFTech Open Platform documentation](https://docs.jftech.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech API credentials, a device token, an online PTZ-capable device, and the selected regional API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
