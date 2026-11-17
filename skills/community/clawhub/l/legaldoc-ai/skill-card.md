## Description:

LegalDoc AI helps legal professionals extract contract clauses, summarize legal documents, conduct legal research, and track deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manas-io-ai](https://clawhub.ai/user/manas-io-ai)

### License/Terms of Use:

Commercial

## Use Case:

Attorneys, paralegals, corporate counsel, litigation teams, and legal operations staff use this skill to speed up document-intensive legal workflows while keeping human review in the loop. It supports clause extraction, document summaries, research queries, deadline extraction, and deadline tracking for legal matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process privileged or client-identifying legal information and send research queries, alerts, storage data, or practice-management data to third-party services.

Mitigation: Confirm firm data-handling approval before use, minimize client-identifying details in external searches, and disable integrations that are not approved for privileged data.

Risk: Deadline and statute-of-limitations outputs may be incomplete or incorrect.

Mitigation: Require attorney verification against source documents, court rules, and applicable law before relying on any deadline.

Risk: Deadline records are persisted locally and the provided configuration does not enable encryption at rest by default.

Mitigation: Store the deadline database in a protected location, apply filesystem encryption or an encrypted replacement store, and restrict access to authorized legal staff.

Risk: The artifact makes strong security and compliance claims while the server scan flags under-disclosed data flows and overstated security claims.

Mitigation: Validate vendor security documentation, data retention, audit logging, and compliance commitments before production deployment.

## Reference(s):

- [LegalDoc AI ClawHub Page](https://clawhub.ai/manas-io-ai/skills/legaldoc-ai)
- [LegalDoc AI Documentation](https://docs.legaldoc.ai)
- [LegalDoc AI API Reference](https://docs.legaldoc.ai/api)
- [Clause Type Glossary](https://docs.legaldoc.ai/clauses)
- [Integration Guides](https://docs.legaldoc.ai/integrations)
- [LegalDoc AI Best Practices](https://docs.legaldoc.ai/best-practices)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown, JSON, tables, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local legal documents, write deadline records, query external legal research providers, and generate risk notes or suggested revisions for attorney review.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
