## Description: <br>
Helps agents summarize public NetEase Cloud Music playlists, songs, artists, rankings, and performance metrics without downloading content or performing bulk scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect public NetEase Cloud Music pages and produce lightweight summaries of playlists, tracks, artists, rankings, and recent performance metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repeated page visits or broad trigger wording could cause unintended browsing or automation. <br>
Mitigation: Confirm before browsing or making repeated page visits, and keep request frequency low. <br>
Risk: Logged-in account use could expose private account details or perform unwanted account actions. <br>
Mitigation: Use logged-in context only for user-approved personal page organization, avoid sharing private account details, and do not automate account interactions. <br>
Risk: Platform compliance issues could arise from downloading, reverse engineering, bypassing controls, or bulk collection. <br>
Mitigation: Restrict use to public pages and lightweight summaries; do not download, reverse engineer, bypass controls, or batch scrape. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/CodeKungfu/netease-music) <br>
- [NetEase Cloud Music](https://music.163.com/) <br>
- [NetEase Cloud Music Toplist](https://music.163.com/#/discover/toplist) <br>
- [NetEase Cloud Music Search](https://music.163.com/#/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public music links, extracted page metadata, and lightweight statistics; does not include downloads, reverse engineering, or bulk scraping.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
