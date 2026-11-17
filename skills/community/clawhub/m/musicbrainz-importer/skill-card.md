## Description:

Looks up MusicBrainz music metadata, finds entries linked to Spotify URLs, and helps add or edit artists, releases, links, and cover art on MusicBrainz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-clawdia](https://clawhub.ai/user/its-clawdia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, metadata curators, and agent users use this skill to check whether music entities already exist on MusicBrainz and to prepare or submit artist, release, Spotify-link, and cover-art edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MusicBrainz credentials may be stored in a plaintext .credentials.json file.

Mitigation: Use a dedicated MusicBrainz password that is not reused elsewhere, prefer environment variables or a secure secret store, and restrict any credential file to owner-only permissions.

Risk: Authenticated browser automation can submit account-changing MusicBrainz edits.

Mitigation: Review every artist, release, Spotify-link, and cover-art edit before submission.

Risk: Unpinned Playwright installation can change browser automation behavior over time.

Mitigation: Pin Playwright or install it from a locked, trusted project directory when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/its-clawdia/skills/musicbrainz-importer)
- [MusicBrainz API Reference](references/api.md)
- [Adding a Release Reference](references/add-release.md)
- [Release Editor Seeding](references/seeding.md)
- [MusicBrainz release editor seeding documentation](https://musicbrainz.org/doc/Development/Seeding/Release_Editor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript snippets, JSON examples, and MusicBrainz identifiers or links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to call MusicBrainz APIs, run local helper scripts, create release-seeding files, and use Playwright for authenticated write operations.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
