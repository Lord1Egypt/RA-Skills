## Description:

Find out what real people say about a product, brand, competitor or problem on Reddit. Searches posts, finds the communities that discuss it, reads the most-discussed threads and their comments, then reports the pains, wants, objections, alternatives and exact phrases people use, with links. Use for voice-of-customer and market research, product validation, brand monitoring, "what does Reddit think of X", or before posting in a subreddit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

Product, marketing, and research teams can use this skill to understand how Reddit users discuss a product, brand, competitor, or problem. It gathers relevant posts and comments, then organizes customer pains, alternatives, objections, and recurring language into a linked research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search wording is sent to LurkAPI and API calls consume credits.

Mitigation: Leave confidential details out of queries and check current charges or credit balance before a large research run.

Risk: An exposed API key could allow unauthorized use of the account.

Mitigation: Keep the key in an environment variable and never paste it into chat.

Risk: The linked endpoint documentation and live service behavior were not verified by the supplied security review.

Mitigation: Check current endpoint documentation and service behavior before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mesmerlord/skills/lurkapi-reddit-research)
- [LurkAPI Reddit search documentation](https://lurkapi.com/docs/reddit/search.md)
- [LurkAPI subreddit search documentation](https://lurkapi.com/docs/reddit/subreddit-search.md)
- [LurkAPI subreddit details documentation](https://lurkapi.com/docs/reddit/subreddit-details.md)
- [LurkAPI post comments documentation](https://lurkapi.com/docs/reddit/post-comments.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research report with linked Reddit threads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized by themes, alternatives, exact phrases, takeaways, and sources.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
