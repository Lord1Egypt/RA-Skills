## Description:

Looks up Overwatch esports data from Liquipedia and OWTV.gg, using local cache files and optional MPS player-stat summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerotwice](https://clawhub.ai/user/zerotwice)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Overwatch esports questions about tournaments, teams, players, matches, rosters, hero picks, earnings, and player performance from Liquipedia and OWTV.gg data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python and Node commands and may pass scraped or user-provided values through command strings.

Mitigation: Review commands before execution, avoid untrusted shell interpolation, and keep scraping inputs constrained to expected Liquipedia and OWTV URLs.

Risk: The skill writes persistent cache files and the security evidence flags cache path handling for review.

Mitigation: Use a dedicated cache directory, review path handling before installation, and avoid running the skill with broader filesystem privileges than needed.

Risk: The skill scrapes external sites and may suggest using browser profiles or cookies when scraping fails.

Mitigation: Do not use personal Chrome profiles or cookies for scraping; use disposable profiles and comply with source-site access rules.

Risk: The security guidance flags the optional multi-search-engine dependency for pinning or avoidance.

Mitigation: Pin any additional search dependency to a reviewed version, or skip the extra install when it is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zerotwice/skills/liquipedia-overwatch)
- [Liquipedia Overwatch](https://liquipedia.net/overwatch/)
- [OWTV.gg](https://owtv.gg/)
- [Cache data schema](references/schema.md)
- [Liquipedia site structure reference](references/site-structure.md)
- [OWTV tournament ID reference](references/owtv-tournament-ids.md)
- [Cache manager helper](references/cache_manager.py)
- [Player stats summarizer](references/player_stats_summarizer.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with JSON cache files and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent local cache files under the configured Liquipedia cache directory.]

## Skill Version(s):

2.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
