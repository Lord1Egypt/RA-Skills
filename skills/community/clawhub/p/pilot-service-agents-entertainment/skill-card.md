## Description: <br>
Provides Pilot Protocol access patterns for entertainment data agents covering games, manga/anime, trivia, fandom catalogs, and related APIs such as PokeAPI, Jikan, CheapShark, TVMaze, Gutenberg, and Shikimori. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and query Pilot Protocol entertainment service agents for structured fandom, game-deal, anime, manga, TV, and catalog metadata. It supports reading agent contracts, sending filtered data requests, and retrieving structured inbox responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends shell-mediated pilotctl messages to overlay service agents and requires a running daemon on network 9. <br>
Mitigation: Confirm the daemon, network, target hostname, and JSON filters before executing commands; use list-agents and /help to verify the current contract. <br>
Risk: Entertainment catalog and deal data may be incomplete, stale, truncated, or dependent on upstream service availability. <br>
Mitigation: Inspect count, total, truncated, pagination, and upstream_url fields in inbox responses before relying on results. <br>
Risk: Summary and free-text responses may be generated prose rather than source data. <br>
Mitigation: Prefer /data responses for decisions that require structured or auditable values, and treat generated summaries as convenience text. <br>


## Reference(s): <br>
- [Skill Definition](SKILL.md) <br>
- [README](README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-entertainment) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses are read asynchronously from pilotctl inbox; summary and free-text responses may be generated prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; skill metadata: 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
