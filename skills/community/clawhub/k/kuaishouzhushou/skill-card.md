## Description:

Searches public Kuaishou videos by keyword, retrieves creators’ public posts, and fetches video comments and engagement data as structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, social media operators, brand marketers, and analysts use it to find Kuaishou content, review public creator posts, and inspect video comments and engagement metrics for content planning and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security inspection was incomplete: 12 of 32 components were only partially inspected, so the benign verdict has medium confidence.

Mitigation: Review the partially inspected components before installation; the scan does not establish that the artifact is risk-free.

## Reference(s):

- [Usage options](references/options.md)
- [Release changelog](references/changelog.md)
- [快手运营助手官网](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishouzhushou)
- [Publisher profile](https://clawhub.ai/user/why20261)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON envelope containing public video search results, creator posts, or video comments and engagement fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Kuaishou data only; requires GUAIKEI_API_TOKEN; result limits depend on the account plan.]

## Skill Version(s):

1.1.2 (source: server release metadata, frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
