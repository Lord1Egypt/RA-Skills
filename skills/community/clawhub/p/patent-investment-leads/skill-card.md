## Description:

Helps industrial parks identify out-of-region companies with active patent activity in a target sector and compile investment-promotion leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Industrial parks and investment-promotion teams can use the skill to find out-of-region companies with patent activity in a chosen sector, review patent-based growth and provincial footprints, and prepare a lead list. Its results are based on public patent information and are not a substitute for commercial due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key protection and cache-file handling weaknesses warrant review.

Mitigation: Use approved HTTPS destinations, protect credentials across redirects, restrict cache paths, store keys securely, and never share production keys in chat.

Risk: Queries are sent to PatentMax and may consume paid credits.

Mitigation: Send only approved information and set a spending limit before running paid searches.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ip930/skills/patent-investment-leads)
- [PatentMax](https://ip930.com)
- [API reference](references/api-reference.md)
- [Search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Files]

**Output Format:** [A concise Chinese-language summary and a UTF-8-with-BOM CSV lead list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The list summarizes company, province, patent activity, expansion signals, existing provincial footprint, and technology; patent activity alone does not establish commercial suitability.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
