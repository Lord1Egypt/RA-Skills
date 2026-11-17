## Description:

Analyzes a user's NetEase Cloud Music playlist and recommends non-repeated songs with free Bilibili links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze a NetEase Cloud Music playlist, infer listening preferences, and produce a daily list of song recommendations with Bilibili links while avoiding prior recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples include user-controlled playlist IDs, artist names, and song titles.

Mitigation: Validate playlist IDs as numeric, avoid shell interpolation for search values, and execute helpers with argument arrays.

Risk: Playlist IDs and search terms are sent to NetEase Cloud Music and Bilibili.

Mitigation: Tell users before external lookups and avoid submitting private or sensitive playlist/search data.

Risk: Recommendation history is stored in the OpenClaw workspace.

Mitigation: Review retention expectations and clear or protect the history directory when recommendations should not persist.

Risk: The workflow writes playlist data to a predictable /tmp path.

Mitigation: Use a secure temporary file or workspace-scoped path instead of predictable /tmp filenames.

## Reference(s):

- [Music Recommender on ClawHub](https://clawhub.ai/geekfoxcharlie/skills/music-recommender)
- [NetEase Cloud Music playlist endpoint](https://music.163.com/api/v6/playlist/detail?id=<ID>&n=1000)
- [Bilibili search endpoint](https://api.bilibili.com/x/web-interface/search/all/v2?keyword=<query>)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Plain text or Markdown recommendations with song names and standalone Bilibili URLs; helper scripts emit JSON, pipe-delimited search results, and local history files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default recommendation count is 10 songs; recommendations are intended to be generated once per day and de-duplicated against local history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
