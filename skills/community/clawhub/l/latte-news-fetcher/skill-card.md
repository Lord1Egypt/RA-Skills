## Description:

Fetches daily news lists and article summaries, including workflows that attempt to access full text through public archive, extraction, browser, and search services.

This skill is for research and development only.

## Publisher:

[luogao2333](https://clawhub.ai/user/luogao2333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current news by preference or source, summarize article links, and look for accessible full-text or alternative-source coverage. It is especially suited to personal news review workflows where source links and concise Markdown summaries are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes workflows that attempt paywall bypass and may conflict with publisher terms, copyright expectations, or local rules.

Mitigation: Use authorized, free, or alternative sources where possible, and confirm that any access method complies with the relevant publisher terms and local requirements.

Risk: Article URLs or content may be sent to third-party extraction, archive, or search services.

Mitigation: Do not provide private, signed, internal, account-specific, or otherwise sensitive URLs; disclose and review third-party service use before deployment.

Risk: Using a logged-in browser profile could expose the user's authenticated session to agent actions.

Mitigation: Use an isolated browser profile by default and require explicit user consent before accessing logged-in sessions.

Risk: News summaries and alternate-source synthesis can be incomplete, delayed, or misleading.

Mitigation: Keep source links visible, prefer primary or reputable free sources, and tell users when full text could not be verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luogao2333/skills/latte-news-fetcher)
- [Project Homepage](https://github.com/luogao2333/Latte-news-fetcher)
- [Professional News Source List](references/news-sources.md)
- [Free News Sources and RSS](references/free-sources.md)
- [Paywall Difficulty Matrix](references/paywall-matrix.md)
- [Bypass Tool Comparison](references/bypass-tools.md)
- [Advanced Techniques and Tools](references/advanced-techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news lists, article summaries, source links, optional shell commands, and plain-text script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write CONFIG/news-preferences.md and may use browser, web fetch, public extraction services, or Tavily when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
