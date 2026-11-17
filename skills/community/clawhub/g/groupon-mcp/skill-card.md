## Description:

Search and read Groupon deal listings, deal details, and categories from the terminal without signing in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search or browse Groupon deals by city, retrieve a deal's details, and inspect the category taxonomy from the terminal. Deal lookups use public data and require no login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated cart and purchase actions belong to a separate MCP server and can affect a user's account.

Mitigation: Keep this skill scoped to public deal lookups. If connecting the separate server, review its credential handling, explicitly authorize account access, and confirm each purchase or cart-clearing action.

## Reference(s):

- [Groupon curl recipes](artifact/references/graphql-queries.md)
- [Groupon consumer GraphQL API](https://www.groupon.com/mobilenextapi/graphql)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/groupon-mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text results with Markdown shell commands and jq recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected city, search terms, and current Groupon listings.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
