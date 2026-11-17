## Description:

BigCommerce (bigcommerce.com). Use this skill for ANY BigCommerce request — reading, creating, updating, and deleting data. Whenever a task involves BigCommerce, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the OOMOL-connected BigCommerce account to inspect products and manage catalog entries. The skill supports listing and retrieving products, as well as creating, updating, and deleting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs an unverified installer whose documented effects extend to installing or updating other agent skills.

Mitigation: Review the CLI installation and release, check which skills it installs or updates, and consider disabling startup skill synchronization using the publisher's documented controls.

Risk: Creating, updating, or deleting products changes BigCommerce store data.

Mitigation: Approve the exact product changes and deletion targets before running write or destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BigCommerce API accounts documentation](https://developer.bigcommerce.com/docs/start/authentication/api-accounts)
- [BigCommerce](https://www.bigcommerce.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
