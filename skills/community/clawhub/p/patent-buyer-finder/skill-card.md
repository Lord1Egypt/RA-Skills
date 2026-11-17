## Description:

Helps patent owners identify companies that may be interested in buying or licensing a patent, using related patents, citations, and recent patent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as university technology-transfer offices, inventors, and patent operators use the skill to identify and prioritize potential corporate buyers or licensees, then prepare a lead list with evidence-based reasons and related patent numbers.

### Deployment Geography for Use:

Global; the documented patent collection covers China, the United States, Europe, Japan, Korea, and WIPO.

## Known Risks and Mitigations:

Risk: The security assessment flags unsafe cache paths and API-key handling.

Mitigation: Prefer a corrected release; until then, use an isolated workspace and a limited trial key, keep the default endpoint, submit only public information, and set a spending limit.

## Reference(s):

- [PatentMax search workflow](artifact/references/search-workflow.md)
- [Patent query construction](artifact/references/query-construction.md)
- [PatentMax API reference](artifact/references/api-reference.md)
- [PatentMax search](https://app.ip930.com/)
- [ClawHub release](https://clawhub.ai/ip930/skills/patent-buyer-finder)

## Skill Output:

**Output Type(s):** [Text, CSV, Guidance]

**Output Format:** [UTF-8 CSV with BOM and conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CSV prioritizes candidate companies and includes evidence-based reasons, related patent publication numbers, region, and notes. Candidate leads do not establish purchase intent or budget.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
