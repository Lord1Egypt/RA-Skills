## Description:

Track and recommend TV shows and movies using Trakt.tv, including watch history, watchlists, search, trending content, and personalized suggestions based on viewing history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3nch13](https://clawhub.ai/user/fr3nch13)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to connect an agent to a Trakt.tv account so it can answer viewing-history questions, suggest shows or movies, search titles, inspect watchlists, and surface trending content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup stores sensitive Trakt client credentials and OAuth tokens in ~/.openclaw/trakt_config.json with weak storage.

Mitigation: Use a dedicated Trakt application, restrict permissions to what the skill needs, and store the configuration file with owner-only permissions.

Risk: Installation guidance includes pip usage with --break-system-packages.

Mitigation: Install dependencies in a virtual environment and avoid modifying system Python packages.

Risk: The PIN authentication command can be unsafe if an agent builds a shell command from untrusted input.

Mitigation: Enter the PIN only into the intended authentication script invocation after reviewing the exact command.

Risk: Authenticated commands can access personal viewing data and may update Trakt watch history.

Mitigation: Confirm write actions before execution and avoid granting broad Trakt permissions unless they are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fr3nch13/skills/openclaw-trakt)
- [Trakt API documentation](https://trakt.docs.apiary.io/)
- [Trakt OAuth applications](https://trakt.tv/oauth/applications)
- [Trakt API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API/client output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Trakt configuration and token data during setup; runtime commands call Trakt API endpoints for account-specific media data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
