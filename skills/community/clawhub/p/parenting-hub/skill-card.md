## Description:

Use when the user needs source-linked parenting guidance from the public Mom AI Agent evidence intelligence API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jupitlunar](https://clawhub.ai/user/jupitlunar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer parenting questions with source-linked guidance from the public Mom AI Agent knowledge API. It is intended for read-only retrieval with explicit age, locale, urgency, source, and coverage boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle includes an operational crawler playbook that describes scraper execution and database or local content writes outside the stated read-only parenting retrieval scope.

Mitigation: Deploy the skill as read-only retrieval only, or remove/split the crawler playbook into a separately reviewed administrator skill with explicit write access, browser automation limits, domain limits, and user confirmation.

Risk: Parenting questions can include sensitive family, child, location, or medical details that would be forwarded to an external public API.

Mitigation: Ask users to avoid names, contact details, exact addresses, and unnecessary medical history; send only the minimum context needed for the source-linked parenting question.

Risk: Retrieved parenting evidence could be mistaken for individualized diagnosis, treatment, or emergency clearance.

Mitigation: Keep responses educational and source-bound, preserve the skill's urgency ladder, and escalate fever in young infants, breathing trouble, dehydration, seizures, unresponsiveness, allergic reactions, heavy postpartum bleeding, chest pain, or self-harm risk to clinician or emergency care.

Risk: A weak or missing match in the public KB API could be misread as proof that the broader website has no relevant content.

Mitigation: State coverage limits clearly: the skill searches public KB, evidence-qualified insight, and topic surfaces, not the full website article corpus.

## Reference(s):

- [Mom AI Agent public knowledge API](https://www.momaiagent.com/api/kb)
- [ClawHub skill page](https://clawhub.ai/jupitlunar/skills/parenting-hub)
- [API Reference](references/api.md)
- [Architecture Boundary](references/architecture.md)
- [High-Risk Examples](references/high-risk-examples.md)
- [Current-Site Deep Search Playbook](references/current-site-deep-search-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown with source, scope, urgency, read-next, and evidence sections when supported by retrieved API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay within public /api/kb/* retrieval results and should not present individualized diagnosis, treatment, or emergency clearance.]

## Skill Version(s):

1.0.0 (source: release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
