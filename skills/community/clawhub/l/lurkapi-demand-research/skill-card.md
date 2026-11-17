## Description:

Check whether people want a product or niche, and what exactly they want, from live public signals. What they type into Google and TikTok Shop, what sells on eBay and at what price, how much attention the topic gets on TikTok and YouTube, what Reddit complains about, and whether the news is picking it up. Use for product validation, niche and keyword research, pricing research, "is there demand for X", or sizing up a category before launching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

Product founders, marketers, and researchers can use this skill to assess demand for a product or niche before investing in a launch. It gathers public search, marketplace, social, forum, and news signals and organizes them into a demand report with price bands and product opportunities.

### Deployment Geography for Use:

Global; TikTok Shop suggestions and eBay results are US-focused.

## Known Risks and Mitigations:

Risk: Search terms and URLs sent to LurkAPI may reveal sensitive interests; its privacy policy says request parameters are logged for 14 days and the account's first request is retained with the account.

Mitigation: Use only search terms and URLs you are comfortable sharing with LurkAPI, and review its privacy policy before use.

Risk: An exposed LurkAPI key could allow unauthorized API use and credit consumption.

Mitigation: Keep the key out of chat and configure it through the documented environment variable.

Risk: API calls consume account credits, and remote service behavior was not audited.

Mitigation: Agree on a credit budget before research runs and review external results before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mesmerlord/skills/lurkapi-demand-research)
- [Google Autocomplete API documentation](https://lurkapi.com/docs/google/autocomplete.md)
- [TikTok Shop Suggestions API documentation](https://lurkapi.com/docs/tiktok/shop-suggestions.md)
- [eBay Search API documentation](https://lurkapi.com/docs/ebay/search.md)
- [TikTok Search Keyword API documentation](https://lurkapi.com/docs/tiktok/search-keyword.md)
- [YouTube Search API documentation](https://lurkapi.com/docs/youtube/search.md)
- [Reddit Search API documentation](https://lurkapi.com/docs/reddit/search.md)
- [Google News API documentation](https://lurkapi.com/docs/google/news.md)
- [LurkAPI Privacy Policy](https://lurkapi.com/privacy)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown report with a signal summary, demand assessment, price bands, and evidence-based product ideas.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Centered on one product or category seed; evidence depends on the selected market and available public signals.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
