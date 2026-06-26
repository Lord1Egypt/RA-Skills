## Description: <br>
Track and recommend TV shows and movies using Trakt.tv for users who ask for recommendations, watch history, watchlists, search, trending content, or personalized suggestions based on viewing history; full functionality requires a Trakt.tv account with a Pro subscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3nch13](https://clawhub.ai/user/fr3nch13) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to connect an assistant to their Trakt.tv account for viewing recommendations, watch history summaries, watchlist checks, search, and trending content discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle and persist sensitive Trakt credentials and OAuth tokens. <br>
Mitigation: Enter secrets locally rather than in chat and protect ~/.openclaw/trakt_config.json with owner-only permissions. <br>
Risk: The skill can give the assistant ongoing access to Trakt account data and viewing history. <br>
Mitigation: Use the narrowest Trakt application permissions possible and review account access periodically. <br>
Risk: Commands may change Trakt account state, including watchlist or history-related actions. <br>
Mitigation: Require explicit user confirmation before running commands that modify watch history, watchlists, or account data. <br>


## Reference(s): <br>
- [Trakt API Reference](references/api.md) <br>
- [Trakt API Documentation](https://trakt.docs.apiary.io/) <br>
- [Trakt Application Settings](https://trakt.tv/oauth/applications) <br>
- [ClawHub Skill Page](https://clawhub.ai/fr3nch13/openclaw-trakt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide OAuth PIN setup and local credential storage for Trakt.tv.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
