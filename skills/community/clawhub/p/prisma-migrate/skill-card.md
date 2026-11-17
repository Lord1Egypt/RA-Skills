## Description:

Migrate Prisma Access configurations between different SCM tenants (TSGs). Use when moving security policies, NAT rules, address objects, and other configurations from one Prisma Access tenant to another. Includes migration compatibility matrix based on real-world testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to plan and perform Prisma Access tenant-to-tenant configuration migrations, including dependency ordering, conflict handling, validation, and user-confirmed commit guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide changes to security policies and tenant configuration in Prisma Access.

Mitigation: Use least-privilege service accounts, review the dry-run output, and require explicit user confirmation before committing changes.

Risk: Incorrect conflict handling or missing dependencies can create failed imports or broken references.

Mitigation: Export and import in dependency order, check conflicts across all relevant folders, validate candidate configuration, and repair missing references before commit.

Risk: Some profile types may be unavailable to the configured service account.

Mitigation: Confirm API permissions before migration and manually recreate or restore URL Filtering, Data Filtering, AI Security, or related references when the API cannot export them.

## Reference(s):

- [Tenant-to-Tenant Migration Workflow Reference](reference/migration-workflow.md)
- [ClawHub skill page](https://clawhub.ai/leesandao/skills/prisma-migrate)
- [Homepage](https://github.com/leesandao/prismaaccess-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, and migration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Prisma Access SCM credentials and curl/jq availability; recommends dry-run review before changes and explicit confirmation before commit.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
