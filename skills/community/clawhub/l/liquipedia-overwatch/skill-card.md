## Description: <br>
Helps an agent answer Overwatch esports questions by querying Liquipedia and OWTV.gg, normalizing results into structured data, and presenting concise summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZEROTWICE](https://clawhub.ai/user/ZEROTWICE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve Overwatch tournament, team, player, match, earnings, hero-pick, and player-stat information from esports sources. It is useful for answering current or historical Overwatch competitive questions with cached structured JSON and human-readable Markdown-style summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the cache helper can write outside the intended cache folder if given a crafted ID. <br>
Mitigation: Use only trusted cache IDs, inspect cache paths before shared use, and require path validation that keeps writes under /workspace/liquipedia-cache before deploying in sensitive workspaces. <br>
Risk: The skill can rely on public esports scraping, third-party fallback searches, and locally cached data. <br>
Mitigation: Treat fetched and fallback content as untrusted, cite source URLs and timestamps in responses, and refresh or discard stale cached records for current matches, rosters, and transfers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZEROTWICE/liquipedia-overwatch) <br>
- [Publisher profile](https://clawhub.ai/user/ZEROTWICE) <br>
- [Liquipedia Overwatch](https://liquipedia.net/overwatch/Overwatch_Champions_Series) <br>
- [OWTV.gg](https://owtv.gg) <br>
- [Schema reference](references/schema.md) <br>
- [Site structure reference](references/site-structure.md) <br>
- [OWTV tournament IDs](references/owtv-tournament-ids.md) <br>
- [Cache manager](references/cache_manager.py) <br>
- [Player stats summarizer](references/player_stats_summarizer.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with source URLs and timestamps, plus structured JSON cache records when saving or loading data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute scraping and cache-management commands; successful fetches are stored under the local Liquipedia cache.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
