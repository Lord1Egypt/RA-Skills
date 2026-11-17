## Description:

Admin CLI for Lemon Squeezy stores. View orders, subscriptions, and customers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abakermi](https://clawhub.ai/user/abakermi)

### License/Terms of Use:


## Use Case:

Developers and store operators use this skill to manage Lemon Squeezy stores from the command line and view orders, subscriptions, customers, and stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Lemon Squeezy API key and may expose store data through CLI output.

Mitigation: Use an API key with the minimum permissions needed for viewing store data and avoid sharing command output that contains customer or order details.

Risk: The documented commands depend on a trusted ls-admin CLI being available in the execution environment.

Mitigation: Confirm the ls-admin command source before installation or execution.

## Reference(s):

- [Lemon Squeezy API settings](https://app.lemonsqueezy.com/settings/api)
- [ClawHub skill page](https://clawhub.ai/abakermi/skills/lemonsqueezy-admin)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the LEMONSQUEEZY_API_KEY environment variable for Lemon Squeezy API authentication.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
