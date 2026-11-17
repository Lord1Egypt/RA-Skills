## Description:

Use this skill to read, create, and update Jumpseller store data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve Jumpseller store, product, category, customer, and order data, and to create or update records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup path downloads and executes installer code without verification, and the setup flow may install an additional agent skill.

Mitigation: Preinstall a reviewed, verified CLI; review the additional skill installation behavior; limit connected-account access and retain confirmations for store changes.

## Reference(s):

- [Jumpseller API documentation](https://jumpseller.com/support/api/)
- [Jumpseller](https://jumpseller.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
