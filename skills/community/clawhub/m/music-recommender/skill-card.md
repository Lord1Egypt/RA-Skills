## Description: <br>
Analyze NetEase Cloud Music playlists, profile listening taste, and recommend non-repeated songs with playable Bilibili links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn a NetEase Cloud Music playlist into a daily taste profile and music recommendation list. It helps avoid repeat recommendations by checking local history before producing a new list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playlist-derived data is sent to NetEase Cloud Music and Bilibili while fetching playlist contents and searching for playable links. <br>
Mitigation: Use the skill only with playlists and searches the user is comfortable sharing with those services. <br>
Risk: Recommendation history is stored locally in clear text under the user's OpenClaw workspace. <br>
Mitigation: Avoid using the skill for sensitive listening data, and delete the local history files when retention is no longer needed. <br>
Risk: Optional exports to Notion, HTML, or text files can save recommendation data outside the immediate chat response. <br>
Mitigation: Use optional exports only when the user explicitly wants the recommendations saved elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geekfoxcharlie/music-recommender) <br>
- [Publisher profile](https://clawhub.ai/user/geekfoxcharlie) <br>
- [NetEase Cloud Music playlist API](https://music.163.com/api/v6/playlist/detail?id=<ID>&n=1000) <br>
- [Bilibili search API](https://api.bilibili.com/x/web-interface/search/all/v2?keyword=<query>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style recommendation list with song names, short group headings, and Bilibili URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may also read and write local JSON history files to enforce once-per-day recommendations and avoid repeated songs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
