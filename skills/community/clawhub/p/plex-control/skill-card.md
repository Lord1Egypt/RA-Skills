## Description:

A standalone command-line skill to interact with and manage Plex Media Server directly, featuring playback controls and secured temporary caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymgenc](https://clawhub.ai/user/ymgenc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent query a Plex Media Server, search cached library metadata, list active clients and sessions, and control playback from command-line actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Plex library metadata may be cached in a predictable shared temporary file.

Mitigation: Use a limited Plex token where possible, avoid running the skill on shared machines, and clear or relocate the cache until it uses a private per-user cache directory with restrictive permissions and clear retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ymgenc/skills/plex-control)
- [Publisher profile](https://clawhub.ai/user/ymgenc)
- [Skill metadata](artifact/metadata.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Structured JSON from a Python command-line script, with Markdown guidance in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLEX_URL and PLEX_TOKEN; uses uv, python3, and the plexapi dependency; search cache is stored in the OS temporary directory.]

## Skill Version(s):

1.1.0 (source: evidence release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
