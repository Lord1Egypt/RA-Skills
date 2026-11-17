## Description:

Assesses a public Part 2 patient notice for SUD programs against 42 CFR §2.22(b) and produces a citable coverage map of notice-content gaps without making claims about actual privacy practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, audit, and policy reviewers use this skill to inspect a publicly posted Part 2 patient notice or notice of privacy practices for the specific content elements required by 42 CFR §2.22. It reports document-coverage gaps only, not legal advice or proof of actual program practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output could be mistaken for legal advice or proof of operational compliance.

Mitigation: Treat the output as a public document-coverage review only, and have a qualified compliance professional decide whether and how to act on any gap.

Risk: Incomplete or summarized notice text can cause incorrect absent or insufficient-information classifications.

Mitigation: Use pasted notice text or verbatim page retrieval before finalizing coverage values, especially when classifying missing elements.

Risk: The §2.22 checklist can be misapplied to entities that are not Part 2 programs.

Mitigation: Run the applicability gate first and stop with a scope finding when the subject is not directly bound by the Part 2 patient-notice duty.

## Reference(s):

- [Part 2 Notice Assessment on ClawHub](https://clawhub.ai/dangsllc/skills/part-2-notice-assessment)
- [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills)
- [Rote Compliance](https://rotecompliance.com)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON coverage map with cited findings and a completeness summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are scoped to public notice content and include applicability, source, element coverage, notice language, regulatory anchors, reasoning, and a professional review note.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
