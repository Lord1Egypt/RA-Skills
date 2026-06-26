## Description: <br>
Music Helper recommends songs and playlists, searches music metadata, retrieves lyrics, and manages local favorites and playlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and music-focused agent workflows use this skill to answer music recommendation, search, lyric lookup, chart, favorites, and playlist requests. It is most useful when the agent can access NetEase Music endpoints and write local preference files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song searches and lyric lookups may be sent to NetEase Music. <br>
Mitigation: Avoid sensitive music queries on shared systems and review the external service behavior before deployment. <br>
Risk: Favorites, playlists, and cached music results can remain in local JSON files. <br>
Mitigation: Delete generated favorites, playlists, and cache files when retained preferences are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cp3d1455926-svg/music-helper) <br>
- [NetEase Music](https://music.163.com/) <br>
- [NetEase Music API Base](https://music.163.com/api) <br>
- [NeteaseCloudMusicApi Reference](https://github.com/Binaryify/NeteaseCloudMusicApi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text responses with optional Python usage examples and local JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call NetEase Music endpoints and may create or update local favorites, playlists, and cache JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
