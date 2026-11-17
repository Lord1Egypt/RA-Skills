## Description:

专利对标、和标杆企业比差距，分析双方技术布局并输出 Excel 可打开的差距清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Companies and patent teams use this skill to compare their patent portfolio with a selected benchmark company, identify underrepresented technology areas and distinctive strengths, and plan patent strategy. It returns a gap list with representative patents and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and cache-path safeguards need review; company and technical queries may be sent to an external service.

Mitigation: Validate cache paths and use a limited credential stored in a protected environment. Keep the documented HTTPS endpoint, verify the request origin, set a spending limit, and obtain approval before sending company or technical queries for external processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/patent-benchmark-gap)
- [PatentMax API reference](artifact/references/api-reference.md)
- [Patent comparison workflow](artifact/references/search-workflow.md)
- [Query construction guide](artifact/references/query-construction.md)
- [PatentMax](https://ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [UTF-8 CSV with BOM and concise written recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CSV lists technology gaps and distinctive areas, with company counts, portfolio shares, representative patents, and suggested actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
