## Description:

批量下载豆瓣电影、电视剧和综艺的剧照与海报，支持按名称搜索、分类下载、缓存去重和反爬延迟。

This skill is for research and development only.

## Publisher:

[zj-john](https://clawhub.ai/user/zj-john)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media workflow users can use this skill to ask an agent for commands and guidance that download a small batch of public Douban stills or posters for a named movie, TV series, or variety show.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install Playwright as an unpinned npm package at runtime.

Mitigation: Install a reviewed, pinned Playwright dependency yourself before running the downloader.

Risk: The skill makes Douban network requests and writes downloaded images under the user's home directory.

Mitigation: Run it only in an environment where those requests and file writes are acceptable, and review the requested content type, count, and output path.

Risk: The single-page downloader can be given arbitrary URLs despite the release being intended for Douban media pages.

Mitigation: Avoid passing non-Douban URLs to download.js and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zj-john/skills/photo-downloader)
- [Publisher profile](https://clawhub.ai/user/zj-john)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Node.js shell commands and downloaded image files on disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded images under ~/.openclaw/output/photo-download by default and prints progress, counts, failures, and save paths.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
