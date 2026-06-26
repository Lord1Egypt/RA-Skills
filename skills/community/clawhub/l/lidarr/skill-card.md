## Description: <br>
Search and add music to Lidarr. Supports artists, albums, and quality profiles (FLAC preferred). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rappo](https://clawhub.ai/user/rappo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Lidarr, add or monitor artists and albums, inspect profiles, and manage an existing music library through Lidarr API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a Lidarr library by adding artists, monitoring albums, refreshing metadata, or removing artists. <br>
Mitigation: Require explicit user confirmation before running add, monitor-album, refresh, or remove commands. <br>
Risk: The remove --delete-files option can delete media files. <br>
Mitigation: Confirm the target artist ID and file-deletion intent before using --delete-files; prefer removal without file deletion unless explicitly requested. <br>
Risk: The skill uses a Lidarr API key from a local config file. <br>
Mitigation: Keep the config file private, verify the configured Lidarr URL, and avoid sharing or logging the API key. <br>


## Reference(s): <br>
- [Lidarr on ClawHub](https://clawhub.ai/rappo/lidarr) <br>
- [MusicBrainz artist pages](https://musicbrainz.org/artist/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown/plain text with inline bash commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a private Lidarr config file with URL, API key, and profile IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
