## Description:

MySQL 8 database schema design guidance for designing, reviewing, optimizing, and generating Customer Relationship Management schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to design CRM data models, generate MySQL 8 schema and migration examples, review relationships and indexes, and choose patterns for custom fields, audit trails, activities, and multi-tenant isolation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schema examples could be adopted before CRM privacy, retention, and compliance requirements are fully defined.

Mitigation: Review generated SQL against the deployment's privacy and retention obligations before production use, and add required erasure, audit, and data-retention controls.

Risk: CRM activity and integration schemas can expose sensitive meeting URLs, recording links, message identifiers, or customer data.

Mitigation: Treat those fields as sensitive, apply access controls and encryption where appropriate, and avoid storing unnecessary identifiers or URLs.

Risk: Shared multi-tenant schemas can leak data if tenant consistency is enforced only informally.

Mitigation: Use tenant-scoped indexes and uniqueness rules, require tenant filters in access paths, and add database or application checks that prevent cross-tenant references.

Risk: Seed data scripts and examples may be inappropriate for production databases.

Mitigation: Run seed procedures only in isolated development or test environments, and block seeding workflows from production deployment paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/skills/mysql8-crm-schema-expert)
- [Core CRM Entities](references/core-entities.md)
- [Relationships and Normalization](references/relationships-and-normalization.md)
- [Indexing and Performance](references/indexing-and-performance.md)
- [Custom Fields and Flexibility](references/custom-fields-and-flexibility.md)
- [Audit Trails and Soft Deletes](references/audit-and-soft-deletes.md)
- [Activities and Timeline](references/activities-and-timeline.md)
- [Security and Multi-Tenancy](references/security-and-multitenancy.md)
- [Migrations and Seeding](references/migrations-and-seeding.md)
- [Reference Schemas](references/reference-schemas.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with SQL and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MySQL 8 schema definitions, indexes, migrations, seed data, and review guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
