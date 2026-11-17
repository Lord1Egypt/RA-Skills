## Description:

Search and add music to Lidarr. Supports artists, albums, and quality profiles (FLAC preferred).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rappo](https://clawhub.ai/user/rappo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Lidarr, add or monitor artists and albums, view configuration, refresh metadata, and remove artists from a Lidarr music library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the Lidarr library, including removing artists and potentially deleting managed media files.

Mitigation: Review proposed commands before execution and require explicit human confirmation before running remove or --delete-files commands.

Risk: The skill depends on a Lidarr URL and API key, and insecure configuration can expose or misuse those credentials.

Mitigation: Prefer an HTTPS Lidarr URL, use placeholder-only API keys in shared examples, and restrict permissions on the credential file.

## Reference(s):

- [ClawHub Lidarr skill page](https://clawhub.ai/rappo/skills/lidarr)
- [ClawHub publisher profile for rappo](https://clawhub.ai/user/rappo)
- [MusicBrainz artist pages](https://musicbrainz.org/artist/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, plus a local Lidarr URL, API key, and quality and metadata profile IDs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
