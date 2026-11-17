## Description:

Interact with Sonarr (TV show manager) via its REST API for TV series search, missing episode checks, download searches, and queue monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minerva-care](https://clawhub.ai/user/minerva-care)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Sonarr instance through REST API workflows for adding TV series, checking missing episodes, triggering searches, and reviewing download queue status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sonarr API actions can modify a media library, trigger downloads, delete episode files or queue items, blacklist releases, rename files, or rescan folders.

Mitigation: Review proposed commands before execution and only provide the Sonarr API key to agents that are allowed to perform those library-changing actions.

## Reference(s):

- [Sonarr API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Sonarr base URL and API key supplied by the user.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
