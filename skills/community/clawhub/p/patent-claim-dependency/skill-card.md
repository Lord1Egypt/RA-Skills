## Description:

Maps explicit references among claims in one specified patent text version into a CSV and Mermaid reading map, preserving multiple-reference meaning, added features, and ambiguity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent readers and analysts use this skill to organize claim references and added limitations in a specified text version for review; it does not assess legal dependency validity or infringement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A claim-reference map could be mistaken for a legal conclusion about dependency, validity, or infringement.

Mitigation: Keep the source text, ambiguous relations, and verification items visible, and state that the map does not make legal or infringement determinations.

Risk: Optional PatentMax retrieval may incur charges and requires use of a service credential.

Mitigation: Confirm the retrieval budget first, keep credentials private, and use a temporary credential unless the user explicitly chooses secure local storage.

## Reference(s):

- [Claim map example](references/claim-map-example.md)
- [WIPO PCT Rule 6.4](https://www.wipo.int/en/web/pct-system/texts/rules/r6)

## Skill Output:

**Output Type(s):** [Files, CSV, Markdown]

**Output Format:** [UTF-8 CSV and Markdown with Mermaid flowcharts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes claim-reference rows, added-feature summaries, source locations, and items to verify; preserves multiple-reference semantics and ambiguity.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
