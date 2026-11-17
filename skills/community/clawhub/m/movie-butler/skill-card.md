## Description:

A Chinese-language movie assistant that helps agents query TMDB and Emby/Plex, compare media-library availability, record viewing preferences, and produce personalized movie recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT

## Use Case:

External users who manage personal media libraries use this skill to query movie information, check whether titles exist on an Emby or Plex server, keep viewing-history notes, and receive weekly or context-aware recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media-server credentials or API keys could be exposed or reused unsafely.

Mitigation: Remove hard-coded keys, rotate any exposed secrets, require user-provided credentials, avoid putting Emby tokens in URLs, and prefer HTTPS for media-server access.

Risk: Local viewing history, ratings, mood, work status, and interests may reveal personal preferences.

Mitigation: Give users clear controls to review, delete, or disable local memory and document what personal context is stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhilei951/skills/movie-butler)
- [Publisher profile](https://clawhub.ai/user/duzhilei951)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text responses with movie summaries, recommendations, viewing records, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include media-library status, ratings, recommendation reasons, and local viewing-memory updates.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
