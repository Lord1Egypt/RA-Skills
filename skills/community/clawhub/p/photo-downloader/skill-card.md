## Description: <br>
批量下载豆瓣电影、电视剧和综艺的剧照与海报，支持按内容名称搜索、分类下载、缓存去重和小批量下载。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zj-john](https://clawhub.ai/user/zj-john) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find public Douban media entries and download small batches of stills or posters for personal, learning, research, or private use. It is intended for movie, TV, and variety-show images, not logged-in content or large-scale scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run an unpinned npm install for Playwright during normal use. <br>
Mitigation: Prefer installing dependencies through the platform setup path before execution and run the skill in a low-privilege environment. <br>
Risk: The skill performs web scraping and downloads public Douban images, which may be subject to site terms and rate limits. <br>
Mitigation: Keep download limits small, avoid large-scale crawling, and use it only for content and purposes allowed by the target site. <br>
Risk: Privacy and session behavior is potentially confusing because older text mentions existing browser sessions while current guidance advises against them. <br>
Mitigation: Do not use real browser sessions or logged-in profiles with this skill; use a fresh headless browser context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zj-john/photo-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Downloaded image files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes image files under ~/.openclaw/output/photo-download and skips files already present in the cache.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
