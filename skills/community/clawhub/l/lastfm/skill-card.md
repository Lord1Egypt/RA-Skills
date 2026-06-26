## Description: <br>
Access Last.fm listening history, music stats, and discovery. Query recent tracks, top artists/albums/tracks, loved tracks, similar artists, and global charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure read-only Last.fm API lookups and retrieve listening history, music statistics, recommendations, search results, and chart data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented examples use plain HTTP Last.fm API URLs. <br>
Mitigation: Prefer HTTPS API URLs where supported before running requests. <br>
Risk: Expanded shell commands or logs may expose the Last.fm API key. <br>
Mitigation: Avoid sharing commands or logs containing the API key, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Last.fm API account creation](https://www.last.fm/api/account/create) <br>
- [Last.fm API documentation](https://lastfm-docs.github.io/api-docs/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced Last.fm endpoints return JSON responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
