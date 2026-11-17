## Description:

Query On the Cheap city sites from the shell for local event listings and searchable articles about free and inexpensive activities when the onthecheap MCP server is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to find local events, deals, and articles about free or inexpensive activities across supported On the Cheap city sites when the onthecheap MCP server is unavailable.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The examples fetch public web pages and parse their responses with local shell and Python commands.

Mitigation: Review request URLs and commands before running them; confirm the returned event date and treat month calendar grids as partial listings.

## Reference(s):

- [Ready-to-run recipes](references/recipes.md)
- [Charlotte On the Cheap](https://www.charlotteonthecheap.com)
- [Mile High On the Cheap](https://www.milehighonthecheap.com)
- [Triangle On the Cheap](https://triangleonthecheap.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summaries and tables of local event listings, deals, and article search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected city, date, and search terms; listings can change over time.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
