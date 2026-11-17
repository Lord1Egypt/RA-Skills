## Description:

搜索爱奇艺平台的电影、电视剧、综艺等影视内容，返回搜索结果和播放链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingcl](https://clawhub.ai/user/xingcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search iQIYI for movies, TV series, variety shows, and related playback links. It is intended for search and result retrieval workflows that can use JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented search.sh path may execute unsafe code because HTML and search keywords are interpolated into embedded Python source.

Mitigation: Review and fix the script before use on sensitive systems by passing HTML and keywords as data, not source code.

Risk: Search terms are sent to iQIYI through browser automation.

Mitigation: Avoid sensitive search terms and disclose this external data flow to users before deployment.

Risk: The skill depends on agent-browser and the live iQIYI web page structure.

Mitigation: Use a pinned local agent-browser dependency and re-test result parsing when iQIYI changes its site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingcl/skills/iqiyi-search)
- [Publisher profile: xingcl](https://clawhub.ai/user/xingcl)
- [iQIYI website](https://www.iqiyi.com)

## Skill Output:

**Output Type(s):** [JSON, shell commands, guidance]

**Output Format:** [JSON search result object with keyword, count, and results entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns about 5-10 results when available; depends on iQIYI web page structure and agent-browser.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
