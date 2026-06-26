## Description: <br>
Kugou helps agents summarize public Kugou Music playlists, charts, song pages, and artist pages for lightweight trend and style analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect public Kugou Music pages and summarize song, playlist, chart, and artist performance data for internal trend tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in Kugou pages may expose personal library or account information if an agent is allowed to inspect them. <br>
Mitigation: Use the skill on public pages by default and only allow inspection of personal pages that the user explicitly wants summarized. <br>
Risk: Automated access to dynamic pages can trigger platform controls or exceed acceptable request volume. <br>
Mitigation: Use human-opened pages, keep request frequency low, and avoid batch scraping, downloads, API reverse engineering, or automated interactions. <br>


## Reference(s): <br>
- [Kugou Music Homepage](https://www.kugou.com/) <br>
- [Kugou Ranking Page](https://www.kugou.com/yy/rank/home/1-8888.html) <br>
- [Kugou Search Page](https://www.kugou.com/yy/html/search.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/mike47512/kugou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links, public music metadata, popularity metrics, and style or language distribution summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
