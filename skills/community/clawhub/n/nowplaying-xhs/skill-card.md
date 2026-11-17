## Description:

NowPlaying XHS recommends current theatrical movies by retrieving recent listings, ratings, reputation signals, box-office news, and nearby showtime context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeu1688](https://clawhub.ai/user/seeu1688)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to answer moviegoing questions with current cinema recommendations, ratings comparisons, and available showtime context. It is most useful when a user wants a ranked, source-aware report for films showing now or soon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install global browser tooling before using direct showtime scraping.

Mitigation: Review before installation and avoid global agent-browser installation unless it is approved for the restricted runtime.

Risk: The chart screenshot workflow can leave a local web server running from a shared temporary folder.

Mitigation: Serve only a private temporary directory bound to localhost, and guarantee cleanup after screenshots are captured.

Risk: Movie, city, location, and preference queries may be sent to external search or movie-data providers.

Mitigation: Use the skill in a restricted environment, minimize location and preference details, and disclose external provider use to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seeu1688/skills/nowplaying-xhs)
- [Publisher profile](https://clawhub.ai/user/seeu1688)
- [Rotten Tomatoes movies in theaters](https://www.rottentomatoes.com/browse/movies_in_theaters)
- [Variety film coverage](https://variety.com/v/film/)
- [Maoyan Pro box office](https://piaofang.maoyan.com/)
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search)
- [Chart.js browser bundle](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, inline links, chart-rendering snippets, and optional screenshot attachments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a dated Markdown report under /tmp when the bundled script is executed; recommendations depend on external movie, search, and showtime providers plus any user location or preference details provided.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
