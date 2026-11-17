## Description:

Search Pinterest pins, pull one pin with its save/share counts, read a user's profile and boards, page through a board, and look up how often external URLs have been saved. 6 endpoints, structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Pinterest content, inspect pins, profiles, and boards, and retrieve URL save counts through Scavio's structured Pinterest API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinterest queries, usernames, pin or board URLs, and URL-stat lookups are sent to Scavio and API calls consume credits.

Mitigation: Confirm the data-sharing posture before use, keep SCAVIO_API_KEY in an environment variable or secret store, and monitor credit usage.

Risk: Pinterest profile and pin descriptions may contain user-generated information about real people.

Mitigation: Summarize returned content and avoid building profiles of individuals beyond what the API response directly supports.

## Reference(s):

- [Scavio API Documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=pinterest-api)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/pinterest-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, json]

**Output Format:** [Markdown guidance with shell, Python, curl, and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY and returns cursor-paginated structured JSON from Scavio endpoints.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
