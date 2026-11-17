## Description:

Build a complete OpenClaw agent package for a real profession or job role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliciawque](https://clawhub.ai/user/aliciawque)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate role-ready OpenClaw agent packages for professions such as product manager, software engineer, lawyer, data analyst, designer, and marketer. The generated package centers on role identity, memory, behavior, tools, and supporting skill recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated professional role packages may include inaccurate, incomplete, or overconfident domain guidance.

Mitigation: Review generated role files before deployment and require qualified human review for legal, compliance, engineering, analytics, or business-critical use.

Risk: Tool and MCP recommendations may involve sensitive systems such as files, Docker, email, calendars, CRMs, analytics, legal documents, or long-term memory.

Mitigation: Approve each recommended integration separately and limit permissions to the minimum needed for the deployed agent.

Risk: Broad trigger wording can cause the skill to be used for roles or industries where the bundled references are only a starting point.

Mitigation: Customize outputs for the actual profession, industry, jurisdiction, and operating context before treating the package as deployment-ready.

## Reference(s):

- [Product Manager Reference](references/product-manager.md)
- [Software Engineer Reference](references/software-engineer.md)
- [Lawyer Reference](references/lawyer.md)
- [Data Analyst Reference](references/data-analyst.md)
- [Designer Reference](references/designer.md)
- [Marketer Reference](references/marketer.md)
- [Apache Superset](https://github.com/apache/superset)
- [Evidence](https://github.com/evidence-dev/evidence)
- [Great Expectations](https://github.com/great-expectations/great_expectations)
- [dbt Core](https://github.com/dbt-labs/dbt-core)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown agent package with role-specific configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces soul.md, identity.md, memory.md, agents.md, tools.md, and skills-recommendation.md content for the requested profession.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
