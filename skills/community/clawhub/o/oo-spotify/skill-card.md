## Description:

Spotify (spotify.com). Use this skill for ANY Spotify request — reading, creating, updating, and deleting data. Whenever a task involves Spotify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Spotify account can search Spotify's catalog, read account and playback information, and manage playlists, saved items, follows, and playback through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions install a remote CLI whose installer contents are unverified, and the skill security review says broader agent changes are unexplained.

Mitigation: Review and approve the CLI installation separately, including any changes to other agents' skills; prefer a verified release and disable unwanted skill synchronization.

Risk: Write and destructive actions can change Spotify playback or account data.

Mitigation: Keep the skill's approval requirements for account changes and confirm the exact target and effect before these actions.

## Reference(s):

- [ClawHub Spotify skill release](https://clawhub.ai/oomol/skills/oo-spotify)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Spotify](https://spotify.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON connector results with natural-language guidance; oo CLI actions use shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Spotify data or change playback and account data; write and destructive actions require user confirmation as specified by the skill.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
