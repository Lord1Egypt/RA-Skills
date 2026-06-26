## Description: <br>
搜索并播放电影。功能包括：(1) 按类型、年份、评分筛选电影；(2) 支持中英文输入；(3) 展示电影海报、评分、剧情简介；(4) 生成可点击的 iframe 播放页面，直接在线观看。触发场景包括：搜索电影、想看电影、找最新电影、按类型/年份/评分筛选电影。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chugenice](https://clawhub.ai/user/chugenice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for movies by title, genre, year, rating, or language and to generate local HTML playback pages when a source is selected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search unvetted free-streaming sites and create local HTML pages that load arbitrary third-party iframe content. <br>
Mitigation: Review every playback URL before opening generated files, avoid entering personal information in embedded pages, and prefer domain allowlists, iframe sandboxing, HTML escaping, and explicit confirmation before file creation. <br>
Risk: Streaming source reliability and legitimacy may vary because the skill selects third-party sources discovered through search. <br>
Mitigation: Prefer licensed providers, verify source domains before use, and fall back to metadata-only results when a trusted playback source is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chugenice/movie-finder) <br>
- [Installation guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses plus generated HTML files and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML pages that embed third-party iframe playback URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
