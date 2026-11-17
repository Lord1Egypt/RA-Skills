## Description:

Screens a technology area or company patent portfolio using visible indicators such as maintenance duration, citations, ranking, and claim breadth, then produces a shortlist with reasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External patent researchers, IP teams, and business analysts use it to shortlist patents for further review, protection planning, or pre-assessment. It is an indicator-based screen, not a patent valuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential destination checks and cache-path containment warrant review before production use.

Mitigation: Ask the publisher to address these issues before using a production key. Until then, use an isolated workspace and a limited trial key, avoid sharing keys in chat, submit only information approved for disclosure, and set a spending limit.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Patent search syntax](references/query-syntax.md)
- [Patent search workflow](references/search-workflow.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [ClawHub skill release](https://clawhub.ai/ip930/skills/high-value-patents)

## Skill Output:

**Output Type(s):** [Analysis, CSV, Text]

**Output Format:** [Ranked CSV shortlist with a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes selection reasons and source notes where available; screening indicators are not a formal valuation.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
