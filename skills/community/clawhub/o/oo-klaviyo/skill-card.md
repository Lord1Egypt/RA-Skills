## Description:

Access Klaviyo data through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read Klaviyo campaigns, events, and profiles, validate an account, and create events through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and introduce persistent agent skills.

Mitigation: Review setup first, prefer a verified CLI release installed under your control, and disable startup skill synchronization if it is not needed.

Risk: OOMOL mediates access to the connected Klaviyo customer data.

Mitigation: Review the connection and data access before use, and keep confirmation in place for write actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Klaviyo API overview](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo](https://www.klaviyo.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
