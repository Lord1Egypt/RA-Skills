## Description:

MovieMovie helps agents search movie torrent and magnet-link resources, recommend trending movies with confirmed downloadable results, and find subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunhai1994](https://clawhub.ai/user/kunhai1994)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for movie search, trending movie recommendations, torrent or magnet-link availability summaries, and subtitle discovery. It is intended for environments where contacting torrent-related services is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts torrent-related services during use and checks torrent-source reachability automatically on session start.

Mitigation: Use it only in environments where torrent-site access is allowed, and review or disable session-start hooks before installation when automatic network checks are not acceptable.

Risk: Movie search terms and interests may be sent to multiple third-party services and observed by network monitors.

Mitigation: Treat search queries as externally disclosed and avoid submitting sensitive viewing interests or private investigation details.

Risk: The artifact encourages users to paste API keys into chat for configuration.

Mitigation: Configure TORRENTCLAW_API_KEY and TMDB_API_KEY through environment variables or approved secret-management settings instead of chat messages.

Risk: The source claims it does not send user data to third parties, but the security evidence flags that claim as inaccurate for search behavior.

Mitigation: Document third-party service contact clearly for users and review all external endpoints before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kunhai1994/skills/moviemovie)
- [Publisher Profile](https://clawhub.ai/user/kunhai1994)
- [TMDb API Search Endpoint](https://api.themoviedb.org/3/search/movie)
- [Rotten Tomatoes Movies at Home Popular Browse](https://www.rottentomatoes.com/browse/movies_at_home/sort:popular)
- [Douban Movie Chart](https://movie.douban.com/chart)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with inline links and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include movie metadata, reviews, torrent availability summaries, magnet links, subtitle links, source reachability status, and API-key setup guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
