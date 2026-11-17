## Description:

SafetyCulture (safetyculture.com). Use this skill for ANY SafetyCulture request — reading, creating, and updating data. Whenever a task involves SafetyCulture, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External SafetyCulture users can read inspection and action records and create actions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup may execute an unverified remote installer, and the hosted connector implementation has not been verified.

Mitigation: Review and approve CLI installation separately, including any automatic installation of other agent skills; consider OOMOL's access to your account and data before connecting SafetyCulture.

Risk: Creating an action changes SafetyCulture data.

Mitigation: Confirm the exact action payload and effect with the user before running it.

## Reference(s):

- [SafetyCulture skill release](https://clawhub.ai/oomol/skills/oo-safetyculture)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [SafetyCulture homepage](https://safetyculture.com)
- [SafetyCulture API documentation](https://developer.safetyculture.com/reference/introduction)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action payloads and returned data, with shell commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and action instructions; creating an action changes SafetyCulture data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
