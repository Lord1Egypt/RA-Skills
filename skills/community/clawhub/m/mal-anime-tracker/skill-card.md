## Description:

Track and manage MyAnimeList anime and manga lists, query titles and forums, and generate update notifications for new episodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josetseph](https://clawhub.ai/user/josetseph)

### License/Terms of Use:

MIT-0

## Use Case:

External users and anime or manga fans use this skill to search MyAnimeList, inspect personal lists, update or remove anime list entries, refresh OAuth tokens, and produce episode-update notification text for OpenClaw delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires MyAnimeList OAuth credentials that can read and modify MAL account data.

Mitigation: Store credentials in the OpenClaw vault or another secret manager, avoid shell profiles and project .env files, and do not run token commands where output is logged.

Risk: Update and delete commands can change or remove entries from a user's MyAnimeList anime list.

Mitigation: Manually confirm anime IDs and intended status changes before running update or delete commands.

## Reference(s):

- [MAL Anime Tracker on ClawHub](https://clawhub.ai/josetseph/skills/mal-anime-tracker)
- [MyAnimeList Developer Portal](https://myanimelist.net/apiconfig)
- [MyAnimeList API OpenAPI Specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output can include MyAnimeList search results, list data, status update responses, delete confirmations, refreshed OAuth tokens, and episode-update notification text.]

## Skill Version(s):

1.9.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
