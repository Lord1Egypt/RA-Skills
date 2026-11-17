## Description:

Find patents associated with a brand's product by identifying company-name variants, searching by product and component across patent types, and grouping results into a product patent list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users, including product researchers, procurement teams, and sellers, can identify patents associated with a brand and product, review them by component, and export a grouped CSV list. The skill supports patent research and does not determine infringement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted patent numbers could escape the skill's file cache.

Mitigation: Wait for a fix; if testing this release, use an isolated writable directory.

Risk: Redirects could expose the API key.

Mitigation: Wait for authenticated-redirect fixes and use a limited trial credential when testing.

Risk: Searches could disclose confidential invention details or exceed intended spending.

Mitigation: Exclude confidential details from searches and agree on spending limits; avoid sending production keys through chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/product-patent-check)
- [Patent search workflow](references/search-workflow.md)
- [Patent query syntax](references/query-syntax.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [CSV, Text]

**Output Format:** [UTF-8 CSV patent list with a concise chat summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV entries are grouped by product component and include patent bibliographic details and a brief relevance description.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
