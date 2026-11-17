## Description:

Lyrion Music controls Lyrion Music Server (LMS) through its JSON-RPC API for playback, volume, playlist management, player selection, and music library queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent operate a Lyrion Music Server on a trusted network, including playback control, volume changes, playlist updates, player discovery, and library searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can target the wrong Lyrion Music Server if host or port settings are incorrect.

Mitigation: Verify LYRION_HOST and LYRION_PORT before use, and keep the server on a trusted network.

Risk: Playback, volume, power, and playlist commands can change a user's media system state, including clearing playlists.

Mitigation: Require user direction before running state-changing or destructive media actions.

Risk: Untrusted player IDs, search terms, or playlist URIs may be unsafe because JSON escaping needs review.

Mitigation: Avoid passing untrusted values until JSON escaping is fixed or independently validated.

## Reference(s):

- [Lyrion Music Server API Reference](references/api.md)
- [Official Lyrion CLI Documentation](https://lyrion.org/reference/cli/)
- [LMS Community Slimserver Repository](https://github.com/LMS-Community/slimserver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for invoking the bundled LMS shell client and interpreting JSON-RPC responses.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
