## Description:

Provides authenticated Moegirlpedia MediaWiki API access for searching pages, retrieving page content and categories, parsing wikitext, checking user information, and summarizing watchlist or recent changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[annangela](https://clawhub.ai/user/annangela)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve authenticated Moegirlpedia data, including page details, categories, user permissions, watchlist summaries, and recent-change summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Moegirlpedia bot password and can access authenticated data, including watchlist information.

Mitigation: Use a dedicated BotPassword with only the documented basic and watchlist permissions; avoid broad edit, rollback, or account-changing rights.

Risk: Persistent memory may be used for credential-rotation tracking across sessions.

Mitigation: Disable or ignore memory-based rotation tracking unless explicitly desired, and handle password rotation reminders outside persistent memory when needed.

Risk: Security evidence reports dormant account-changing API methods in the bundled client.

Mitigation: Review before installation and run only the documented read, lookup, watchlist, and recent-change operations with least-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/annangela/skills/moegirlpedia-mediawiki-api)
- [Moegirlpedia BotPasswords](https://mzh.moegirl.org.cn/Special:BotPasswords)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON on stdout, with brief text arrays for summary operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports pagination tokens; the skill documentation says not to fetch additional pages unless the user explicitly requests more content.]

## Skill Version(s):

0.7.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
