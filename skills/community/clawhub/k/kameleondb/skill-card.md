## Description:

Store and query structured data without planning schemas upfront, while evolving data structures as new fields are discovered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosnataqs](https://clawhub.ai/user/marcosnataqs)

### License/Terms of Use:


## Use Case:

Developers and agents use KameleonDB to create, evolve, query, and optimize persistent structured data stores for contacts, tasks, knowledge bases, external data ingestion, and similar stateful workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad autonomous persistent storage, schema changes, and handling of personal or customer data.

Mitigation: Use a dedicated development or least-privilege database first, avoid storing secrets or regulated personal data by default, and require explicit approval before ingesting customer/contact data or changing schemas.

Risk: Installing or running the database package without verification could expose the agent environment to unreviewed package behavior.

Mitigation: Pin or otherwise verify the kameleondb package before installation and review the package source and security posture before production use.

## Reference(s):

- [KameleonDB GitHub Repository](https://github.com/marcosnataqs/kameleondb)
- [KameleonDB PyPI Package](https://pypi.org/project/kameleondb/)
- [KameleonDB First Principles](https://github.com/marcosnataqs/kameleondb/blob/main/FIRST-PRINCIPLES.md)
- [KameleonDB Architecture Guide](https://github.com/marcosnataqs/kameleondb/blob/main/docs/ARCHITECTURE.md)
- [Example Agent-Driven Data Modeling Workflow](artifact/examples/workflow.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown]

**Output Format:** [Markdown with inline shell, SQL, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the kameleondb CLI and KAMELEONDB_URL environment variable.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
