## Description:

Organizes movie recommendations in Obsidian and generates suggestions based on user profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adnxone](https://clawhub.ai/user/adnxone)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal knowledge-base users use this skill to organize movie watchlists, seen movies, recommendations, trailers, streaming notes, and reflection prompts in an Obsidian-style Markdown vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and move files in the configured Obsidian Movies folder.

Mitigation: Scope file access to the configured movie directory and require review before moving or overwriting existing notes.

Risk: The skill can create release reminders through cron.

Mitigation: Require explicit user confirmation for each reminder and show the proposed schedule before creating it.

Risk: The skill may check recent logs or mood signals without clear scoping.

Mitigation: Avoid access to general recent logs or files outside the configured movie directory unless the user explicitly provides them.

Risk: The skill uses online movie lookups for trailers, streaming suggestions, ratings, and posters.

Mitigation: Review external links and fetched metadata before storing them in the vault.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adnxone/skills/movie-manager)
- [Publisher profile](https://clawhub.ai/user/adnxone)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise agent guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update movie watchlist files, seen-movie files, a Movies.md index, a cinematic profile file, and release reminders when permitted.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
