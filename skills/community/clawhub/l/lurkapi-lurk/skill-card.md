## Description:

Lurk a brand. From just a name or a website, a one-page snapshot of whether it advertises right now on Meta and Google, what its live ads push, and how big it is on Facebook, Instagram and TikTok, in 4 calls (the run behind the LurkAPI dashboard). Use when the user names a company or domain and asks what it is up to, whether it runs ads, how big it is on social, or wants a quick competitor check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for a quick competitor check when they want to know whether a named brand is advertising on Meta or Google and what its social audience looks like. It produces a concise snapshot from four LurkAPI calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LurkAPI receives the brand searches and authentication key; a normal run consumes four credits.

Mitigation: Keep the key in the documented environment variable and out of chat and logs. Check the account balance before running and send only intended brand searches.

Risk: The supplied security review covers the instructions, not the remote service or a separately installed connector.

Mitigation: Review the remote service and connector independently before connecting an account or relying on returned data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mesmerlord/skills/lurkapi-lurk)
- [LurkAPI dashboard and API key setup](https://lurkapi.com/dashboard)
- [Facebook company search API](https://lurkapi.com/docs/facebook/search-companies.md)
- [Google company ads API](https://lurkapi.com/docs/google/company-ads.md)
- [Facebook company ads API](https://lurkapi.com/docs/facebook/company-ads.md)
- [TikTok profile API](https://lurkapi.com/docs/tiktok/profile.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [One-page Markdown brand snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes estimated ad counts, ad themes, and social audience metrics; a standard run uses four API calls.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
