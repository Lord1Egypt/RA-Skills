## Description:

Google Workspace Reseller: Manage Workspace subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Developers and administrators use this skill to inspect Google Workspace Reseller CLI resources and run customer, subscription, and reseller notification operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents commands that can change paid customer subscriptions.

Mitigation: Use tightly scoped Google Workspace reseller credentials and confirm the customer ID, subscription ID, requested change, and expected service or billing impact before destructive or billing-affecting calls.

Risk: The skill depends on external Google Workspace reseller authentication and the gws CLI being configured correctly.

Mitigation: Review the shared Google Workspace authentication guidance and inspect each method with gws schema before building parameters for account or subscription changes.

## Reference(s):

- [Google Workspace Reseller API: Manage customers](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_customers)
- [Google Workspace Reseller API: Manage subscriptions](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions)
- [Google Workspace Reseller API: Order a new customer account](https://developers.google.com/workspace/admin/reseller/v1/reference/customers/insert.html)
- [Google Workspace Admin Help: Verify your domain](https://support.google.com/a/answer/9122284)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and prior Google Workspace reseller authentication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
