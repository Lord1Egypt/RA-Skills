## Description:

Generates a structured Chinese-language PRD in Markdown from prototype or page descriptions, then self-checks for consistency, missing items, and out-of-scope content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosscui-chy](https://clawhub.ai/user/rosscui-chy)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, business analysts, and developers use this skill to convert scoped prototype or page descriptions into formal PRD documents. It is intended for Chinese-language requirements writing where scope boundaries, template conformance, and consistency checks are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated implementation notes, API details, or estimates may be incomplete or misleading when the prototype or scope is incomplete.

Mitigation: Review generated PRD content before treating it as authoritative, and provide clear scope, readable prototype details, and template preference when requested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rosscui-chy/skills/prd-generator-from-prototype)
- [Skill Definition](artifact/SKILL.md)
- [Business PRD Template](artifact/template_business.md)
- [Data Analysis PRD Template](artifact/template_analysis.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown PRD document with consistency self-check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are constrained to the user-provided scope and may ask for missing scope, prototype, or template information before generating a full PRD.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
