## Description: <br>
中文新闻门户列表抓取，可输出 Markdown 简报或 JSON/RSS，无需新闻类 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Chinese news headlines and links from configured portal list pages or RSS feeds, then produce a concise Markdown brief or structured JSON/RSS-style output for aggregation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches web pages and RSS feeds, which can expose destination choices or retrieve untrusted remote content. <br>
Mitigation: Use the documented host allowlist for stricter control, keep private-address blocking enabled, and review requested sources before running the fetch script with sensitive workflows. <br>
Risk: Broad trigger wording could route unrelated news requests to this skill. <br>
Mitigation: Invoke it with explicit Chinese news aggregation intent and confirm output settings such as pages, feeds, limits, and format before execution. <br>
Risk: Fetched headlines and links may be incomplete, blocked, stale, or inaccurate because they depend on source sites and heuristic extraction. <br>
Mitigation: Treat results as source links for review, follow source-site terms and robots guidance, and verify important facts against the original publishers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/news-cn) <br>
- [JisuAPI Publisher Profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI Website](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefs, JSON objects, or command guidance with inline JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can group results by source, limit per-source and total item counts, deduplicate titles, and emit fetch warnings to stderr when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
