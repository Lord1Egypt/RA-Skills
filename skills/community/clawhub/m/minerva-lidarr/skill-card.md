## Description:

Interact with Lidarr (music/album manager) via its REST API. Use when searching for artists or albums, checking missing/wanted releases, triggering downloads, or monitoring queue status. Part of the *arr media management suite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minerva-care](https://clawhub.ai/user/minerva-care)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a Lidarr music library through REST API workflows, including artist and album lookup, missing release checks, download searches, and queue monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a live Lidarr instance and may trigger downloads or change media library state.

Mitigation: Confirm targets and command intent before execution, especially add, search, delete, blacklist, and queue operations.

Risk: The Lidarr API key grants control over the configured instance.

Mitigation: Store the API key in a protected secret file and avoid exposing it in logs, prompts, or shared shell history.

## Reference(s):

- [Lidarr API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration guidance, Text]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be reviewed before execution because commands can change a Lidarr library, trigger downloads, delete track files, remove queue items, or blacklist releases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
