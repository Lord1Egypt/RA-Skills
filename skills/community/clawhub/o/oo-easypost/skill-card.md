## Description:

Use this skill for any EasyPost request, including reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing shipping workflows use this skill to retrieve EasyPost addresses and trackers, list carrier types and trackers, and create addresses or standalone trackers through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked downloads and introduce broader agent changes without clear approval.

Mitigation: Use a reviewed CLI distribution, require approval for local installation, and decide whether to disable automatic skill synchronization.

Risk: Connecting EasyPost entrusts OOMOL with service credentials and shipping information.

Mitigation: Review the connection before use and limit the shipping information shared to what the requested action requires.

## Reference(s):

- [EasyPost API documentation](https://docs.easypost.com/docs/authentication)
- [EasyPost](https://www.easypost.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [Structured JSON data with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
