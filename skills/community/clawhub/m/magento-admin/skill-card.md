## Description:

Helps store owners administer their Magento 2 installations through SSH, REST, GraphQL, and database access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nj070574-gif](https://clawhub.ai/user/nj070574-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Magento store owners and administrators use this skill to inspect and manage their own stores, including orders, products, configuration, maintenance, and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SSH, database, admin API, and sudo access can change or disrupt a store.

Mitigation: Install only on infrastructure you own and administer; limit granted privileges and review high-impact commands before execution.

Risk: Refunds, admin-user creation, extension installs, database restores, service restarts, and raw SQL can have significant effects.

Mitigation: Require explicit owner approval for these operations before allowing autonomous execution.

## Reference(s):

- [Magento Admin skill on ClawHub](https://clawhub.ai/nj070574-gif/skills/magento-admin)
- [Publisher profile on ClawHub](https://clawhub.ai/user/nj070574-gif)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration guidance, Text]

**Output Format:** [Markdown with command examples and plain-language status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires owner-supplied access to the Magento host, database, and admin API.]

## Skill Version(s):

5.7.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
