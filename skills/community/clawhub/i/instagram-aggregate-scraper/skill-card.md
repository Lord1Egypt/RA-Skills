## Description:

Instagram社媒数据采集 helps agents query Instagram users, posts, Reels, Stories, comments, searches, hashtags, and locations through MaxHub's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, creator, and analysis teams use this skill to gather and summarize Instagram profile, content, search, hashtag, location, and engagement data. It supports bilingual English and Chinese workflows for browsing, analysis, and comparison tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MaxHub API key and sends queried Instagram identifiers to www.aconfig.cn.

Mitigation: Install only when the publisher and MaxHub are trusted, keep the API key scoped and secret, and avoid exposing unrelated secrets in the install environment.

Risk: Returned third-party social media data may be incomplete, unavailable, or suitable only for reference.

Mitigation: Review API responses before making decisions and disclose any skipped endpoints, empty results, or permission limitations in user-facing summaries.

Risk: Incorrect endpoint paths or parameter names can waste API calls or produce failed requests.

Mitigation: Use the bundled reference files and documented full paths instead of guessing endpoints or cross-version parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/instagram-aggregate-scraper)
- [MaxHub API website](https://www.aconfig.cn)
- [README.md](artifact/README.md)
- [User Data API](artifact/references/api-user.md)
- [Post Data API](artifact/references/api-post.md)
- [Search & Explore API](artifact/references/api-search.md)
- [Parameter Mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, summaries, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs match the user's detected language and summarize data returned by the MaxHub API.]

## Skill Version(s):

3.6.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
