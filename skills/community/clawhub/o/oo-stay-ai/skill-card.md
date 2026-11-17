## Description:

Access Stay AI account settings, subscriptions, and orders through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve Stay AI account settings, subscriptions, and order information through read-only actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unchecked remote code and make unclear local changes, including installing other agent skills.

Mitigation: Use a verified oo CLI release and review and approve its local changes before setup.

Risk: Requests pass through OOMOL, while remote installer behavior and server-side credential handling remain unverified.

Mitigation: Review setup and credential handling, and connect only the Stay AI account and permissions needed for the task.

## Reference(s):

- [Stay AI](https://stay.ai)
- [Stay AI API documentation](https://docs.stay.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON results from Stay AI read actions, summarized in text; Markdown with oo CLI command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves account settings, subscriptions, and orders through read-only actions.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
