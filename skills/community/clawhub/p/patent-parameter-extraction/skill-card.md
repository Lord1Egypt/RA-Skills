## Description:

Extracts process settings, compositions, and test results from patent specifications while linking each value to its example, conditions, original unit, and source passage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent researchers and R&D teams use the skill to organize parameters from supplied patent documents or retrieved specifications into source-linked evidence tables, preserving examples, conditions, units, and items that need verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may misstate the source of patent data.

Mitigation: Name the actual document source in each report, distinguishing user-provided material from data retrieved through PatentMax.

Risk: Trial credentials may be saved without reliably enforced private access.

Mitigation: Prefer local document processing, approve retrieval costs explicitly, keep paid keys temporary, and confirm the credential cache is private before using automatic trials.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [CSV, Markdown, Guidance]

**Output Format:** [UTF-8 CSV evidence table with a Markdown summary and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original values, units, patent passages, conditions, and verification notes; converted values are separately identified when provided.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
