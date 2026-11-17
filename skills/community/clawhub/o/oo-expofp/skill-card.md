## Description:

ExpoFP (expofp.com). Use this skill for ANY ExpoFP request — reading, creating, updating, and deleting data. Whenever a task involves ExpoFP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to read and manage exhibitor and expo data in an ExpoFP account through the connected service. It provides instructions for listing, retrieving, creating, updating, and deleting exhibitors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may make broader automatic changes to installed agent skills than this skill documents.

Mitigation: Review the CLI's installation behavior and use a reviewed, fixed CLI release; set OO_SKILLS_SYNC_DISABLED=1 to disable documented startup skill synchronization.

Risk: Using the connected ExpoFP service requires trusting OOMOL to handle ExpoFP credentials and requests.

Mitigation: Confirm that you trust OOMOL to handle ExpoFP credentials and requests before using the skill.

## Reference(s):

- [ExpoFP JSON API documentation](https://developer.expofp.com/guide/json-api)
- [ExpoFP](https://expofp.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses and concise CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the ExpoFP action and its input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
