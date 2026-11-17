## Description:

Plausible Analytics (plausible.io). Use this skill for ANY Plausible Analytics request — reading, creating, and updating data. Whenever a task involves Plausible Analytics, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics users can query website statistics and record pageview or custom events in a connected Plausible account through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer can run downloaded code without a pinned release or prior approval.

Mitigation: Review the installer and approve installation separately; use a reviewed, fixed release and disable automatic skill synchronization if it is not wanted.

Risk: The hosted connector implementation and its handling of connected Plausible credentials are unverified.

Mitigation: Review the connection and credential handling before relying on the integration for sensitive analytics work.

## Reference(s):

- [Plausible Stats API documentation](https://plausible.io/docs/stats-api)
- [Plausible Analytics](https://plausible.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by the selected Plausible Analytics action.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
