## Description:

Connects an OpenClaw agent to your Home Assistant instance to answer smart-home questions and control devices with confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nj070574-gif](https://clawhub.ai/user/nj070574-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Home Assistant owners use this skill through OpenClaw to check device status, temperatures, energy use, presence, and cameras, and to request confirmed device or automation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device and automation actions can change the physical state of a home.

Mitigation: Require explicit confirmation for actions; leave lock and alarm control disabled unless needed.

Risk: Home status, presence, and camera data can expose private activity.

Mitigation: Restrict who can message connected OpenClaw channels and treat snapshots and URLs as private.

Risk: A long-lived token or unencrypted connection can expose control of the Home Assistant instance.

Mitigation: Use a dedicated low-privilege user and HTTPS; leave the cleartext HTTP override unset unless knowingly accepting LAN token exposure.

## Reference(s):

- [Home Assistant Integration on ClawHub](https://clawhub.ai/nj070574-gif/skills/home-assistant-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device status, home summaries, camera snapshot URLs, and confirmation prompts.]

## Skill Version(s):

2.5.1 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
