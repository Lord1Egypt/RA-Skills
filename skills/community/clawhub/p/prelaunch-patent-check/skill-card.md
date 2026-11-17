## Description:

Before a product launch, checks each feature for relevant in-force patents, listing the closest ones, their owners and remaining term, as a screening list to decide whether to commission a formal legal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams use this skill before launch to screen each product feature for relevant in-force patents, identify candidates for closer review, and decide whether to commission formal patent legal analysis.

### Deployment Geography for Use:

China, the United States, Europe, Japan, South Korea, and WIPO coverage, as supported by the patent database.

## Known Risks and Mitigations:

Risk: Credential routing needs correction before using a paid key.

Mitigation: Use a version that fixes credential routing; supply a limited-use key outside chat.

Risk: Cache containment and file handling have verified weaknesses.

Mitigation: Use a version that fixes cache containment and avoid confidential product details until then.

Risk: Search-result validation needs improvement.

Mitigation: Use a version that fixes response validation and review the returned patent records; treat results as preliminary screening, not legal clearance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/prelaunch-patent-check)
- [Search workflow](references/search-workflow.md)
- [PatentMax API reference](references/api-reference.md)
- [PatentMax FAQ](references/faq.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV file]

**Output Format:** [Feature-grouped patent screening list and UTF-8 CSV that opens in Excel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary screening only; not a legal opinion or infringement conclusion.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
