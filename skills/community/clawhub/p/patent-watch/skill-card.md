## Description:

Builds reusable patent watch lists and summarizes newly published patents found in later searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users can track competitors or technology areas by maintaining reusable patent searches and baselines, then reviewing newly published patents in subsequent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This version has verified flaws that could expose its API key.

Mitigation: Prefer a release that fixes credential forwarding. If evaluating this version, use a restricted environment and a limited-value API key.

Risk: Crafted patent numbers could access files outside the skill's cache.

Mitigation: Prefer a release that fixes cache-path validation; avoid exposing sensitive local files while evaluating this version.

Risk: Searches disclose research interests to PatentMax, API calls may incur charges, and credentials may persist locally.

Mitigation: Avoid sensitive queries, limit-value credentials and spending, and independently verify empty statistics before relying on a report.

## Reference(s):

- [PatentMax API Platform](https://api.ip930.com/features/api-platform)
- [PatentMax Search](https://app.ip930.com/)

## Skill Output:

**Output Type(s):** [text, CSV]

**Output Format:** [Conversational patent update summaries and Excel-compatible CSV watch lists and reports]

**Output Parameters:** [Watch targets, search queries, baseline and check dates, and newly published patent records]

**Other Properties Related to Output:** [The user initiates each run; monitoring is not scheduled automatically. Patent publication delays and database coverage limit results.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
