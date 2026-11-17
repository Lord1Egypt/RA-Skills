## Description:

Provides music recommendations, playlist management, music search, lyric lookup, and popular chart retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer music discovery requests, retrieve lyrics, manage favorites and playlists, and look up NetEase music charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Music searches, lyric lookups, and ranking requests may be sent to NetEase music endpoints.

Mitigation: Use the skill only when sharing those requests with the music service is acceptable.

Risk: Favorites, playlists, play counts, and cached lookup results may be stored as local JSON files.

Mitigation: Review, protect, or clear local data files when music preferences are sensitive on the device.

## Reference(s):

- [ClawHub Music Helper Skill Page](https://clawhub.ai/cp3d1455926-svg/skills/music-helper)
- [NetEase Cloud Music](https://music.163.com/)
- [NetEase Cloud Music API Endpoint](https://music.163.com/api)
- [NeteaseCloudMusicApi Reference](https://github.com/Binaryify/NeteaseCloudMusicApi)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown text with optional Python usage examples and local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write favorites, playlists, and cache data as local JSON files; NetEase lookup results may be cached for one hour.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
