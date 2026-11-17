## Description:

Use this skill to read, create, and update WebinarJam data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve webinar details, webinar lists, registrants, and attendee data, and register users for webinars through a connected WebinarJam account. Confirm the target webinar and registrant before running the registration action, which changes account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs remote installers and can synchronize bundled skills without clear approval or disclosure of broader agent changes.

Mitigation: Review setup before running it, use a reviewed fixed oo CLI version, and control bundled-skill synchronization.

Risk: The connected account may expose WebinarJam webinar and registrant data to OOMOL.

Mitigation: Confirm which WebinarJam account is connected and what account and registrant data OOMOL may access.

Risk: Registering a user changes WebinarJam account data.

Mitigation: Keep the required confirmation and verify the exact webinar and registrant before registration.

## Reference(s):

- [WebinarJam homepage](https://webinarjam.com)
- [WebinarJam API documentation](https://support.webinarjam.com/en/collections/19655423-developer-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-webinarjam)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live action schema; registration is a confirmed write.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
