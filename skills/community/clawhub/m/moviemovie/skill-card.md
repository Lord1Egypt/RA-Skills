## Description: <br>
Searches movie torrent and magnet-link resources, verifies availability, and recommends trending downloadable movies with optional subtitle and review lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunhai1994](https://clawhub.ai/user/kunhai1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and movie-focused agents use this skill to find films, confirm downloadable torrent or magnet resources, compare quality and size tiers, and locate subtitles. It is intended for movie search and recommendation workflows where live source availability matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches torrent and magnet-link sources, which can produce legally sensitive or untrusted results. <br>
Mitigation: Review results before use, follow applicable law and platform policy, and treat external links and magnet metadata as untrusted. <br>
Risk: A SessionStart hook can automatically run network source checks when the skill starts. <br>
Mitigation: Disable or remove the SessionStart hook if automatic startup network checks are not desired. <br>
Risk: API-key guidance can lead users to expose secrets if keys are pasted into unsafe contexts. <br>
Mitigation: Configure TORRENTCLAW_API_KEY and TMDB_API_KEY only through environment variables or a trusted secrets UI. <br>
Risk: Broad activation wording can trigger the skill for general movie or download requests. <br>
Mitigation: Review invocation behavior and limit use to intentional movie search, recommendation, and subtitle workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kunhai1994/moviemovie) <br>
- [Rotten Tomatoes popular at home](https://www.rottentomatoes.com/browse/movies_at_home/sort:popular) <br>
- [Rotten Tomatoes box office](https://www.rottentomatoes.com/browse/movies_in_theaters/sort:top_box_office) <br>
- [Douban movie chart](https://movie.douban.com/chart) <br>
- [TMDb movie search API](https://api.themoviedb.org/3/search/movie) <br>
- [TMDb weekly trending API](https://api.themoviedb.org/3/trending/movie/week) <br>
- [SubHD search](https://subhd.tv/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with movie recommendations, torrent or magnet details, subtitle links, and optional JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external links, quality tiers, seed counts, file sizes, and environment setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
