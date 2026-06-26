## Description: <br>
Looks up and adds MusicBrainz music metadata, including artist, release, Spotify-link, and cover-art workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-clawdia](https://clawhub.ai/user/its-clawdia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, music metadata maintainers, and agent users use this skill to check MusicBrainz for existing artists, albums, and releases, then prepare or submit MusicBrainz edits with Spotify links and cover art when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a MusicBrainz account to make authenticated public edits. <br>
Mitigation: Review every proposed artist, release, URL relationship, and cover-art upload before submission. <br>
Risk: MusicBrainz credentials may be stored in a plaintext .credentials.json file. <br>
Mitigation: Use a dedicated MusicBrainz account, avoid password reuse, and remove or restrict the credentials file when it is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/its-clawdia/musicbrainz-importer) <br>
- [MusicBrainz API Reference](artifact/references/api.md) <br>
- [Adding a Release Reference](artifact/references/add-release.md) <br>
- [Release Editor Seeding](artifact/references/seeding.md) <br>
- [MusicBrainz Release Editor Seeding Documentation](https://musicbrainz.org/doc/Development/Seeding/Release_Editor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MusicBrainz identifiers, public edit links, credential setup guidance, and commands that require user review before authenticated writes.] <br>

## Skill Version(s): <br>
1.2.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
