## Description:

Find public posts near a user-selected place, quote them, and compare their writing with the user's; requires the PowPop MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to review public posts near a place and compare the text with their own writing. They choose whether to like any of the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published posts and attached images may reveal location or personal information.

Mitigation: Review the location, text, and attached images before approving publication.

Risk: Liking an expired post can extend its visibility by 24 hours.

Mitigation: Check the post's status and account for the extra visibility before approving a like.

Risk: Nearby search results may omit posts that use different place labels.

Mitigation: Treat search results as partial and do not present them as a complete record.

## Reference(s):

- [PowPop skill release](https://clawhub.ai/durenzidu/skills/powpop-two-stories)
- [PowPop MCP server](https://global.powpow.online/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Text with quoted posts and concise comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to five posts, with dates and approximate distances when available.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
