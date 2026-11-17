## Description:

Search and read Mailchimp Marketing API audiences, members, campaigns, content, and reports through a local MCP wrapper. Use when the user asks about Mailchimp marketing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use the skill to inspect a connected Mailchimp account, including its audiences, members, campaigns, campaign content, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read contacts, campaign content, and reports from the connected Mailchimp account.

Mitigation: Connect only an account whose data the agent is authorized to inspect.

Risk: A misconfigured API base could direct authenticated requests to an unintended endpoint.

Mitigation: Verify that the provisioned API base is the correct HTTPS Mailchimp endpoint before use.

## Reference(s):

- [mcporter](https://github.com/steipete/mcporter)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Mailchimp account data as JSON, with text summaries where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results vary by the selected Mailchimp data request.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
