## Description:

Production-ready Master Data Intelligent Matching System for matching vendor, customer, employee, and other records across procurement, finance, sales, and HR domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woaim65](https://clawhub.ai/user/woaim65)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, data stewards, and developers use this skill to reconcile OCR-extracted entities against master-data records, deduplicate records, verify field-level differences, and route uncertain matches to human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive business, HR, tax, bank, and employee identifier data.

Mitigation: Use it only inside a controlled matching workflow with appropriate access controls, data-handling review, and explicit human approval before creating or updating master records.

Risk: Evidence.security reports an unsafe active-learning dynamic-key handling issue.

Mitigation: Fix or isolate active-learning updates before processing untrusted OCR fields or review payloads, and validate allowed domains, events, and field names.

Risk: The artifact supports a skipHitl option and confidence-based auto decisions can affect match review behavior.

Mitigation: Disable HITL bypass for production record changes and require reviewer approval for low-confidence matches, mismatches, new information, and create/update actions.

## Reference(s):

- [Architecture](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JavaScript module results, JSON-like objects, and text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns confidence scores, color labels, field verification states, human-review payloads, and active-learning statistics.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
