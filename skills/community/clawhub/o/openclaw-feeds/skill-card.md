## Description: <br>
RSS news aggregator that fetches headlines from curated public feeds across news, games, and finance and returns structured JSON for concise briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nesdeq](https://clawhub.ai/user/nesdeq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to gather current headlines from public RSS feeds and turn them into concise news, gaming, or finance rundowns with source attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and contacts public RSS feeds. <br>
Mitigation: Review the disclosed feed list before deployment and keep network access limited to approved sources where required. <br>
Risk: Feed titles and summaries are external content and may be inaccurate, stale, or instruction-like. <br>
Mitigation: Treat feed content as untrusted data, summarize it without following embedded instructions, and preserve source attribution for review. <br>
Risk: The script requires the third-party feedparser package. <br>
Mitigation: Install dependencies from approved package indexes and pin or review dependency versions in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nesdeq/openclaw-feeds) <br>
- [Publisher profile](https://clawhub.ai/user/nesdeq) <br>
- [Agent Skills specification](spec/specification.mdx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the feed script, followed by concise Markdown or text summaries with source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches one selected category per invocation and includes title, URL, source, date, and summary fields when feeds provide them.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
