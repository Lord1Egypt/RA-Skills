## Description: <br>
Access Last.fm user profile, now playing, top tracks/artists/albums by period, loved tracks, and optionally love/unlove tracks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dennisooki](https://clawhub.ai/user/dennisooki) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to retrieve Last.fm profile and listening-history summaries from an agent. When optional write credentials are provided, the skill can also love or unlove tracks on the user's Last.fm account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Last.fm API keys, session keys, or API secrets could be exposed through repositories, logs, backups, or synced dotfiles. <br>
Mitigation: Store credentials only in the configured environment or secret store, and avoid printing or committing LASTFM_API_KEY, LASTFM_SESSION_KEY, or LASTFM_API_SECRET. <br>
Risk: Optional write credentials allow the agent to change loved-track state on the user's Last.fm account. <br>
Mitigation: Provide LASTFM_SESSION_KEY and LASTFM_API_SECRET only when love or unlove operations are intended; omit them for read-only use. <br>
Risk: Rapid repeated Last.fm requests can exceed the documented service rate limit. <br>
Mitigation: Throttle requests and retry gracefully when Last.fm returns a rate-limit error. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dennisooki/lastfm-openclaw) <br>
- [Last.fm API Endpoints Reference](references/api-endpoints.md) <br>
- [Last.fm Authentication Guide](references/auth-guide.md) <br>
- [Last.fm API documentation](https://www.last.fm/api) <br>
- [Last.fm API account registration](https://www.last.fm/api/account/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq. Read operations require LASTFM_API_KEY and LASTFM_USERNAME; write operations additionally require LASTFM_SESSION_KEY and LASTFM_API_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
